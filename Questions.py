from StateTypes import GraphState
from context_utils import check_quit

class Questions:
  def __init__(self, llm, section):
      self.llm = llm
      self.section = section

  def __call__(self, state: GraphState):

    print("\nI need a bit more information")

    section_obj = getattr(state, self.section, None)
    questions_section = getattr(section_obj, 'questions', None) if section_obj else []
    questions = getattr(questions_section, 'questions', []) if questions_section else []
    answers = getattr(questions_section, 'answers', None) if questions_section else {}
 
    if len(questions) == 0:
        print("I have no questions to ask.")
        return

    for question in questions:
        user_input = input(f"\n{question}\nYour answer: ")
        check_quit(user_input)
            
        answers[question] = user_input

    questions_location = f"{self.section}.questions"

    return {
       questions_location: {**getattr(state, self.section, {}).__dict__, "answers": answers}
    }