from StateTypes import GraphState
from context_utils import check_quit
from pprint import pprint

class Choice:
  def __init__(self, llm, section, choice, options):
      self.llm = llm
      self.section = section
      self.choice = choice
      self.options = options

  def __call__(self, state: GraphState):

    # pprint(state)

    print("\nI need you to make a decision.")

    section_obj = getattr(state, self.section, None)
    choice_section = getattr(section_obj, 'choice', None) if section_obj else []
    choices_made = getattr(choice_section, 'choices_made', {}) if choice_section else {}

    if len(self.options) == 0:
        print("I have no options for you to select from. I must go now!")
        exit(0)

    valid = False
    while not valid:
        user_input = input(f"\n{self.choice}\nYour choice: {'/'.join(self.options)}: ")
        check_quit(user_input)
        valid = user_input.lower() in [opt.lower() for opt in self.options]
        if not valid:
            print(f"\nInvalid choice. Please select from: {'/'.join(self.options)}")

    choices_made[self.choice] = user_input
    
    # Update choice_section directly since it's already working for choices_made
    if hasattr(choice_section, 'last_choice'):
        choice_section.last_choice = user_input
    
    choice_location = f"{self.section}.choice"

    return {
       choice_location: choice_section
    }