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
Provides an implementation of the uniform speed distribution.  In this case a
speed of a node is assigned at random with the uniform probability
distribution.
"""


from sim2net.speed._speed import Speed
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Uniform(Speed):
    """
    This class implements the uniform speed distribution that assigns node's
    speeds from a given range with equal probability.
    """

    def __init__(self, minimal_speed, maximal_speed):
        """
        *Parameters*:
            - **minimal_speed** (`float`): a value of a node's minimal speed;
            - **maximal_speed** (`float`): a value of a node's maximal speed.
        """
        super(Uniform, self).__init__(Uniform.__name__)
        check_argument_type(Uniform.__name__, 'minimal_speed', float,
                            minimal_speed, self.logger)
        self.__minimal_speed = float(minimal_speed)
        check_argument_type(Uniform.__name__, 'maximal_speed', float,
                            maximal_speed, self.logger)
        self.__maximal_speed = float(maximal_speed)
        if self.__minimal_speed == self.__maximal_speed:
            self.__current_speed = float(self.__minimal_speed)
        else:
            self.__current_speed = None
            self.get_new()

    @property
    def current(self):
        """
        (*Property*)  A value of the current speed of type `float` (or `None`
        if the value has yet not been assigned).
        """
        return self.__current_speed

    def get_new(self):
        """
        Assigns a new speed value.

        .. warning::

            Depending on distribution parameters, negative values may be
            randomly selected.

        *Returns*:
            (`float`) the absolute value of a new speed.
        """
        if self.__minimal_speed == self.__maximal_speed:
            return self.__current_speed
        self.__current_speed = \
            self.random_generator.uniform(self.__minimal_speed,
                                          self.__maximal_speed)
        return self.__current_speed
