from StateTypes import GraphState
from context_utils import check_quit

class AskChoice:
  def __init__(self, section, choice, options):
      self.section = section
      self.choice = choice
      self.options = options

  def __call__(self, state: GraphState):

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
    
    if hasattr(choice_section, 'last_choice'):
        choice_section.last_choice = user_input
    
    return {}