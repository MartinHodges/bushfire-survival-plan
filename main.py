from dotenv import load_dotenv
from context_utils import check_quit, print_context, value_with_default
from Choice import AskChoice
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from StateTypes import GraphState
import time
import nodes
from datetime import datetime
from AssessRisk import AssessRisk
from AssessDefence import AssessDefence
from Questions import AskQuestions
from CreateLeavePlan import CreateLeavePlan
from CreateStayPlan import CreateStayPlan
from ShowPlan import ShowPlan

load_dotenv()

llm = init_chat_model("gpt-4o")

# Build graph
graph_builder = StateGraph(GraphState)
graph_builder.add_node(nodes.CLASSIFY_RISK_NODE, AssessRisk(llm))
graph_builder.add_node(nodes.ASK_RISK_QUESTIONS_NODE, AskQuestions("risk_assessment"))
graph_builder.add_node(nodes.CONTINUE_WITH_PLAN_NODE, AskChoice("risk_assessment", "Continue with plan?", ["yes","no"]))
graph_builder.add_node(nodes.ASSESS_DEFENCE_NODE, AssessDefence(llm))
graph_builder.add_node(nodes.ASK_DEFENCE_QUESTIONS_NODE, AskQuestions("defence_assessment"))
graph_builder.add_node(nodes.ASK_STRATEGY_NODE,  AskChoice("defence_assessment", "Do you want to create a leave early or stay and defend plan?", ["leave", "stay"]))
graph_builder.add_node(nodes.CREATE_LEAVE_PLAN_NODE,  CreateLeavePlan(llm))
graph_builder.add_node(nodes.ASK_LEAVE_PLAN_QUESTIONS_NODE, AskQuestions("leave_plan"))
graph_builder.add_node(nodes.CREATE_STAY_PLAN_NODE,  CreateStayPlan(llm))
graph_builder.add_node(nodes.ASK_STAY_PLAN_QUESTIONS_NODE, AskQuestions("stay_plan"))
graph_builder.add_node(nodes.SHOW_PLAN_NODE,  ShowPlan(llm))

# define edges to constrain what nodes are accessible from another
# fixed edges

graph_builder.add_edge(START, nodes.CLASSIFY_RISK_NODE)
graph_builder.add_edge(nodes.ASK_RISK_QUESTIONS_NODE, nodes.CLASSIFY_RISK_NODE)
graph_builder.add_edge(nodes.ASK_DEFENCE_QUESTIONS_NODE, nodes.ASSESS_DEFENCE_NODE) 
graph_builder.add_edge(nodes.ASK_STAY_PLAN_QUESTIONS_NODE, nodes.CREATE_STAY_PLAN_NODE) 
graph_builder.add_edge(nodes.ASK_LEAVE_PLAN_QUESTIONS_NODE, nodes.CREATE_LEAVE_PLAN_NODE) 
graph_builder.add_edge(nodes.SHOW_PLAN_NODE, END)

graph_builder.add_conditional_edges(
    source=nodes.CLASSIFY_RISK_NODE,
    path=lambda state: value_with_default(state.risk_assessment.risk_level, ['low', 'high', 'unclear']),
    path_map={
        "unclear": nodes.ASK_RISK_QUESTIONS_NODE,
        "low": nodes.CONTINUE_WITH_PLAN_NODE,
        "high": nodes.CONTINUE_WITH_PLAN_NODE,
        "default": nodes.CLASSIFY_RISK_NODE
    }
)

graph_builder.add_conditional_edges(
    source=nodes.CONTINUE_WITH_PLAN_NODE,
    path=lambda state: value_with_default(state.risk_assessment.choice.last_choice, ['no', 'yes']),
    path_map={
        "yes": nodes.ASSESS_DEFENCE_NODE,
        "no": END,
        "default": nodes.CONTINUE_WITH_PLAN_NODE
    }
)

