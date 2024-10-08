from abc import ABC, abstractmethod


class AbstractRobot():
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
    def check_for_end_or_abort(self):
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
    def gripper(self):
        ...
