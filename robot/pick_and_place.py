from transitions import Machine
from robot import TestRobot

class PickAndPlaceRobot:
    def __init__(self, robot):
        self.robot = robot
        self.attempts = 0

        states = ['idle', 'pick', 'error', 'retry', 'place', 'finished', 'abort']

        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'pick'},
            {'trigger': 'fail', 'source': 'pick', 'dest': 'error'},
            {'trigger': 'retry_pick', 'source': 'error', 'dest': 'retry'},
            {'trigger': 'retry_decision', 'source': 'retry', 'dest': 'pick'},
            {'trigger': 'abort_retry', 'source': 'retry', 'dest': 'abort'},
            {'trigger': 'success', 'source': 'pick', 'dest': 'place'},
            {'trigger': 'place_success', 'source': 'place', 'dest': 'finished'},
            {'trigger': 'reset', 'source': '*', 'dest': 'idle'}
        ]

        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle')

    def on_enter_idle(self):
        self.attempts = 0
        print("State: Idle - Waiting for operation.")
        input("Press any key to continue...")


