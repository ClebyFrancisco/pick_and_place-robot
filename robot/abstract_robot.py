from abc import ABC, abstractmethod


class AbstractRobot(ABC):
    """
    This class is an abstract class for the robot.
    """

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def check_finished(self):
        ...

    @abstractmethod
    def clear_faults(self):
        ...

    @abstractmethod
    def move_joints(self, joints_list):
        ...

    @abstractmethod
    def move_cartesian(self, pose_list):
        ...

    @abstractmethod
    def apply_emergency_stop(self):
        ...
        
    @abstractmethod
    def check_faults(self):
        ...
    @abstractmethod
    def open_gripper(self, value):
        ...
