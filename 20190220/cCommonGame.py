from enum import IntEnum
import numpy as np


class ShipType(IntEnum):
    MIL = 0
    CIV = 1


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(vars(self))


class ShipInfo:
    def __init__(self,
                 ship_id=0,
                 position=Position(0, 0),
                 heading=0,
                 size=0,
                 is_sunken=False,
                 ship_type=ShipType.MIL):
        self.ship_id = ship_id
        self.ship_type = ship_type
        # Position of of the ship head
        self.position = position
        self.heading = heading
        self.size = size
        self.is_sunken = is_sunken
        # list of position occupied by the vehicle
        # first position is the bow of the ship
        self.area = self.get_placement()

    def __repr__(self):
        return str(vars(self))

    def move_forward(self):
        head_rad = self.heading * np.pi / 180.0
        pos = np.array([0, -1])
        kin_mat = np.array([[np.cos(head_rad), np.sin(head_rad)],
                            [-np.sin(head_rad), np.cos(head_rad)]])
        transpose = np.dot(pos, kin_mat)
        transpose = transpose.astype(int)
        self.position.x += transpose[0]
        self.position.y += transpose[1]
        self.area = self.get_placement()

    def set_heading(self, heading):
        self.heading = heading
        self.area = self.get_placement()

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y
        self.area = self.get_placement()

    def turn_clockwise(self):
        self.heading += 90
        self.heading = self.wrap(self.heading)
        self.area = self.get_placement()

    def turn_counter_clockwise(self):
        self.heading -= 90
        self.heading = self.wrap(self.heading)
        self.area = self.get_placement()

    def get_placement(self):
        # get the upper half size of the ship
        half_size = (self.size - 1) // 2

        # Get the index of the ship
        placement = np.array([np.zeros(self.size),
                              np.arange(-half_size, (self.size - half_size)),
                              np.ones(self.size)])
        placement = np.transpose(placement)

        # Get the kinematic matrix
        head_rad = self.heading * np.pi / 180.0
        kin_mat = np.array([[np.cos(head_rad),  np.sin(head_rad),   0],
                            [-np.sin(head_rad), np.cos(head_rad),   0],
                            [self.position.x,   self.position.y,    1]])

        # compute the ship placement
        placement = np.dot(placement, kin_mat)

        # remove the last column
        placement = np.delete(placement, -1, 1)

        placement = np.round(placement)
        # remove the negative 0
        placement += 0.
        placement = placement.astype(int)

        return placement.tolist()

    @staticmethod
    def wrap(degree):
        result = ((degree + 180.0) % 360) - 180.0
        return result


class UwCollectedData:
    def __init__(self, N=[], NE=[], E=[], SE=[], S=[], SW=[], W=[], NW=[]):
        self.N = N
        self.NE = NE
        self.E = E
        self.SE = SE
        self.S = S
        self.SW = SW
        self.W = W
        self.NW = NW

    def __repr__(self):
        return str(vars(self))
		
class UwParams:
    def __init__(self,
                 civ_sr=[8,4,3,2],
                 civ_br=[3,4,3,4],
                 mil_sr=[12,10,8,7],
                 mil_br=[5,6,7,4],
				 SNR=[15,25],
				 SNR_decay=[1,1.5],
				 SNR_br=[1,2],
				 vector_len=100,
				 p_ml=0.1):
        self.civ_sr = civ_sr
        self.civ_br = civ_br
        self.mil_sr = mil_sr
        self.mil_br = mil_br
        self.SNR = SNR
        self.SNR_decay = SNR_decay
        self.SNR_br = SNR_br
        self.vector_len = vector_len
        self.p_ml = p_ml
