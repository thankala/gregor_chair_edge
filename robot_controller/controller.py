from typing import Any

from lib.interface import Interface
from time import sleep


class RobotController:
    def __init__(self, port: str = '/dev/ttyUSB0'):
        self.doBot = Interface(port)
        if self.doBot.connected():
            print(f'doBot: {self.doBot} is connected.')
        else:
            print(f'doBot: {self.doBot} is not connected.')

    # Primitive functions
    def move(self, x: Any, y: Any, z: Any, r: Any):
        self.doBot.set_point_to_point_command(1, x, y, z, r)
        self.block()

    def grip(self, enable_control: bool = True, enable_grip: bool = True):
        self.doBot.set_end_effector_gripper(enable_control, enable_grip)
        self.doBot.wait(300)
        self.block()

    def ungrip(self):
        self.doBot.set_end_effector_gripper(True, False)
        self.doBot.wait(300)
        self.doBot.set_end_effector_gripper(False, False)
        self.block()

    def wait(self, ms: Any):
        self.doBot.wait(ms)
        self.block()

    def get_pose(self):
        return self.doBot.get_pose()[0:4]

    def clear_alarms(self):
        self.doBot.clear_alarms_state()

    def block(self):
        self.doBot.wait(0)
        queue_index = self.doBot.get_current_queue_index()
        while True:
            if self.doBot.get_current_queue_index() > queue_index:
                break

            sleep(0.5)

    # Composite functions
    def place_part(self, x1: Any, y1: Any, z1: Any, r1: Any, x2: Any, y2: Any, z2: Any, r2: Any):
        self.ungrip()
        self.move(x1, y1, z1, r1)
        self.grip()
        self.move(x2, y2, z2, r2)
        self.ungrip()

    def move_and_screw(self, x: Any, y: Any, z: Any, r: Any, deg: Any):
        self.move(x, y, z, r)
        self.grip()
        self.move(x, y, z, 150)
        self.grip()
        self.move(x, y, z, 150 - deg)
        self.ungrip()
