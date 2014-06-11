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
Contains an abstract class that should be implemented by all simulation area
classes.
"""


from abc import ABCMeta, abstractmethod, abstractproperty

from sim2net.utility import logger


__docformat__ = 'reStructuredText'


#pylint: disable=R0921
class Area(object):
    """
    This class is an abstract class that should be implemented by all
    simulation area classes.
    """

    __metaclass__ = ABCMeta

    #: The origin for simulation areas.
    ORIGIN = (0.0, 0.0)

    def __init__(self, name):
        """
        *Parameters*:
            - **name** (`str`): a name of the implemented simulation area.
        """
        self.__logger = logger.get_logger('area.' + str(name))
        assert self.__logger is not None, \
            'A logger object expected but "None" value got!'

    @property
    def logger(self):
        """
        (*Property*)  A logger object of the :class:`logging.Logger` class with
        an appropriate channel name.

        .. seealso::  :mod:`sim2net.utility.logger`
        """
        return self.__logger

    @abstractproperty
    def height(self):
        """
        (*Property*)  A height of the simulation area of type `float`.

        *Raises*:
            - **NotImplementedError**: this property is an abstract property.
        """
        raise NotImplementedError('The abstract class "Area" has no'
                                  ' implementation of the "height" property!')

    @abstractproperty
    def width(self):
        """
        (*Property*)  A width of the simulation area of type `float`.

        *Raises*:
            - **NotImplementedError**: this property is an abstract property.
        """
        raise NotImplementedError('The abstract class "Area" has no'
                                  ' implementation of the "width" property!')

    @abstractmethod
    def within(self, horizontal_coordinate, vertical_coordinate):
        """
        Tests whether the given coordinates are within the simulation area.

        *Parameters*:
            - **horizontal_coordinate** (`float`): a horizontal (x-axis)
              coordinate;
            - **vertical_coordinate** (`float`): a vertical (y-axis)
              coordinate.

        *Returns*:
            (`bool`) `True` if the given coordinates are within the simulation
            area, or `False` otherwise.

        *Raises*:
            - **NotImplementedError**: this method is an abstract method.
        """
        raise NotImplementedError('The abstract class "Area" has no'
                                  ' implementation of the "within()" method!')

    @abstractmethod
    def get_area(self):
        """
        Creates a dictionary that stores information about the simulation area.

        *Returns*:
            A dictionary containing the simulation area information.

        *Raises*:
            - **NotImplementedError**: this method is an abstract method.
        """
        raise NotImplementedError('The abstract class "Area" has no'
                                  ' implementation of the "get_area()"'
                                  ' method!')
