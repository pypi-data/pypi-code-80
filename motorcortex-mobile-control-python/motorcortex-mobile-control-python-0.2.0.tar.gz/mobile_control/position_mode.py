#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

from .planar_pose import PlanarPose
from .system_defs import MotionGeneratorStates, States
from enum import Enum
import time
from .system_defs import SHORT_SLEEP_SEC, TIMEOUT_INF


class PositionModeEvents(Enum):
    """List of events for the mobile platform in position mode"""
    EMPTY = 0
    GOTO_TARGET_POSITION = 1
    RESET = 2
    STOP = 6


class PositionMode(object):
    """PositionMode is an object that allows the mobile platform to be controlled in position mode
    """

    LOGIC_STATE_COMMAND = "root/Logic/stateCommand"
    LOGIC_MODE_COMMAND = "root/Logic/modeCommand"
    LOGIC_STATE = "root/Logic/state"
    LOGIC_MODE = "root/Logic/mode"
    SET_POSE = "root/Control/hostInTargetPosition"
    GLOBAL_POSE = "root/Control/globalPositionOut"
    RELATIVE_POSE_TR = "root/Control/TranslationFader/output"
    RELATIVE_POSE_ROT = "root/Control/RotationFader/output"
    HOSTIN_COMMAND = "root/Control/hostInCommand"
    CTRL_STATE = "root/Control/stateOut"

    def __init__(self, req):
        self.__req = req

    def setTargetPose(self, pose):
        """Sets mobile platform target pose

            Args:
                pose(PlanarPose): target pose

            Returns:
                status of the command execution.

        """
        return self.__req.setParameter(PositionMode.SET_POSE, [pose.x(), pose.y(), pose.rz()]).get()

    def getTargetPose(self):
        """Gets mobile platform current target pose
            Returns:
                target pose.

        """
        res = self.__req.getParameter(PositionMode.SET_POSE).get().value
        return PlanarPose(res[0], res[1], res[2])

    def getActualPose(self):
        """Gets mobile platform actual pose
            Returns:
                actual pose.

        """
        res = self.__req.getParameterList([PositionMode.RELATIVE_POSE_TR, PositionMode.RELATIVE_POSE_ROT]).get()
        return PlanarPose(res.params[0].value[0], res.params[1].value[0])

    def getGlobalPose(self):
        """Gets mobile platform global pose
            Returns:
                global pose.

        """
        res = self.__req.getParameter(PositionMode.GLOBAL_POSE).get().value
        return PlanarPose(res[0], res[1], res[2])

    def startMove(self):
        """Commands to start motion
            Returns:
                status of the command execution.

        """
        return self.__req.setParameter(PositionMode.HOSTIN_COMMAND, PositionModeEvents.GOTO_TARGET_POSITION.value).get()

    def stopMove(self):
        """Commands to stop motion
            Returns:
                status of the command execution.

        """
        return self.__req.setParameter(PositionMode.HOSTIN_COMMAND, PositionModeEvents.STOP.value).get()

    def resetPose(self):
        """Commands to reset motion
            Returns:
                status of the command execution.

        """
        return self.__req.setParameter(PositionMode.HOSTIN_COMMAND, PositionModeEvents.RESET.value).get()

    def isMoving(self):
        """Check if the platform is currently moving
            Returns:
                True if the platform is moving.

        """
        val = self.__req.getParameterList([PositionMode.CTRL_STATE, PositionMode.LOGIC_STATE]).get()
        ctrl_state = MotionGeneratorStates(val.params[0].value[0])
        logic_state = States(val.params[1].value[0])
        return (ctrl_state != MotionGeneratorStates.IDLE) or (logic_state == States.FREEZE_S) or (
                logic_state == States.MOBILITY_TRANSITION_S)

    def moveTo(self, pose, reset, timeout_sec=TIMEOUT_INF):
        """Commands the platform to move to a target pose, the move starts immediately (if allowed)
            Args:
                pose(PlanarPose): target pose
                reset(bool): flag to reset position integrator
                timeout_sec(float): timeout for the move
            Returns:
                status of the command execution.

        """
        if reset:
            self.resetPose()

        self.setTargetPose(pose)
        self.startMove()

        while self.isMoving():
            time.sleep(SHORT_SLEEP_SEC)
            timeout_sec -= SHORT_SLEEP_SEC
            if SHORT_SLEEP_SEC < 0:
                self.stopMove()
                return False

        return True
