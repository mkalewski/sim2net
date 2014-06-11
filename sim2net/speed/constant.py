#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
#
# This file is a part of the Simple Network Simulator (sim2net) project.
# USE, MODIFICATION, COPYING AND DISTRIBUTION OF THIS SOFTWARE IS SUBJECT TO
# THE TERMS AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY
# OF THE MIT LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY
# FROM HTTP://WWW.OPENSOURCE.ORG/.
#
# For bug reports, feature and support requests please visit
# <https://github.com/mkalewski/sim2net/issues>.

"""
Provides an implementation of a constant node speed.  In this case a speed of a
node is constant at a given value.
"""

from math import fabs

from sim2net.speed._speed import Speed
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Constant(Speed):
    """
    This class implements a constant node speed fixed at a given value.
    """

    def __init__(self, speed):
        """
        *Parameters*:
            - **speed** (`float`): a value of the node speed.

        *Example*:

        .. testsetup::

            from sim2net.speed.constant import Constant

        .. doctest::

            >>> speed = Constant(5.0)
            >>> speed.current
            5.0
            >>> speed.get_new()
            5.0
            >>> speed = Constant(-5.0)
            >>> speed.current
            5.0
            >>> speed.get_new()
            5.0
        """
        super(Constant, self).__init__(Constant.__name__)
        check_argument_type(Constant.__name__, 'speed', float, speed,
                            self.logger)
        self.__current_speed = fabs(float(speed))

    @property
    def current(self):
        """
        (*Property*)  The absolute value of the current speed of type `float`.
        """
        return self.__current_speed

    def get_new(self):
        """
        Returns the absolute value of the given node speed of type `float`.
        """
        return self.current