graph_builder.add_conditional_edges(
    source=nodes.ASSESS_DEFENCE_NODE,
    path=lambda state: value_with_default(state.defence_assessment.capability_level, ['low', 'high', 'unclear']),
    path_map={
        "unclear": nodes.ASK_DEFENCE_QUESTIONS_NODE,
        "low": nodes.ASK_STRATEGY_NODE,
        "high": nodes.ASK_STRATEGY_NODE,
        "default": nodes.ASSESS_DEFENCE_NODE
    }
)

graph_builder.add_conditional_edges(
    source=nodes.ASK_STRATEGY_NODE,
    path=lambda state: value_with_default(state.defence_assessment.choice.last_choice, ['stay', 'leave']),
    path_map={
        "stay": nodes.CREATE_STAY_PLAN_NODE,
        "leave": nodes.CREATE_LEAVE_PLAN_NODE,
        "default": nodes.ASK_STRATEGY_NODE
    }
)

graph_builder.add_conditional_edges(
    source=nodes.CREATE_LEAVE_PLAN_NODE,
    path=lambda state: value_with_default(state.leave_plan.plan_status, ['more', 'done']),
    path_map={
        "more": nodes.ASK_LEAVE_PLAN_QUESTIONS_NODE,
        "done": nodes.SHOW_PLAN_NODE,
        "default": nodes.CREATE_LEAVE_PLAN_NODE
    }
)

graph_builder.add_conditional_edges(
    source=nodes.CREATE_STAY_PLAN_NODE,
    path=lambda state: value_with_default(state.stay_plan.plan_status, ['more', 'done']),
    path_map={
        "more": nodes.ASK_STAY_PLAN_QUESTIONS_NODE,
        "done": nodes.SHOW_PLAN_NODE,
        "default": nodes.CREATE_STAY_PLAN_NODE
    }
)

graph = graph_builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=[]
)

# diagram = graph.get_graph().draw_mermaid_png()
# with open("diagram.png", "wb") as f:
#     f.write(diagram)

def run_chatbot():
    print("\nAt any time, enter 'quit', 'exit' or just 'q' to exit\n")

    thread_id = f"conversation_{int(time.time() * 1000)}"
    config = {"configurable": {"thread_id": thread_id}}
    
    user_input = input("\n\nTell me about why you want to create a bushfire plan:\n")
    check_quit(user_input)

    prompt = """
**Situation**
You are an expert emergency management consultant specializing in Australian bushfire preparedness. 
You're assisting me in creating a comprehensive bushfire survival plan tailored to 
my specific circumstances. This is the initial interaction that will set the foundation 
for developing their personalized bushfire plan.

**Task**
Introduce yourself and explain the bushfire planning process to me. Explain that you
will collect essential information about their property, location, household composition,
and any specific concerns as the process unfolds.

**Objective**
To establish rapport with the user, set appropriate expectations for the planning 
process, and gather the foundational information needed to develop a thorough and 
personalized bushfire survival plan that will help protect lives and property.

**Knowledge**
Bushfire plans typically address property details, surrounding vegetation, 
access routes, water sources, equipment availability, household member capabilities, 
and evacuation options.
Different regions have varying bushfire risks and regulations.
Household composition (including children, elderly, people with disabilities, pets) 
significantly impacts planning decisions.
Property characteristics (building materials, surrounding vegetation, water access) 
determine defendability.
Early decision-making about whether to stay and defend or leave early is critical to 
survival.

**Constraints**
Accept that I might not be able to answer your questions. When this happens
do not ask the question again.
   """

    graph.invoke({
        "messages": [HumanMessage(content=prompt)],
        "user_motivation": user_input,
    }, config)

    while True:
        current_state = graph.get_state(config)
        if not current_state.next or current_state.next == END:
            # print_context(current_state)
            plan = current_state.values.get('final_plan')
            if plan:
                print("\nPlanning complete - here is your plan:")
                print("-" * 50)
                for line in current_state.values['final_plan']['content']:
                    print(line)
            else:
                print("Planning complete - no plan created")
            break

        graph.invoke(None, config)

if __name__ == "__main__":
    run_chatbot()