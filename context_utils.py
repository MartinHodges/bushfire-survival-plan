from openai import BaseModel
from StateTypes import GraphState
import json
from pprint import pprint

def check_quit(user_input):
    if user_input.lower() in ['exit', 'quit', 'q']:
        print("Goodbye! ...")
        exit(0)

def build_context(state: GraphState):
    # Build context from all messages and answers
    context_parts = []
    
    if state.user_motivation:
        context_parts.append(f"User's reason for creating bushfire plan: {state.user_motivation}")
    
    for msg in state.messages:
        context_parts.append(msg.content)

    if state.risk_assessment:
        context_parts.append(f"Risk Assessment: {state.risk_assessment}")
    
    if state.defence_assessment:
        context_parts.append(f"Defence Assessment: {state.defence_assessment}")
    
    if state.leave_plan:
        context_parts.append(f"Leave Plan: {state.leave_plan}")
    
    if state.stay_plan:
        context_parts.append(f"Stay Plan: {state.stay_plan}")

    full_context = "\n\n".join(context_parts)

    return full_context

def value_with_default(value, values, state = None):
   if not state is None:
       print("State:")
       pprint(state)

   if value is None or not value.lower() in values:
       print(f"Using default as {value}")
       return 'default'
   return value.lower()

def print_context(state: GraphState):
    # Retrieve the underlying state data from the StateSnapshot object
    if hasattr(state, 'values'):
        underlying_state = state.values
    else:
        # Fallback for when the state is a simple dictionary
        underlying_state = state


    # Handle the case where the state is a dictionary
    # Convert non-serializable objects to serializable format
    state_copy = {}
    for k, v in underlying_state.items():
        if k != 'messages':
            if hasattr(v, 'model_dump'):
                state_copy[k] = v.model_dump()
            elif hasattr(v, '__dict__'):
                state_copy[k] = str(v)
            else:
                state_copy[k] = v
    
    json_output = json.dumps(state_copy, indent=2)
    print("--------------")
    print(f"""
    Current state:
    {json_output}
    """)
    
    # Print messages separately
    if 'messages' in underlying_state and underlying_state['messages']:
        print("--- Messages from the state ---")
        for msg in underlying_state['messages']:
            print(f"{msg.__class__.__name__}: {msg.content}")
    
    print("--------------")