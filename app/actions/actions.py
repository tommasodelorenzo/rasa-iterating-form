from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, FollowupAction
import logging

class ActionStartForm(Action):
    """
    Custom action starting the form 'my_form'.
    It gets called by 'action_end_form' to iterate the info retrieval by 'my_form'.
    """
    def name(self) -> Text:
        return "action_start_form"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict
    ) -> List[EventType]:

        # needed only to dispatch the current iteration step
        current_iteration = int(tracker.get_slot('current_iteration'))
        dispatcher.utter_message(text=f"Iteration {current_iteration}.")

        # triggering my_form
        return [FollowupAction('my_form')]

class ActionEndForm(Action):
    """
    Custom action called when 'my_form' is completed.
    This function saves the current iteration slots in 'iterations', and then:
        - If additional iterations are still needed, it resets the required slots and triggers 'action_start_form'.
        - If instead it is the last iteration needed, it just utter a final message.
    """
    def name(self) -> Text:
        return "action_end_form"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict
    ) -> List[EventType]:

        N = int(tracker.get_slot('N'))
        current_iteration = int(tracker.get_slot('current_iteration'))

        # saving the current iteration slots as a dictionary in 'iterations'
        form_slots = domain['forms']['my_form']['required_slots']    
        iteration = {slot: tracker.get_slot(slot) for slot in form_slots}
        iterations = tracker.get_slot('iterations').copy()
        iterations.append(iteration)
        events = [SlotSet(key="iterations", value=iterations)]

        if current_iteration != N:

            # reseting the required slots    
            events.extend([SlotSet(key=slot, value=None) for slot in form_slots])
            # incrementing the current_iteration value
            events.append(SlotSet(key="current_iteration", value=current_iteration+1))
   
            # triggering 'action_start_form'
            events.append(FollowupAction(name="action_start_form"))
        else:
            dispatcher.utter_message(text=f"All {N} iterations completed. Your inputs: {', '.join([k['lorem-ipsum'] for k in iterations])}")
            
        return events


class ActionSessionStart(Action):
    """
    This action gets triggered by /start and /restart commands.
    It simply asks for the value N of iterations needed.
    """
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        events = [SessionStarted()]

        dispatcher.utter_message(response='utter_ask_N')

        events.append(ActionExecuted("action_listen"))

        return events
