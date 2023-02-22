from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType, FollowupAction
import logging

class ActionStartForm(Action):
    def name(self) -> Text:
        return "action_start_form"

    def run(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict
    ) -> List[EventType]:


        N = int(tracker.get_slot('N'))
        current_iteration = int(tracker.get_slot('current_iteration'))

        dispatcher.utter_message(text=f"Iteration {current_iteration}.")

        return [FollowupAction('my_form')]

class ActionEndForm(Action):
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

        form_slots = domain['forms']['my_form']['required_slots']
            
        iteration = {slot: tracker.get_slot(slot) for slot in form_slots}
        iterations = tracker.get_slot('iterations').copy()
        iterations.append(iteration)

        events = []

        events.append(SlotSet(key="iterations", value=iterations))

        if current_iteration != N:

            events.extend([SlotSet(key=slot, value=None) for slot in form_slots])
            events.append(SlotSet(key="current_iteration", value=current_iteration+1))
   
            events.append(FollowupAction(name="action_start_form"))
        else:
            dispatcher.utter_message(text=f"All {N} iterations completed. Your inputs: {', '.join([k['lorem-ipsum'] for k in iterations])}")
            
        return events


class ActionSessionStart(Action):
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
