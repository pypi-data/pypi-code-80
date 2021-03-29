#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

import time
from .system_defs import SHORT_SLEEP_SEC


class VelocityMode(object):
    """VelocityMode is an object that allows the mobile platform to be controlled in velocity mode
    """

    TARGET_VELOCITY = "root/Control/hostInTargetVelocity"
    ACTUAL_VELOCITY_POLAR = "root/Control/VelocityIntegrator/velocityOutPolar"
    ACTUAL_VELOCITY_CARTESIAN = "root/Control/VelocityIntegrator/velocityOut"

    def __init__(self, req):
        self.__req = req

    def setVelocity(self, vel, timeout_sec=0):
        """VelocityMode controls the robot in velocity mode
            Args:
                vel(Velocity): target velocity

            Returns:
                status of the command execution.
        """

        if timeout_sec == 0:
            return self.__req.setParameter(VelocityMode.TARGET_VELOCITY, [vel.x(), vel.y(), vel.rz()])

        status = None
        while timeout_sec > 0:
            t0 = time.time()
            status = self.__req.setParameter(VelocityMode.TARGET_VELOCITY, [vel.x(), vel.y(), vel.rz()])
            t1 = time.time()
            timeout_sec -= (t1 - t0)
            if timeout_sec >= 0:
                time.sleep(SHORT_SLEEP_SEC)
                timeout_sec -= SHORT_SLEEP_SEC

        return status

    def getTargetVelocity(self):
        """Gets the current target velocity
            Returns:
                target velocity.

        """
        return self.__req.getParameter(VelocityMode.TARGET_VELOCITY).get().value

    def getActualVelocity(self):
        """Gets the actual velocity
            Returns:
                actual velocity.

        """
        return self.__req.getParameter(VelocityMode.ACTUAL_VELOCITY_POLAR).get().value
