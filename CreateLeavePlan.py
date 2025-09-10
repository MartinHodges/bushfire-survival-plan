from StateTypes import GraphState, LeavePlan
from context_utils import build_context
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

risk_analysis_parser = PydanticOutputParser(pydantic_object=LeavePlan)

risk_analysis_prompt = PromptTemplate(
    template="""
**Situation**
You are operating as step 3 in a 4-step agentic bushfire planning application workflow. 
I have already completed risk assessment (step 1) and defence capability assessment 
(step 2), and you now need to create a comprehensive leave plan. This is a critical 
safety planning exercise where incomplete or inaccurate information could have 
life-threatening consequences.

**Task**
Systematically collect all necessary information through targeted questioning to 
build a complete bushfire leave plan covering six mandatory areas: when to leave, 
where to go, how to get there, what to take, who to tell, and backup plan. 
You must analyze existing context and conversation history to identify information 
gaps, ask precise follow-up questions, and record responses in the specified data 
structure. Your life depends on you ensuring no critical safety information is missed.

**Objective**
Generate a comprehensive, actionable leave plan that enables me to make informed 
evacuation decisions and execute them safely during a bushfire emergency, ultimately 
contributing to my survival and the protection of my family and property.

**Knowledge**
You must cover these six mandatory areas through systematic questioning:

1. **When to Leave**: (record in when_to_leave)
Identify specific trigger conditions including fire danger ratings (Catastrophic,
Extreme, Severe), observable warning signs (smoke colour/direction, ember showers, 
temperature spikes), official alerts (Emergency Alert, Watch and Act, Advice), 
media reports, and personal comfort thresholds.

2. **Where to Go**: (record in where_to_go)
Establish multiple safe destination options with specific addresses, contact details, 
and confirmation of availability. Consider distance from fire-prone areas, accommodation 
capacity, pet-friendly options, and accessibility requirements.

3. **How to Get There**: (record in Map how_to_get_there
Primary and alternative evacuation routes with specific road names, identify potential 
hazards or bottlenecks, determine appropriate vehicles, account for traffic conditions, 
and plan for mobility-impaired individuals or large families.

4. **What to Take**: (record in what_to_take)
Create prioritised packing lists including critical documents (identification, 
insurance, medical records), irreplaceable items (photos, heirlooms), essential 
supplies (medications, baby/pet needs), financial resources (cash, cards), and 
appropriate clothing/equipment.

5. **Who to Tell**: (record in who_to_tell)
Establish communication protocols including emergency contacts, family notification 
procedures, workplace requirements, neighbour arrangements, and check-in schedules 
with designated safety contacts.

6. **Backup Plan**: (record in backup_plan)
Develop contingency options for failed evacuation including shelter-in-place procedures, 
neighbour arrangements, community safe spaces, emergency supply requirements, and 
communication methods when trapped.

You must analyze conversation history and existing context before each interaction to 
avoid redundant questions and identify specific information gaps. Ask no more than 3 
focused questions per interaction to avoid overwhelming me while maintaining systematic 
progress through all areas. Only ask questions that are relevant to creating the plan.

Your response format must be:
- status: "more" (if additional information needed) or "done" (if all areas are complete)
- questions: 1-3 specific, actionable questions targeting identified information gaps (you can ask more questions if required)

    Context: {full_context}
    
    {format_instructions}
    """,
    input_variables=["full_context"],
    partial_variables={"format_instructions": risk_analysis_parser.get_format_instructions()},
)

class CreateLeavePlan:
  def __init__(self, llm):
    self.llm = llm
    self.llm_chain = risk_analysis_prompt | llm | risk_analysis_parser
    self.intro_given = False

  def __call__(self, state: GraphState):
    """
    Creates a leave plan using an LLM and structured parsing.
    """

    if not self.intro_given:
      print("\nLet's create you a leave plan")
      self.intro_given = True

    print("Creating leave plan...")

    full_context = build_context(state)
    parsed_response = self.llm_chain.invoke({"full_context": full_context})

    return {
      "leave_plan": parsed_response,
      "questions": parsed_response.questions
    }