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
Provides an implementation of a rectangular simulation area in the
two-dimensional space.
"""

from sim2net.area._area import Area
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Rectangle(Area):
    """
    This class implements a rectangular simulation area of the given size in
    the two-dimensional space with the origin in (0, 0).
    """

    def __init__(self, width, height):
        """
        *Parameters*:
            - **width** (`float`): a width of the rectangular simulation area
              (along the horizontal x-axis),
            - **height** (`float`): a height of the rectangular simulation area
              (along the vertical y-axis).

        *Raises*:
            - **ValueError**: raised when a given value of either **width** or
              **height** parameter is equal to or less than 0.
        """
        super(Rectangle, self).__init__(Rectangle.__name__)
        check_argument_type(Rectangle.__name__, 'width', float, width,
                            self.logger)
        if width <= 0:
            raise ValueError('Parameter "width": the width of a simulation'
                             ' area cannot be equal to or less than 0, but'
                             ' %d given!' % float(width))
        self.__width = float(width)
        check_argument_type(Rectangle.__name__, 'height', float, height,
                            self.logger)
        if height <= 0:
            raise ValueError('Parameter "height": the height of a simulation'
                             ' area cannot be equal to or less than 0, but'
                             ' %d given!' % float(height))
        self.__height = float(height)

    @property
    def height(self):
        """
        (*Property*)  A height of the simulation area of type `float`.
        """
        return self.__height

    @property
    def width(self):
        """
        (*Property*)  A width of the simulation area of type `float`.
        """
        return self.__width

    def within(self, horizontal_coordinate, vertical_coordinate):
        """
        Tests whether the given coordinates are within the simulation area.

        *Parameters*:
            - **horizontal_coordinate** (`float`): a horizontal (x-axis)
              coordinate;
            - **vertical_coordinate** (`float`): a vertical (y-axis)
              coordinate.

        *Returns*:
            (`bool`) `True` if the given coordinates are within the rectangular
            simulation area, or `False` otherwise.
        """
        if horizontal_coordinate < 0.0 or vertical_coordinate < 0.0:
            return False
        if horizontal_coordinate <= self.__width \
                and vertical_coordinate <= self.__height:
            return True
        return False

    def get_area(self):
        """
        Creates a dictionary that stores information about the simulation area.

        *Returns*:
            A dictionary that stores information about the simulation area;
            it has the following fields:

                - 'area name': a name of the simulation area of type `str`,
                - 'width': a width of the simulation area of type `float`,
                - 'height': a height of the simulation area of type `float`.
        """
        return {'area name': self.__class__.__name__.lower(),
                'width': self.__width,
                'height': self.__height}
