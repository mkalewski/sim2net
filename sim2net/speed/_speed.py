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
Contains an abstract class that should be implemented by all speed distribution
classes.
"""


from abc import ABCMeta, abstractmethod, abstractproperty

from sim2net.utility import logger
from sim2net.utility.randomness import get_random_generator


__docformat__ = 'reStructuredText'


#pylint: disable=R0921
class Speed(object):
    """
    This class is an abstract class that should be implemented by all speed
    distribution classes.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name):
        """
        *Parameters*:
            - **name** (`str`): a name of the implemented speed distribution.
        """
        self.__random_generator = get_random_generator()
        assert self.__random_generator is not None, \
               'A random generator object expected but "None" value got!'
        self.__logger = logger.get_logger('speed.' + str(name))
        assert self.__logger is not None, \
               'A logger object expected but "None" value got!'

    @property
    def random_generator(self):
        """
        (*Property*)  An object representing the
        :class:`sim2net.utility.randomness._Randomness` pseudo-random number
        generator.
        """
        return self.__random_generator

    @property
    def logger(self):
        """
        (*Property*)  A logger object of the :class:`logging.Logger` class with
        an appropriate channel name.

        .. seealso::  :mod:`sim2net.utility.logger`
        """
        return self.__logger


    @abstractproperty
    def current(self):
        """
        (*Property*)  A value of the current speed of type `float`.

        *Raises*:
            - **NotImplementedError**: this property is an abstract property.
        """
        raise NotImplementedError('The abstract class "Speed" has' \
                                  ' no implementation of the "current"' \
                                  ' property!')

    @abstractmethod
    def get_new(self):
        """
        Assigns a new speed value.

        *Returns*:
            (`float`) a new speed value.

        *Raises*:
            - **NotImplementedError**: this method is an abstract method.
        """
        raise NotImplementedError('The abstract class "Speed" has' \
                                  ' no implementation of the "get_new()"' \
                                  ' method!')
