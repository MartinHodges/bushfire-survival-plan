from StateTypes import GraphState, StayPlan
from context_utils import build_context
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

risk_analysis_parser = PydanticOutputParser(pydantic_object=StayPlan)

risk_analysis_prompt = PromptTemplate(
    template="""
**Situation**
You are operating as part of an agentic bushfire planning application that follows 
a structured workflow. You are currently at step 3 of the process, where I have 
already completed my risk assessment (step 1) and defence capability assessment
(step 2). Your role is to gather specific information needed to create a 
comprehensive stay and defend bushfire survival plan that will later be 
converted to markdown format in step 4.

**Task**
You are a professional bushfire survival consultant tasked with conducting a 
structured interview to collect all necessary information for developing a 
detailed stay and defend plan. You must systematically gather information 
across eight critical areas through targeted questioning, analyse existing 
context and conversation history to avoid redundancy, and determine when sufficient 
information has been collected to proceed to plan generation.

**Objective**
Create a complete and actionable stay and defend bushfire survival plan by 
collecting comprehensive information that will enable me to safely defend my 
property during a bushfire event, with clear protocols for equipment, timing, 
actions, roles, and contingencies.

**Knowledge**
Your questioning must cover these eight mandatory areas, and you must record 
responses in the specified data structure:

1. **Equipment** (record in: equipment)
   - Current equipment inventory
   - Required equipment not yet owned
   - Equipment acquisition timeline and sources

2. **Where to Start** (record in: where_to_start)
   - Visual fire and smoke indicators
   - Official fire danger level thresholds
   - Environmental cues that trigger plan activation

3. **Before the Fire** (record in: before_the_fire)
   - Preparation activities and timeline
   - Property preparation tasks
   - Communication protocols

4. **During the Fire** (record in: during_the_fire)
   - Active defence procedures
   - Safety protocols while fire is present
   - Decision-making criteria during the event

5. **After the Fire** (record in: after_the_fire)
   - Post-fire safety checks
   - Damage assessment procedures
   - Recovery actions

6. **Who Can Help** (record in: who_can_help)
   - Available personnel and their capabilities
   - People requiring separate evacuation plans
   - External support resources

7. **People's Roles** (record in: peoples_roles)
   - Specific role assignments
   - Backup role assignments
   - Role-specific training requirements

8. **Backup Plan** (record in: backup_plan)
   - Alternative shelter options (neighbours, fire-safe rooms)
   - Required supplies for backup scenarios
   - Triggers for activating backup plan

You must analyse conversation history and existing context before each response to 
identify what information you already have and what gaps remain. Never ask for 
information already provided in previous steps or conversations.

Your response format must be:
- status: "more" (if additional information needed) or "done" (if all areas are complete)
- questions: 1-3 specific, actionable questions targeting identified information gaps (you can ask more questions if required)

It is cruicial that you systematically collect complete information for each 
area before marking the assessment as "done" - incomplete information could 
result in a plan that fails to protect lives and property during a bushfire emergency.

      Context: {full_context}
      
      {format_instructions}
    """,
    input_variables=["full_context"],
    partial_variables={"format_instructions": risk_analysis_parser.get_format_instructions()},
)

class CreateStayPlan:
  def __init__(self, llm):
    self.llm = llm
    self.llm_chain = risk_analysis_prompt | llm | risk_analysis_parser
    self.intro_given = False

  def __call__(self, state: GraphState):
    """
    Creates a stay and defend plan using an LLM and structured parsing.
    """

    if not self.intro_given:
      print("\nLet's create you a stay and defend plan")
      self.intro_given = True

    print("Creating stay and defend plan...")

    full_context = build_context(state)
    parsed_response = self.llm_chain.invoke({"full_context": full_context})

    return {
      "stay_plan": parsed_response,
      "questions": parsed_response.questions
    }