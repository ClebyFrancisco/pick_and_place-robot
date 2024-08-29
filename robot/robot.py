from kortex_api.Exceptions.KException import KException
from kortex_api.autogen.messages import Base_pb2, DeviceConfig_pb2, Common_pb2
from abstract_robot import AbstractRobot
from robot_connection import RobotConnection
from transitions import Machine
import time
import threading

class Robot(AbstractRobot):
    
    def __init__(self):
        self.device = None
        self.device_config = None
        self.gripper = None
        self.base_cyclic = None
        self.base = None
        self.action = None
        self.action_finished = True
        self.critical_error = None
        self.gripper_command = None
    
    def connect(self, connection_ip: str = "192.168.2.10") -> None:
        self.device = RobotConnection.create_tcp_connection(connection_ip)
        self.device.connect()
        
        self.base = self.device.get_base_client()
        self.base_cyclic = self.device.get_base_cyclic_client()
        self.gripper = self.device.get_gripper_cyclic_client()
        self.device_config = self.device.get_device_config_client()
        print("robot conettec")
        
    def disconnect(self) -> None:
        if self.device is None:
            return
        self.device.disconnect()
        print("Robot desconectado")
        
    def move_joints(self, joints_list: list[float]) -> bool:
        self.action = Base_pb2.Action()
        self.action.name = "Angular action movement"
        self.action.application_data = ""

        for joint_id in range(len(joints_list)):
            joint_angle = self.action.reach_joint_angles.joint_angles.joint_angles.add()
            joint_angle.joint_identifier = joint_id
            joint_angle.value = joints_list[joint_id]

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )
        
        base.ExecuteAction(action)
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        return finished

    def move_cartesian(self, pose_list: list[float]) -> bool:
        self.action = Base_pb2.Action()
        self.action.name = "Example Cartesian action movement"
        self.action.application_data = ""

        cartesian_pose = self.action.reach_pose.target_pose
        cartesian_pose.x = pose_list[0]  
        cartesian_pose.y = pose_list[1]  
        cartesian_pose.z = pose_list[2] 
        cartesian_pose.theta_x = pose_list[3]  
        cartesian_pose.theta_y = pose_list[4] 
        cartesian_pose.theta_z = pose_list[5] 

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        print("Executing action")
        base.ExecuteAction(action)

        print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)
        return finished
    
    def apply_emergency_stop(self):
        self.base.ApplyEmergencyStop()
        self.critical_error = True
        print("Emergency")
    
    def check_finished(self):
        if self.check_finished:
            return True
        return False

    def clear_faults(self):
        if self.critical_error:
            self.base.ClearFaults()
            self.critical_error = False
            print("Clear Faults")
    
    def check_faults(self) -> bool:
        if self.critical_error:
            return True
        return False

    def open_gripper(self, value: float = 0.70) -> None:
        self.gripper_command = Base_pb2.GripperCommand()
        finger = self.gripper_command.gripper.finger.add()

        self.gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = value
        self.base.SendGripperCommand(self.gripper_command)
        
        
    
if __name__ == "__main__":
    robot = Robot()
    
    robot.connect()
    
    time.sleep(3)
    
    robot.disconnect()
    time.sleep(3)
    robot.connect()
    
    # robot.open_gripper()
    
    time.sleep(3)
    
    robot.apply_emergency_stop()
    
    time.sleep(3)
    
    robot.clear_faults()
    
    robot.disconnect()
    
    # if robot.move_joints([88.112, 327.125, 138.133, 236.530, 84.188, 94.708]):
    #     print("Moveu por juntas")
        
    if robot.move_cartesian([19.344, 3.946, -0.177, 291.928, 58.471, 102.523]):
        print("Moveu por cart")
        
    # if robot.move_cartesian([0.1, 0.0, 0.1, 0.0, 0.0, 0.0]):