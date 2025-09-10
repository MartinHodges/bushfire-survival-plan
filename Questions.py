from StateTypes import GraphState
from context_utils import check_quit

class AskQuestions:
  def __init__(self, section):
      self.section = section

  def __call__(self, state: GraphState):

    print("\nI need a bit more information")

    section_obj = getattr(state, self.section, None)
    
    questions_section = getattr(section_obj, 'questions', None) if section_obj else None
    questions = questions_section.questions if questions_section else []
    answers = questions_section.answers if questions_section else {}
    
    if len(questions) == 0:
        print("I have no questions to ask.")
        return

    for question in questions:
        user_input = input(f"\n{question}\nYour answer: ")
        check_quit(user_input)
            
        answers[question] = user_input

    # Return empty dict to avoid overwriting - LangGraph will handle the state update
    # The answers are already updated in the existing questions_section object
    return {}