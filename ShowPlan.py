from StateTypes import GraphState
from context_utils import build_context
from langchain_core.prompts import PromptTemplate

plan_prompt = PromptTemplate(
    template="""
Situation
You are an expert bushfire safety consultant tasked with creating the final deliverable 
of a comprehensive bushfire survival plan. This is the fourth and final step in an 
agentic workflow that has already completed risk assessment, defense capability 
evaluation, and stay/leave decision-making.

Task
Transform all previously collected information into a professional, well-structured, 
and actionable bushfire survival plan document in Markdown format that follows strict 
formatting guidelines while ensuring all critical safety information is properly 
organized and presented.

Objective
Create a clear, actionable bushfire survival plan document that I can easily reference
during an emergency, ensuring my safety and helping mr make informed decisions under 
pressure.

Knowledge
The plan must follow a specific structure with mandatory sections including
Risk Summary, Risk Level, Capability to Defend, Decision, and detailed action plans
based on whether the decision is to stay and defend or to leave. The document should
incorporate all previously gathered information from the risk assessment, defense
capability assessment, and stay/leave decision phases.

It is crucial that you ensure this document is comprehensive, clearly formatted, and 
contains all critical safety information without omission. The document must be 
immediately usable in an emergency situation where quick reference to information 
could save lives.

When creating the plan:

Use today's actual date in the title (not placeholder text).
Ensure all section headings use proper Markdown formatting.
Convert all assessment summaries into concise, actionable language.
Include specific triggers for action rather than vague guidelines.
Make sure all lists are properly formatted with bullet points.
Bold critical information that requires immediate attention.
Maintain a serious, authoritative tone throughout.
Ensure the document flows logically from risk assessment to specific actions.
Verify that all sections from the appropriate plan type (leave or stay) are
included and fully developed.
Double-check that no placeholder text remains in the final document.

    Context: {full_context}
    """,
    input_variables=["full_context"]
)

class ShowPlan:
  def __init__(self, llm):
    self.llm = llm
    self.llm_chain = plan_prompt | llm
    self.intro_given = False

  def __call__(self, state: GraphState):
    """
    Create a bushfire plan based on the information gathered
    """
    print("Entering ShowPlan")

    if not self.intro_given:
      print("\nDrafting your plan")
      self.intro_given = True

    full_context = build_context(state)
    response = self.llm_chain.invoke({"full_context": full_context})
    
    # Split the markdown into lines for display
    plan_lines = response.content.split('\n')
    
    return {
      "final_plan": {"content": plan_lines}
    }