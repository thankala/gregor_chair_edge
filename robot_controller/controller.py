import typing
from typing import Any

from lib.interface import Interface
from time import sleep


class RobotController:
    def __init__(self, name: str = 'robot1', port: str = '/dev/ttyUSB'):
        self.name = name
        self.port = port + '_' + name
        self.doBot = Interface(self.port)

        if self.doBot.connected():
            self.doBot.set_device_name(self.name)
            print(f'doBot: {self.doBot.get_device_name()} is connected.')
            self.home()
        else:
            print(f'doBot: {self.doBot} is not connected.')

    def home(self):
        self.move(260, 0, 90, 90)
        self.ungrip()

    # Primitive functions
    def move(self, x: Any, y: Any, z: Any, r: Any):
        pose = self.get_pose()
        is_same = lambda a, b: abs(a - b) >= 0.0001
        if is_same(pose["x"], x) and is_same(pose["y"], y) and is_same(pose["z"], z) and is_same(pose["r"], r):
            return

        self.doBot.set_point_to_point_command(1, x, y, z, r)
        self.block()

    def grip(self, enable_control: bool = True, enable_grip: bool = True):
        control, grip = self.doBot.get_end_effector_gripper()
        if grip:
            return

        self.doBot.set_end_effector_gripper(True, True)
        self.doBot.wait(300)
        self.doBot.set_end_effector_gripper(False, True)
        self.block()

    def ungrip(self):
        control, grip = self.doBot.get_end_effector_gripper()
        if not grip:
            return

        self.doBot.set_end_effector_gripper(True, False)
        self.doBot.wait(300)
        self.doBot.set_end_effector_gripper(False, True)
        self.block()

    def wait(self, ms: Any):
        self.doBot.wait(ms)
        self.block()

    def get_pose(self) -> typing.Dict[str, float]:
        pose = self.doBot.get_pose()[0:4]
        return {
            'x': pose[0],
            'y': pose[1],
            'z': pose[2],
            'r': pose[3]
        }

    def clear_alarms(self):
        self.doBot.clear_alarms_state()

    def get_alarms_state(self):
        return self.doBot.get_alarms_state()

    def block(self):
        self.doBot.wait(0)
        queue_index = self.doBot.get_current_queue_index()
        while True:
            if self.doBot.get_current_queue_index() > queue_index:
                break

            sleep(0.5)

    # Composite functions
    def move_to(self, name: str):
        if name == "W2":
            if self.name == 'robot1':
                self.move(260, -120, 90, 90)
            if self.name == 'robot2':
                self.move(260, 120, 90, 90)
            if self.name == "robot3":
                raise Exception("Robot3 cannot move to W2.")
        if name == "W1":
            if self.name == 'robot1':
                self.move(260, 120, 90, 90)
            if self.name == 'robot2':
                self.move(260, -120, 90, 90)
            if self.name == "robot3":
                self.move(260, 0, 90, 90)

    def pick_and_place(self):
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))

    def pick_and_insert(self):
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.grip()
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.ungrip()
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))

    def pick_and_flip_and_press(self):
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.grip()
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.ungrip()
        self.grip()
        self.ungrip()
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))

    def screw_pick_and_fasten(self):
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') - 45,
                  self.get_pose().get('r'))
        self.grip()
        self.ungrip()
        self.grip()
        self.ungrip()
        self.move(self.get_pose().get('x'),
                  self.get_pose().get('y'),
                  self.get_pose().get('z') + 45,
                  self.get_pose().get('r'))
