from abc import abstractmethod
from guthoms_helpers.base_types.BaseType import BaseType
from guthoms_helpers.base_types.VectorBase import VectorBase
from guthoms_helpers.base_types.RotationBase import RotationBase

from typing import List, Dict, Tuple

import numpy as np

class PoseBase(BaseType):

    def __init__(self, trans: VectorBase, rotation: RotationBase, visible: bool):
        self.trans: VectorBase = trans
        self.rotation: RotationBase = rotation
        self.visible: bool = visible

    def __add__(self, other: 'PoseBase') -> 'PoseBase':
        trans = other.trans + self.trans
        rot = other.rotation + self.rotation
        return type(self)(trans, rot, self.visible or other.visible)

    def __sub__(self, other: 'PoseBase') -> 'PoseBase':
        trans = other.trans - self.trans
        rot = other.rotation - self.rotation
        return type(self)(trans, rot, self.visible or other.visible)

    @abstractmethod
    def __getitem__(self, item):
        raise Exception("Nor Implemented!")
