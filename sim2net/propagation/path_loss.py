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
This module provides an implementation of the simplified path loss model.

The path loss model predicts the reduction in attenuation (power density) a
signal encounters as it propagates through space.  In this simplified
implementation, it is presumed that for all nodes that are within transmission
range of each other, the **signal-to-noise ratio** (*SNR*) is above the minimal
usable level, and hence, the nodes are able to communicate directly.
"""


from math import pow, sqrt

from sim2net.propagation._propagation import Propagation
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class PathLoss(Propagation):
    """
    This class implements simplified path loss model in which the
    signal-to-noise ration is calculated on the given value of the transmission
    range of nodes.
    """

    def __init__(self, transmission_range):
        """
        *Parameters*:
            - **transmission_range** (`float`): a value of the transmission (or
              communication) radius of nodes, that is, the distance from a
              transmitter at which the signal strength remains above the
              minimum usable level.

        *Raises*:
            - **ValueError**: raised when the given transmission range is less
              or equal to 0.
        """
        super(PathLoss, self).__init__(PathLoss.__name__)
        check_argument_type(PathLoss.__name__, 'transmission_range', float,
                            transmission_range, self.logger)
        if transmission_range <= 0.0:
            raise ValueError('Parameter "transmission_range": a value of the' \
                             ' transmission range cannot be less or equal to' \
                             ' 0 but %f given!' % float(transmission_range))
        self.__transmission_range = float(transmission_range)

    def __distance(self, source_coordinates, destination_coordinates):
        """
        Calculates the distance between source and destination nodes in
        Cartesian space.

        *Parameters*:
            - **source_coordinates** (`list`): values of the source node's
              horizontal and vertical coordinates at the current simulation
              step;
            - **destination_coordinates** (`list`): values of the destination
              node's horizontal and vertical coordinates at the current
              simulation step.

        *Returns*:
            The distance between source and destination nodes in Cartesian
            space of type `float`.
        """
        return \
            sqrt(pow(source_coordinates[0] - destination_coordinates[0], 2) \
                 + pow(source_coordinates[1] - destination_coordinates[1], 2))

    def get_neighbors(self, coordinates):
        """
        Calculates identifiers of all nodes in a network that would be able to
        receive a wireless signal transmitted from a source node, according to
        the implemented propagation model.  All nodes in the network are
        considered, one by one, as the source node.

        *Parameters*:
           - **coordinates** (`list`): a list of coordinates of all nodes in
             the simulated network at the current simulation step.

        *Returns*:
            A `list` that in position ``i`` is a list of all nodes that would
            be able to receive a wireless signal transmitted by a node whose
            identifier is equal to ``i``.

        *Examples*:

        .. testsetup::

            from sim2net.propagation.path_loss import PathLoss

        .. doctest::

            >>> pathloss = PathLoss(1.0)
            >>> coordinates = [[1.0, 2.0], [1.5, 2.5], [2.0, 3.0], [2.5, 3.5]]
            >>> print pathloss.get_neighbors(coordinates)
            [[1], [0, 2], [1, 3], [2]]
            >>> coordinates = [[1.0, 2.0], [1.1, 2.1], [1.2, 2.2], [1.3, 2.3]]
            >>> print pathloss.get_neighbors(coordinates)
            [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
        """
        neighbors = list()
        for node in range(0, len(coordinates)):
            neighbors.append(list())
        for source_node in range(0, len(coordinates)):
            for destination_node in range(source_node + 1, len(coordinates)):
                if self.__distance(coordinates[source_node],
                                   coordinates[destination_node]) \
                   <= self.__transmission_range:
                    neighbors[source_node].append(destination_node)
                    neighbors[destination_node].append(source_node)
        if __debug__ and self.logger.isEnabledFor('DEBUG'):
            self.logger.debug('Neighboring nodes has been computed for %d' \
                              ' nodes' % len(coordinates))
        return neighbors
