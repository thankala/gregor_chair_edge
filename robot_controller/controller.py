import typing
from typing import Any

from serial.serialutil import SerialException

from lib.interface import Interface
from time import sleep


class RobotController:
    def __init__(self, serial_number: str, name: str = 'robot1', port: str = '/dev/ttyUSB', ):
        print(f'Initializing doBot: {name} with serial number: {serial_number}')
        self.name = name
        self.doBot = None
        for i in range(10):
            try:
                interface = Interface(port + str(i))
                interface_serial = str(interface.get_device_serial_number())
                print("Checking serial number: " + interface_serial + " on port: " + port + str(i))
                if serial_number == interface_serial.strip('\x00'):
                    self.doBot = interface
                    self.port = port + str(i)
                    break
            except SerialException:
                print("Unable to find doBot on port: " + port + str(i))
                continue
            except AttributeError:
                print("An error has occurred")
                continue

        if self.doBot is None:
            raise Exception("Unable to find doBot on any port.")
        if self.doBot.connected():
            self.doBot.set_device_name(self.name)
            print(f'doBot: {self.doBot.get_device_name()} is connected.')
            self.home()
        else:
            print(f'doBot: {self.doBot} is not connected.')

    def get_pose(self) -> typing.Dict[str, float]:
        pose = self.doBot.get_pose()[0:4]
        return {
            'x': pose[0],
            'y': pose[1],
            'z': pose[2],
            'r': pose[3]
        }

    def home(self):
        current_pose = self.get_pose()
        if self.name == "robot1":
            self.move(current_pose.get('x'), current_pose.get('y'), 90, current_pose.get('r'))
            self.move(260, 0, 90, 0)
        elif self.name == "robot2":
            self.move(current_pose.get('x'), current_pose.get('y'), 90, current_pose.get('r'))
            self.move(260, 0, 90, 50)
        elif self.name == "robot3":
            self.move(current_pose.get('x'), current_pose.get('y'), 90, current_pose.get('r'))
            self.move(260, 0, 90, 0)
        self.ungrip()

    # Primitive functions
    def move(self, x: Any, y: Any, z: Any, r: Any) -> typing.Dict[str, any]:
        self.doBot.set_point_to_point_command(1, x, y, z, r)
        self.block()
        return {'x': x, 'y': y, 'z': z, r: 'r'}

    def grip(self, enable_control: bool = True, enable_grip: bool = True):
        self.doBot.set_end_effector_gripper(enable_control, enable_grip)
        self.block()
        self.doBot.set_end_effector_gripper(False, False)
        self.block()

    def ungrip(self):
        self.doBot.set_end_effector_gripper(True, False)
        self.block()
        self.doBot.set_end_effector_gripper(False, False)
        self.block()

    def wait(self, ms: Any):
        self.doBot.wait(ms)
        self.block()

    def clear_alarms(self):
        self.doBot.clear_alarms_state()

    def get_alarms_state(self):
        return self.doBot.get_alarms_state()

    def block(self):
        self.doBot.wait(50)
        queue_index = self.doBot.get_current_queue_index()
        while True:
            if self.doBot.get_current_queue_index() > queue_index:
                break
            sleep(0.5)

    # Composite functions
    def move_to(self, name: str) -> typing.Dict[str, float]:
        current_pose = self.get_pose()
        if name == "W1":
            if self.name == 'robot1':
                self.move(260, 110, 90, current_pose.get('r'))
            elif self.name == 'robot2':
                self.move(260, -110, 90, current_pose.get('r'))
            elif self.name == "robot3":
                self.move(260, 0, 90, current_pose.get('r'))
        elif name == "W2":
            if self.name == 'robot1':
                self.move(270, -90, 40, current_pose.get('r'))
            elif self.name == 'robot2':
                self.move(270, 80, 40, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}.")
        elif name == "CB1":
            if self.name == "robot1":
                self.move(230, -120, 40, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}.")
        elif name == "CB2":
            if self.name == "robot3":
                self.move(220, -150, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "CB3":
            if self.name == "robot3":
                self.move(220, 190, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B1":
            if self.name == "robot1":
                self.move(210, 90, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B2":
            if self.name == "robot1":
                self.move(200, 180, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B3":
            if self.name == "robot1":
                self.move(290, 0, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B4":
            if self.name == "robot2":
                self.move(170, -160, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B5":
            if self.name == "robot2":
                self.move(290, 20, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B6R":
            if self.name == "robot3":
                self.move(160, 180, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        elif name == "B6L":
            if self.name == "robot3":
                self.move(210, 170, 20, current_pose.get('r'))
            else:
                raise Exception(f"{self.name} cannot move to {name}")
        else:
            raise Exception(f"{self.name} cannot move to {name}")
        return self.get_pose()

    def pick(self):
        current_pose = self.get_pose()
        self.grip()
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  110,
                  current_pose.get('r'))

    def place(self):
        current_pose = self.get_pose()
        self.ungrip()
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  110,
                  current_pose.get('r'))
    
    def screw(self):
        self.grip()
        current_pose = self.get_pose()
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z'),
                  -100)
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z'),
                  100)
        self.ungrip()
        # self.move(current_pose.get('x'),
        #           current_pose.get('y'),
        #           current_pose.get('z'),
        #           -100)
        # self.move(current_pose.get('x'),
        #           current_pose.get('y'),
        #           current_pose.get('z') + 30,
        #           100)
        # self.move(current_pose.get('x'),
        #           current_pose.get('y'),
        #           current_pose.get('z'),
        #           current_pose.get('r'))

    def flip(self):
        current_pose = self.get_pose()
        self.grip()
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z') + 30,
                  current_pose.get('r'))
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z'),
                  current_pose.get('r'))
        self.ungrip()
    

    def press(self):
        current_pose = self.get_pose()
        self.grip()
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z') + 30,
                  current_pose.get('r'))
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z'),
                  current_pose.get('r'))
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z') + 30,
                  current_pose.get('r'))
        self.move(current_pose.get('x'),
                  current_pose.get('y'),
                  current_pose.get('z'),
                  current_pose.get('r'))
        self.ungrip()

    # def screw_pick_and_fasten(self):
    #     current_pose = self.get_pose()
    #     self.grip()
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               -100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z') + 30,
    #               100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               -100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               100)
    #     self.move(current_pose.get('x'),
    #               current_pose.get('y'),
    #               current_pose.get('z'),
    #               current_pose.get('r'))
