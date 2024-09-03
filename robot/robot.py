from kortex_api.Exceptions.KException import KException
from kortex_api.autogen.messages import Base_pb2, DeviceConfig_pb2, Common_pb2
from abstract_robot import AbstractRobot
from robot_connection import RobotConnection
import time
import threading

TIMEOUT_DURATION = 20

class Robot(AbstractRobot):
    
    def __init__(self):
        self.device = None
        self.device_config = None
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
        self.device_config = self.device.get_device_config_client()
        print("robot connected!")
        
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
        notification_handle = self.base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )
        
        self.base.ExecuteAction(self.action)
        finished = e.wait(TIMEOUT_DURATION)
        self.base.Unsubscribe(notification_handle)

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
        notification_handle = self.base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        print("Executing action")
        self.base.ExecuteAction(self.action)

        print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)
        self.base.Unsubscribe(notification_handle)
        return finished
    
    def apply_emergency_stop(self):
        self.base.ApplyEmergencyStop()
        self.critical_error = True
        print("Emergency")
    
    def check_for_end_or_abort(self, e):
        def check(notification, e = e):
            print("EVENT : " + \
                Base_pb2.ActionEvent.Name(notification.action_event))
            if notification.action_event == Base_pb2.ACTION_END \
            or notification.action_event == Base_pb2.ACTION_ABORT:
                e.set()
        return check

    def clear_faults(self):
        if self.critical_error:
            self.base.ClearFaults()
            self.critical_error = False
            print("Clear Faults")
    
    def check_faults(self) -> bool:
        if self.critical_error:
            return True
        return False

    def gripper(self, value: float = 0.70) -> None:
        self.gripper_command = Base_pb2.GripperCommand()
        finger = self.gripper_command.gripper.finger.add()

        self.gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = value
        self.base.SendGripperCommand(self.gripper_command)
        
        
    