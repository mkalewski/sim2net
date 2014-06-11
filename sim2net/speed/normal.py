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
Provides an implementation of the normal speed distribution.  In this case a
speed of a node is assigned at random with the normal, i.e.  Gaussian,
probability distribution.
"""

from sim2net.speed._speed import Speed
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Normal(Speed):
    """
    This class implements the normal speed distribution that assigns node's
    speeds with the Gaussian probability distribution.
    """

    def __init__(self, mean=0.0, standard_deviation=0.2):
        """
        (Defaults to **standard normal distribution**.)

        *Parameters*:
            - **mean** (`float`): a value of the expectation (default: `0.0`);
            - **standard_deviation** (`float`): a value of the standard
              deviation (default: `0.2`).
        """
        super(Normal, self).__init__(Normal.__name__)
        check_argument_type(Normal.__name__, 'mean', float, mean, self.logger)
        self.__mean = float(mean)
        check_argument_type(Normal.__name__, 'standard_deviation', float,
                            standard_deviation, self.logger)
        self.__standard_deviation = float(standard_deviation)
        self.__current_speed = None
        self.get_new()

    @property
    def mean(self):
        """
        (*Property*)  A value of the expectation of type `float`.
        """
        return self.__mean

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
        self.__current_speed = \
            self.random_generator.normal(self.__mean,
                                         self.__standard_deviation)
        return self.__current_speed
