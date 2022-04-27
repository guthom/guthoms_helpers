from torch.optim.lr_scheduler import _LRScheduler
from typing import Optional, List
import math

class ExponentialDecay(_LRScheduler):

    def __init__(self, optimizer, gamma, last_epoch=-1, milestones: Optional[List[int]]=None):
        self.gamma = gamma
        self.lastLearningrate = []
        self.milestones = milestones
        super(ExponentialDecay, self).__init__(optimizer, last_epoch)

    def Calculate(self):
        ret = [self.base_lrs[group] * math.exp(-self.gamma * (self.last_epoch - 1)) for group in range(self.optimizer.param_groups.__len__())]
        self.lastLearningrate = ret
        return ret

    def get_lr(self):
        targetEpoch = self.last_epoch - 1

        if self.milestones != None:
            if targetEpoch in self.milestones:
                return self.Calculate()

        return self.Calculate()
