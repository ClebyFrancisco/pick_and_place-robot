from kortex_api.Exceptions.KException import KException
from kortex_api.autogen.messages import Base_pb2, DeviceConfig_pb2, Common_pb2
from abstract_robot import AbstractRobot
from robot_connection import RobotConnection

class Robot(AbstractRobot):
    
    def __init__(self):
        self.device = None
        self.error_number = None
        self.action_finished = True
    
    def __connect(self, connection_ip: str = "192.168.2.10") -> None:
        self.device = RobotConnection.create_tcp_connection(connection_ip)
        self.device.connect()
        
    def disconnect(self) -> None:
        if self.device is None:
            return
        self.device.disconnect()
        
    def move_joints(self, joints_list):
        self.check_finished = False
        print(f'Moving joints from position: {joints_list[0]}, {joints_list[1]}, {joints_list[2]}, '
              f'{joints_list[3]}, {joints_list[4]}, {joints_list[5]}')
        sleep(0.001)
        self.check_finished = True
        return True

    def move_cartesian(self, pose_list):
        self.check_finished = False
        print(f'Moving cartesian pose from position: {pose_list[0]}, {pose_list[1]}, {pose_list[2]}, {pose_list[3]}, '
              f'{pose_list[4]}, {pose_list[5]}')
        sleep(0.001)
        self.check_finished = True
        return True
    
    def apply_emergency_stop(self):
        print('Applying emergency stop...')
        sleep(0.001)
    
    def check_finished(self):
        if self.check_finished:
            return True
        return False

    def clear_faults(self):
        print('Clearing faults...')
        self.error_number = 0
        sleep(0.001)
    
    def check_faults(self) -> bool:
        if self.error_number != 0:
            return True
        return False

    def gripper(self, value):
        self.check_finished = True
        
    
a = Robot()