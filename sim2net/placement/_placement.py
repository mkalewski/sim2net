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
Contains an abstract class that should be implemented by all placement classes.
"""


from abc import ABCMeta, abstractmethod

from sim2net.utility import logger
from sim2net.utility.randomness import get_random_generator


__docformat__ = 'reStructuredText'


#pylint: disable=R0921
class Placement(object):
    """
    This class is an abstract class that should be implemented by all placement
    model classes.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name):
        """
        *Parameters*:
            - **name** (`str`): a name of the implemented placement model.
        """
        self.__random_generator = get_random_generator()
        assert self.__random_generator is not None, \
               'A random generator object expected but "None" value got!'
        self.__logger = logger.get_logger('placement.' + str(name))
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

    @abstractmethod
    def get_placement(self):
        """
        Generates placement positions and returns the result as a dictionary.

        *Returns*:
            A dictionary containing the placement information.

        *Raises*:
            - **NotImplementedError**: this method is an abstract method.
        """
        raise NotImplementedError('The abstract class "Placement" has' \
                                  ' no implementation of the' \
                                  ' "get_placement()" method!')

    @staticmethod
    def position_conflict(horizontal_coordinates, vertical_coordinates,
                          index=-1):
        """
        If *index* is less than 0, checks whether the given coordinates are
        unique, that is, if no two points have the same horizontal and vertical
        coordinates.  Otherwise, checks if there is a point that has the same
        coordinates as these at the *index* position.

        *Parameters*:
            - **horizontal_coordinates** (`list`): a list of horizontal
              coordinates;
            - **vertical_coordinates** (`list`): a list of vertical
              coordinates;
            - **index** (`int`): an index of the coordinate lists; if greater
              than -1, it is checked whether there is a point with the same
              horizontal and vertical coordinates as at *index*.

        *Returns*:
            (`int`) an index of the coordinate that is in conflict, or -1 if
            the given coordinates are unique.

        *Raises*:
            - **ValueError**: if given coordinate lists have different lengths,
              or if a given value of the *index* parameter is greater than the
              total number of coordinates.

        *Examples*:

        .. testsetup::

            from sim2net.placement._placement import Placement

        .. doctest::

            >>> Placement.position_conflict([1, 2, 2, 4], [5, 6, 6, 7])
            2
            >>> Placement.position_conflict([1, 2, 2, 4], [5, 6, 6, 7], 1)
            2
            >>> Placement.position_conflict([1, 2, 2, 4], [5, 6, 6, 7], 0)
            -1
        """
        if len(horizontal_coordinates) <= 0:
            raise ValueError('Parameter "horizontal_coordinates": no' \
                             ' coordinates given!')
        if len(vertical_coordinates) <= 0:
            raise ValueError('Parameter "vertical_coordinates": no' \
                             ' coordinates given!')
        if len(horizontal_coordinates) != len(vertical_coordinates):
            raise ValueError('The given horizontal and vertical coordinate' \
                             ' lists have different lengths!')
        if index > len(horizontal_coordinates):
            raise ValueError('Parameter "index": the given number is grater' \
                             ' than the total number of coordinates!')
        unique_positions = {}
        for idx, pos in enumerate(list(zip(horizontal_coordinates,
                                           vertical_coordinates))):
            if index > -1:
                if index == idx:
                    continue
                if (horizontal_coordinates[index],
                    vertical_coordinates[index]) == pos:
                    return idx
            else:
                try:
                    unique_positions[pos]
                except KeyError:
                    unique_positions[pos] = 1
                else:
                    return idx
        return -1
