import maya.cmds as cmds
import math
import os

for i in range(1,249):
    cmds.parentConstraint(f'Net_joint{i}', f'Root_joint{i}', mo=False)
