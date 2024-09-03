from abstract_robot import AbstractRobot
from transitions import Machine
import time

class TestRobot(AbstractRobot):
    """
    class test robot
    """

    def __init__(self):
        self.device = None
        self.base = None


    def connect(self, connection_ip: str = "192.168.2.10"):
        print("using Test Robot")
        print(f'Connecting to robot with IP: {connection_ip}')
        self.device = True
        self.base = True
        
    def disconnect(self):
        print('Disconnecting from robot...')
        self.device = None
        self.base = None
        time.sleep(0.001)

        
    def move_joints(self, joints_list):
        self.check_finished = False
        print(f'Moving joints from position: {joints_list[0]}, {joints_list[1]}, {joints_list[2]}, '
              f'{joints_list[3]}, {joints_list[4]}, {joints_list[5]}')
        time.sleep(0.001)
        self.check_finished = True
        return True

    def move_cartesian(self, pose_list):
        self.check_finished = False
        print(f'Moving cartesian pose from position: {pose_list[0]}, {pose_list[1]}, {pose_list[2]}, {pose_list[3]}, '
              f'{pose_list[4]}, {pose_list[5]}')
        time.sleep(0.001)
        self.check_finished = True
        return True
    
    def apply_emergency_stop(self):
        print('Applying emergency stop...')
        time.sleep(0.001)
    
    def check_for_end_or_abort(self):
        if self.check_finished:
            return True
        return False

    def clear_faults(self):
        print('Clearing faults...')
        self.error_number = 0
        time.sleep(0.001)
    
    def check_faults(self) -> bool:
        if self.error_number != 0:
            return True
        return False

    def gripper(self, value):
        print(value)
        
if __name__ == "__main__":
    robot = TestRobot()
    
    robot.connect()
    
    time.sleep(3)
    robot.gripper(0.7)
    
    robot.disconnect()
    time.sleep(3)
    robot.connect()
    
    # robot.open_gripper()
    
    time.sleep(3)
    
    robot.apply_emergency_stop()
    
    time.sleep(3)
    
    robot.clear_faults()
    
    robot.disconnect()
    