from enum import Enum


class WorkbenchPin(Enum):
    OUT_1 = 27
    OUT_2 = 17
    OUT_3 = 22
    OUT_4 = 18

    def __str__(self):
        return self.name
