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
Provides an implementation of the uniform placement model.

In the uniform placement model, a simulation area of a given size is chosen and
a given number of nodes are placed over it with the uniform probability
distribution.
"""


from sim2net.placement._placement import Placement
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Uniform(Placement):
    """
    This class implements implements the uniform placement model, in which  a
    given number of nodes are placed over a simulation area with the uniform
    probability distribution.
    """

    def __init__(self, area, nodes_number):
        """
        *Parameters*:
            - **area**: an object representing the simulation area;
            - **nodes_number** (`int`): a number of nodes to place over the
              simulation area.

        *Raises*:
            - **ValueError**: raised when the number of nodes is less or equal
              to 0, or when the given value of the *area* parameter is `None`.
        """
        if area is None:
            raise ValueError('Parameter "area": a simulation area object'
                             ' expected but "None" value given!')
        super(Uniform, self).__init__(Uniform.__name__)
        self.__area = area
        check_argument_type(Uniform.__name__, 'nodes_number', int,
                            nodes_number, self.logger)
        if nodes_number <= 0:
            raise ValueError('Parameter "nodes_number": the number of nodes'
                             ' cannot be less or equal to zero but %d given!' %
                             int(nodes_number))
        self.__nodes_number = int(nodes_number)

    def get_placement(self):
        """
        Generates uniform placement coordinates for the given number
        of nodes and returns the result as a dictionary.

        *Returns*:
            A list of tuples of horizontal and vertical coordinates for each
            host.
        """
        if self.__area is None or self.__nodes_number is None:
            return None
        while True:
            horizontal_coordinates = \
                [self.random_generator.uniform(0, self.__area.width)
                    for coordinate in range(0, self.__nodes_number)]
            vertical_coordinates = \
                [self.random_generator.uniform(0, self.__area.height)
                    for coordinate in range(0, self.__nodes_number)]
            if Placement.position_conflict(horizontal_coordinates,
                                           vertical_coordinates) == -1:
                break
        self.logger.debug('Initial placement coordinates has been'
                          ' generated: %d nodes within %dx%d %s simulation'
                          ' area' %
                          (self.__nodes_number, self.__area.width,
                           self.__area.height,
                           self.__area.__class__.__name__.lower()))
        return zip(horizontal_coordinates, vertical_coordinates)
