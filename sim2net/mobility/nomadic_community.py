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
This module provides an implementation of the Nomadic Community mobility model.

The Nomadic Community ([CBD02]_) is a group mobility model, in which a group of
nodes collectively moves from one destination to another.  Destinations for the
group are determined by the so-called *reference point* that is selected at
random within the simulation area.  Moreover, each node uses an entity mobility
model to roam, within a fixed range, around the current reference point.  But
when the reference point changes, all nodes travel to the new area defined by
new coordinates of the reference point (and its range of free roam) and then
begin roaming around it.  The whole process is repeated again and again until
simulation ends.
"""


from math import fabs

from sim2net.mobility._mobility import Mobility
from sim2net.mobility.random_waypoint import RandomWaypoint
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class NomadicCommunity(RandomWaypoint, Mobility):
    """
    This class implements the Nomadic Community mobility model, in which a
    group of nodes travels together from one location to another.

    In this implementation, coordinates of the reference point are uniformly
    selected at random within the simulation area once every :math:`x+y\\times
    pause\\_time` *simulation time* units (see: :mod:`sim2net._time` module),
    where :math:`x` is uniformly picked at random from the range :math:`[100,
    200]`, and :math:`y` from the range :math:`[1, 10]`.  Nodes roam around
    reference points in accordance with the **Random Waypoint** mobility model
    (see: :mod:`sim2net.mobility.random_waypoint` module).  The width and
    height of the (square or rectangular) free roam area around the reference
    point are computed as a product of the *area_factor* parameter and the
    width and height (respectively) of the simulation area.

    .. note::

        The :meth:`get_current_position` method computes a position of a node
        at the current *simulation step* (see: :mod:`sim2net._time`), so it is
        presumed that the method is called at each step of the simulation.
    """

    #: The minimum value of the range used to determine the reference point
    #: change time.
    __DEFAULT_MINIMUM_RELOCATION_TIME = 100.0

    #: The maximum value of the range used to determine the reference point
    #: change time.
    __DEFAULT_MAXIMUM_RELOCATION_TIME = 200.0

    #: The minimum value of the range for the pause time used to determine the
    #: reference point change time.
    __DEFAULT_MINIMUM_RELOCATION_PAUSE_TIME = 1.00

    #: The maximum value of the range for the pause time used to determine the
    #: reference point change time.
    __DEFAULT_MAXIMUM_RELOCATION_PAUSE_TIME = 10.0


    def __init__(self, area, time, initial_coordinates, pause_time=0.0,
                 area_factor=0.25):
        """
        *Parameters*:
            - **area**: an object representing the simulation area;
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class;
            - **initial_coordinates** (`list`): initial coordinates of all
              nodes; each element of this parameter should be a tuple of two
              coordinates: horizontal and vertical (respectively) of type
              `float`;
            - **pause_time** (`float`): a maximum value of the pause time in
              the *simulation time* units (default: `0.0`, see also:
              :mod:`sim2net._time`);
            - **area_factor** (`float`): a factor used to determine the width
              and height of the free roam area around the reference point
              (default: `0.25`).

        *Raises*:
            - **ValueError**: raised when the given value of the *area*, *time*
              or *initial_coordinates* parameter is `None`; or when the given
              value of the *pause_time* parameter is less that zero; or when
              the given value of the *area_factor* parameter is less than zero
              or greater than one.

        (At the beginning, nodes' destination points are set to be equal to its
        initial coordinates passed by the *initial_coordinates* parameter.)
        """
        if area is None:
            raise ValueError('Parameter "area": a simulation area object' \
                             ' expected but "None" value given!')
        if time is None:
            raise ValueError('Parameter "time": a time abstraction object' \
                             ' expected but "None" value given!')
        if initial_coordinates is None:
            raise ValueError('Parameter "initial_coordinates": identifiers' \
                             ' of nodes expected but "None" value given!')
        Mobility.__init__(self, NomadicCommunity.__name__)
        check_argument_type(RandomWaypoint.__name__, 'initial_coordinates',
                            list, initial_coordinates, self.logger)
        check_argument_type(RandomWaypoint.__name__, 'pause_time', float,
                            pause_time, self.logger)
        if pause_time < 0.0:
            raise ValueError('Parameter "pause_time": a value of the pause' \
                             ' time cannot be less that zero but %f given!' \
                             % float(pause_time))
        self._pause_time = float(pause_time)
        check_argument_type(RandomWaypoint.__name__, 'area_factor', float,
                            area_factor, self.logger)
        if area_factor < 0.0 or area_factor > 1.0:
            raise ValueError('Parameter "area_factor": a value of the factor' \
                             ' used to compute the free roam area of nodes' \
                             ' cannot be less than zero or greater than one' \
                             ' but %f given!' % float(area_factor))
        self.__area_factor = float(area_factor)
        self._area = area
        self._time = time
        self.__reference_point = \
            (self.random_generator.uniform(self._area.ORIGIN[0],
                                           self._area.width),
             self.random_generator.uniform(self._area.ORIGIN[1],
                                           self._area.height))
        self.__relocation_time = None
        # { node id:
        #     { 'destination':  (horizontal coordinate, vertical coordinate),
        #       'pause time' :  time } }
        #       'on site'    :  True/False } }
        self._destinations = dict()
        for node_id in range(0, len(initial_coordinates)):
            self._destinations[node_id] = dict()
            self._destinations[node_id]['destination'] = \
                initial_coordinates[node_id]
            self._destinations[node_id]['pause time'] = None
            self._destinations[node_id]['on site'] = False
        self.logger.debug('Destination points has been initialized for %d' \
                          ' nodes with the initial reference point at (%f,' \
                          ' %f)' % (len(self._destinations),
                                    self.__reference_point[0],
                                    self.__reference_point[1]))

    def __get_free_roam_area_edges(self, reference_point):
        """
        Computes boundaries of a free roam area around a given reference point.

        *Parameter*:
            - **reference_point** (`tuple`) containing horizontal and vertical
              coordinates (respectively) of the reference point.

        *Returns*:
            A `tuple` containing values of the top, right, bottom and left
            boundaries (respectively) in the simulation area.
        """
        offset = 0.5 * self._area.width * self.__area_factor
        left_edge = reference_point[0] - offset
        if left_edge < 0.0:
            left_edge = 0.0
        right_edge = reference_point[0] + offset
        if right_edge > self._area.width:
            right_edge = self._area.width
        offset = 0.5 * self._area.height * self.__area_factor
        bottom_edge = reference_point[1] - offset
        if bottom_edge < 0.0:
            bottom_edge = 0.0
        top_edge = reference_point[1] + offset
        if top_edge > self._area.height:
            top_edge = self._area.height
        return (top_edge, right_edge, bottom_edge, left_edge)

    def __get_new_reference_point(self):
        """
        Uniformly randomizes new coordinates of the reference point.  The
        vertical and horizontal coordinates are returned (respectively) as a
        `tuple`.
        """
        edges = self.__get_free_roam_area_edges(self.__reference_point)
        while True:
            reference_point = \
                (self.random_generator.uniform(self._area.ORIGIN[0],
                                               self._area.width),
                 self.random_generator.uniform(self._area.ORIGIN[1],
                                               self._area.height))
            new_edges = self.__get_free_roam_area_edges(reference_point)
            if new_edges[2] > edges[0] or new_edges[3] > edges[1] \
               or new_edges[0] < edges[2] or new_edges[1] < edges[3]:
                break
        self.logger.debug('New coordinates of the reference point has been' \
                          ' selected: (%f, %f)' % (reference_point[0],
                                                   reference_point[1]))
        return reference_point

    def __get_new_relocation_time(self):
        """
        Randomizes and returns a new relocation time of type `float`, after
        which coordinates of the reference point will be changed.
        """
        relocation_time = \
            self.random_generator.uniform(
                NomadicCommunity.__DEFAULT_MINIMUM_RELOCATION_TIME,
                NomadicCommunity.__DEFAULT_MAXIMUM_RELOCATION_TIME) \
            + (self.random_generator.uniform(
                   NomadicCommunity.__DEFAULT_MINIMUM_RELOCATION_PAUSE_TIME,
                   NomadicCommunity.__DEFAULT_MAXIMUM_RELOCATION_PAUSE_TIME) \
               * self._pause_time)
        self.logger.debug('New reference point relocation time has been' \
                          ' selected: %f simulation time units'
                          % relocation_time)
        return relocation_time

    def __reference_point_relocation(self):
        """
        Relocates the reference point by picking its new coordinates.  The
        relocation takes place only if all nodes are within the current area of
        free roam and the relocation time has expired.  Otherwise, the current
        coordinates of the reference point are preserved.
        """
        if self.__relocation_time is None:
            for node_id in self._destinations:
                if not self._destinations[node_id]['on site']:
                    return
            self.__relocation_time = \
                self._time.simulation_time + self.__get_new_relocation_time()
        else:
            if self.__relocation_time <= self._time.simulation_time:
                self.__relocation_time = None
                for node_id in self._destinations:
                    self._destinations[node_id]['on site'] = False
                self.__reference_point = self.__get_new_reference_point()

    def _get_new_destination(self):
        """
        Uniformly randomizes a new waypoint within the range of free roam and
        returns its coordinates as a `tuple`.
        """
        edges = self.__get_free_roam_area_edges(self.__reference_point)
        return (self.random_generator.uniform(edges[3], edges[1]),
                self.random_generator.uniform(edges[2], edges[0]))

    def get_current_position(self, node_id, node_speed, node_coordinates):
        """
        Calculates and returns a node's position at the current simulation step
        in accordance with the Nomadic Community mobility model (and Random
        Waypoint model within the area of free roam).

        A distance of the route traveled by the node, between the current and
        previous simulation steps, is calculated as the product of the current
        node's speed and the *simulation period* (see: :mod:`sim2net._time`
        module).  Therefore, it is assumed that this method is called at every
        simulation step.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_speed**: an object representing the node's speed;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.

        *Returns*:
            A tuple containing current values of the node's horizontal and
            vertical coordinates.
        """
        # reference point relocation?
        self.__reference_point_relocation()
        # pause time?
        if self._destinations[node_id]['pause time'] is not None:
            if self._pause(node_id, node_coordinates) is None:
                self._assign_new_destination(node_id, node_speed)
            return node_coordinates
        # movement
        coordinates = self._step_move(node_id, node_speed, node_coordinates)
        assert 0 <= coordinates[0] <= self._area.width \
               and 0 <= coordinates[1] <= self._area.height, \
               'The new coordinates (%f, %f) exceed dimensions of the' \
               ' simulation area!' % coordinates
        if (coordinates[0] == self._destinations[node_id]['destination'][0]
            and
            coordinates[1] == self._destinations[node_id]['destination'][1]):
            if not self._destinations[node_id]['on site']:
                edges = self.__get_free_roam_area_edges(self.__reference_point)
                if coordinates[0] >= edges[3] \
                   and coordinates[0] <= edges[1] \
                   and coordinates[1] >= edges[2] \
                   and coordinates[1] <= edges[0]:
                    self._destinations[node_id]['on site'] = True
            if self._assign_new_pause_time(node_id) is not None:
                self._destinations[node_id]['destination'] = [None, None]
            else:
                self._assign_new_destination(node_id, node_speed)
        elif __debug__ and self.logger.isEnabledFor('DEBUG'):
            msg = 'The current position of the node #%d is (%f, %f) with the' \
                  ' current speed equal to %f'
            self.logger.debug(msg % (node_id, coordinates[0], coordinates[1],
                                     fabs(node_speed.current)))
        print "%.30f    %.30f    %.30f    %.30f" % (coordinates[0], coordinates[1], self.__reference_point[0], self.__reference_point[1])
        return coordinates
