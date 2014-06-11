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
Provides an implementation of the grid placement model.

In the grid placement model nodes are placed at intersections of a square or
rectangular grid.  Usually, the grid has quadratic-shaped cells with edge
length that is close to the communication radius of a node.  It creates
networks that are regular in shape and provides excellent connectivity at a
startup.
"""


from math import modf, sqrt

from sim2net.placement._placement import Placement
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Grid(Placement):
    """
    This class implements the grid placement model, in which a given number of
    nodes are placed at intersections of a square or rectangular grid within a
    simulator area.
    """

    def __init__(self, area, nodes_number, transmission_range):
        """
        *Parameters*:
            - **area**: an object representing the simulation area;
            - **nodes_number** (`int`): a number of nodes to place within the
              simulation area;
            - **transmission_range** (`float`): a value of the transmission (or
              communication) radius of nodes, that is, the distance from a
              transmitter at which the signal strength remains above the
              minimum usable level.

        *Raises*:
            - **ValueError**: raised when: the given number of nodes or
              transmission range is less or equal to 0, or when the given value
              of the *area* parameter is `None`.
        """
        if area is None:
            raise ValueError('Parameter "area": a simulation area object'
                             ' expected but "None" value given!')
        super(Grid, self).__init__(Grid.__name__)
        self.__area = area
        check_argument_type(Grid.__name__, 'nodes_number', int, nodes_number,
                            self.logger)
        if nodes_number <= 0:
            raise ValueError('Parameter "nodes_number": the number of nodes'
                             ' cannot be less or equal to zero but %d given!' %
                             int(nodes_number))
        self.__nodes_number = int(nodes_number)
        check_argument_type(Grid.__name__, 'transmission_range', float,
                            transmission_range, self.logger)
        if transmission_range <= 0.0:
            raise ValueError('Parameter "transmission_range": a value of the'
                             ' transmission range cannot be less or equal to'
                             ' 0 but %f given!' % float(transmission_range))
        self.__transmission_range = float(transmission_range)

    def __adjust_grid_dimensions(self, columns, rows):
        """
        Adjusts the given grid dimensions to the size of the simulation area.
        If the area shape is square and the grid shape is rectangular, the
        longer side of the grid is placed along the horizontal x-axis of the
        simulation area.  If both shapes are rectangular, the longer side of
        the grid is placed along the longer size of the simulation area.

        *Parameters*:
            - **columns** (`int`): a number of grid columns;
            - **rows** (`int`): a number of grid rows.

        *Returns*:
            A number of grid columns and rows as a tuple.
        """
        if columns == rows:
            return (columns, rows)
        if self.__area.width == self.__area.height:
            if columns > rows:
                return (columns, rows)
            else:
                return (rows, columns)
        if self.__area.width > self.__area.height:
            if columns > rows:
                return (columns, rows)
            else:
                return (rows, columns)
        if self.__area.width < self.__area.height:
            if columns > rows:
                return (rows, columns)
            else:
                return (columns, rows)

    def __get_grid_dimensions(self):
        """
        Calculates dimensions of the grid based on the number of nodes.  If the
        number has a square root, the grid shape will be a square, otherwise it
        will be a rectangular.  In the worst case if the number of nodes is
        prime, the number of rows (or columns) will be equal to one.

        *Returns*:
            A number of grid columns and rows as a tuple.
        """
        if self.__nodes_number is None or self.__nodes_number <= 0:
            return (0.0, 0.0)
        dimensions = modf(sqrt(self.__nodes_number))
        if dimensions[0] == 0:
            return (int(dimensions[1]), int(dimensions[1]))
        for value in range(int(dimensions[1]), 0, -1):
            if modf(float(self.__nodes_number) / float(value))[0] == 0:
                return \
                    self.__adjust_grid_dimensions(value,
                                                  self.__nodes_number / value)

    def __get_nodes_distance(self, columns, rows):
        """
        Calculates a distance between nodes in the same row and column based on
        the their transmission ranges.  The distance is also adjust to fit the
        dimensions of the simulation area.

        *Returns*:
            A distance between nodes in the grid of type `float`.
        """
        distance = sqrt(0.5 * (self.__transmission_range *
                               self.__transmission_range))
        if distance * (columns + 1) > self.__area.width:
            distance = float(self.__area.width) / (float(columns) + 1.0)
        if distance * (rows + 1) > self.__area.height:
            distance = float(self.__area.height) / (float(rows) + 1.0)
        return distance

    def __get_horizontal_coordinates(self, columns, rows, distance):
        """
        Generates horizontal coordinates of nodes based on the number of
        columns, rows and the distance between nodes.

        *Returns*:
            A list of horizontal coordinates.
        """
        coordinates = []
        offset = 0.5 * (self.__area.width - ((columns + 1) * distance))
        for row in range(0, rows):
            coordinate = offset
            for column in range(0, columns):
                coordinate = coordinate + distance
                assert 0 <= coordinate <= self.__area.width, \
                    'The computed horizontal coordinate %f exceeds' \
                    ' dimensions of the simulation area!' % coordinate
                coordinates.append(coordinate)
        return coordinates

    def __get_vertical_coordinates(self, columns, rows, distance):
        """
        Generates vertical coordinates of nodes based on the number of
        columns, rows and the distance between nodes.

        *Returns*:
            A list of vertical coordinates.
        """
        coordinates = []
        offset = 0.5 * (self.__area.height - ((rows + 1) * distance))
        coordinate = offset
        for row in range(0, rows):
            coordinate = coordinate + distance
            assert 0 <= coordinate <= self.__area.height, \
                'The computed vertical coordinate %f exceeds dimensions' \
                ' of the simulation area!' % coordinate
            for column in range(0, columns):
                coordinates.append(coordinate)
        return coordinates

    def get_placement(self):
        """
        Generates grid placement coordinates for the given number of nodes and
        its transmission ranges and returns the result as a dictionary.

        *Returns*:
            A list of tuples of horizontal and vertical coordinates for each
            host.
        """
        columns, rows = self.__get_grid_dimensions()
        distance = self.__get_nodes_distance(columns, rows)
        horizontal_coordinates = \
            self.__get_horizontal_coordinates(columns, rows, distance)
        vertical_coordinates = \
            self.__get_vertical_coordinates(columns, rows, distance)
        self.logger.debug('Initial placement coordinates has been'
                          ' generated: %d nodes within %dx%d %s simulation'
                          ' area' %
                          (self.__nodes_number, self.__area.width,
                           self.__area.height,
                           self.__area.__class__.__name__.lower()))
        return zip(horizontal_coordinates, vertical_coordinates)
