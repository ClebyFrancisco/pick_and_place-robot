from transitions import Machine
import time
import random
from test_robot import TestRobot
from robot import Robot
from bank_movements import BANK_MOVEMENT

class PickAndPlaceRobot:
    def __init__(self, robot):
        self.robot = robot
        self.attempts = 0
        self.max_attempts = 3

        states = ['idle', 'pick', 'error', 'retry', 'place', 'finished', 'abort']

        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'pick'},
            {'trigger': 'fail', 'source': 'pick', 'dest': 'error'},
            {'trigger': 'retry_pick', 'source': 'error', 'dest': 'retry'},
            {'trigger': 'retry_decision', 'source': 'retry', 'dest': 'pick', 'conditions': 'can_retry', 'unless': 'should_abort'},
            {'trigger': 'abort_retry', 'source': 'retry', 'dest': 'abort', 'conditions': 'should_abort'},
            {'trigger': 'success', 'source': 'pick', 'dest': 'place'},
            {'trigger': 'place_success', 'source': 'place', 'dest': 'finished'},
            {'trigger': 'reset', 'source': ['finished', 'abort'], 'dest': 'idle'}
        ]

        self.machine = Machine(model=self, states=states, transitions=transitions, initial='idle')

    def connect(self):
        self.robot.connect()
        print(self.state)

    def disconnect(self):
        self.robot.disconnect()

    def can_retry(self):
        return self.attempts < self.max_attempts

    def should_abort(self):
        return self.attempts >= self.max_attempts

    def on_enter_idle(self):
        input("Pressione qualquer tecla para iniciar o processo de pick and place...")
        self.start()


    def on_enter_pick(self):
        self.robot.move_joints(BANK_MOVEMENT.get('quadrant_1'))
        self.robot.gripper(0.3)
        time.sleep(1)
        self.robot.move_cartesian(BANK_MOVEMENT.get('medicine_1'))
        time.sleep(1)
        self.robot.gripper(0.8)
        time.sleep(1)
        self.robot.move_cartesian(BANK_MOVEMENT.get('medicine_1_recoil'))
        time.sleep(1)
        if random.choice([True, False]):  # Simula uma chance de falha
            print("Falha ao pegar o objeto.")
            self.fail()
        else:
            print("Sucesso ao pegar o objeto.")
            time.sleep(1)
            self.success()

    def on_enter_error(self):
        print("Erro ocorrido. Tentativa de recuperação...")
        self.retry_pick()

    def on_enter_retry(self):
        input("Pressione qualquer tecla para tentar novamente...")
        self.attempts += 1
        if self.can_retry():
            self.retry_decision()
        else:
            self.abort_retry()

    def on_enter_place(self):
        self.robot.move_joints(BANK_MOVEMENT.get('drop_safe_1'))
        self.robot.move_cartesian(BANK_MOVEMENT.get('drop_1'))
        self.robot.gripper(0.3)
        
        time.sleep(2)
        self.robot.move_joints(BANK_MOVEMENT.get('drop_safe_1'))
        print("Peça colocada com sucesso.")
        self.place_success()

    def on_enter_finished(self):
        self.robot.move_joints(BANK_MOVEMENT.get('home'))
        print("Processo de pick and place finalizado com sucesso.")
        input("Pressione qualquer tecla para resetar o sistema...")
        self.attempts = 0
        self.reset()

    def on_enter_abort(self):
        self.robot.move_joints(BANK_MOVEMENT.get('home'))
        print("Máximo de tentativas atingido. Processo abortado.")
        input("Pressione qualquer tecla para resetar o sistema...")
        self.reset()

def main():
    system = True
    robot = None
    while system:
        if robot is None:
            print("****MENU DE ESCOLHA DO ROBÔ****\n"
                  "[1] Robô real\n"
                  "[2] Robô de teste\n"
                  "Para sair digite uma letra:\n")
            choice = input()
            if choice.isnumeric():
                choice = int(choice)
                while choice not in [1, 2]:
                    print('Escolha invalida, escolha 1 ou 2.')
                    choice = int(input())
                if choice == 1:
                    robot = Robot()
                elif choice == 2:
                    robot = TestRobot()
                pick_place_robot = PickAndPlaceRobot(robot)
                pick_place_robot.connect()

                while True:
                    pick_place_robot.on_enter_idle()
                    time.sleep(1)  

            else:
                print('Saindo do programa')
                system = False
        else:
            pick_place_robot.disconnect()

if __name__ == '__main__':
    main()
