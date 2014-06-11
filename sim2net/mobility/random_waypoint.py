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
This module provides an implementation of the Random Waypoint mobility model.

In this model ([JM96]_, [BMJ+98]_), a node first stops for some random *pause
time*.  Then, the node randomly picks a point within the simulation area and
starts moving toward it with a constant, but randomly selected, speed that is
uniformly distributed between the *minimum* and *maximum speed* values.  Upon
reaching the destination point (or waypoint), the node pauses again and then
moves toward a newly randomized point.  (If the *pause time* is equal to zero,
this leads to continuous mobility.)  The whole process is repeated again and
again until simulation ends.  The speed and destination of each node are chosen
independently of other nodes.


.. [JM96]  David B. Johnson and David A. Maltz.  Dynamic Source Routing in Ad
   Hoc Wireless Networks.  In *Mobile Computing*, edited by Tomasz Imielinski
   and Hank Korth, chapter 5, pp. 153--181.  Kluwer Academic Publishers, 1996.
.. [BMJ+98]  Josh Broch, David A. Maltz, David B. Johnson, Yih-Chun Hu, Jorjeta
   Jetcheva.  A Performance Comparison of Multi-hop Wireless Ad Hoc Network
   Routing Protocols.  In Proceedings of the *4th Annual ACM/IEEE International
   Conference on Mobile Computing and Networking* (MobiCom 1998), pp. 85--97.
   Dallas, Texas, United States, October 1998.
"""


from math import fabs, sqrt

from sim2net.mobility._mobility import Mobility
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class RandomWaypoint(Mobility):
    """
    This class implements the Random Waypoint mobility model, in which each
    node moves along straight lines from one waypoint to another.

    The waypoints are randomly picked within the simulation area.  The nodes
    may also have *pause times* when they reach waypoints, and their speeds are
    selected at random between the *minimum* and *maximum speed* values.  (All
    random picks are uniformly distributed).

    .. note::

        The :meth:`get_current_position` method computes a position of a node
        at the current *simulation step* (see: :mod:`sim2net._time`), so it is
        presumed that the method is called at each step of the simulation.
    """

    def __init__(self, area, time, initial_coordinates, pause_time=0.0):
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
              :mod:`sim2net._time`).

        *Raises*:
            - **ValueError**: raised when the given value of the *area*, *time*
              or *initial_coordinates* parameter is `None` or when the given
              value of the *pause_time* parameter is less that zero.

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
        super(RandomWaypoint, self).__init__(RandomWaypoint.__name__)
        self._area = area
        self._time = time
        self._destinations = dict()
        check_argument_type(RandomWaypoint.__name__, 'initial_coordinates',
                            list, initial_coordinates, self.logger)
        check_argument_type(RandomWaypoint.__name__, 'pause_time', float,
                            pause_time, self.logger)
        if pause_time < 0.0:
            raise ValueError('Parameter "pause_time": a value of the pause' \
                             ' time cannot be less that zero but %f given!' \
                             % float(pause_time))
        self._pause_time = float(pause_time)
        # { node id:
        #     { 'destination':  (horizontal coordinate, vertical coordinate),
        #       'pause time' :  time } }
        for node_id in range(0, len(initial_coordinates)):
            self._destinations[node_id] = dict()
            self._destinations[node_id]['destination'] = \
                initial_coordinates[node_id]
            self._destinations[node_id]['pause time'] = None
        self.logger.debug('Destination points has been initialized for %d' \
                          ' nodes' % len(self._destinations))

    def _get_new_destination(self):
        """
        Randomizes a new waypoint and returns its coordinates as a `tuple`.
        """
        return (self.random_generator.uniform(self._area.ORIGIN[0],
                                              self._area.width),
                self.random_generator.uniform(self._area.ORIGIN[1],
                                              self._area.height))

    def _get_new_pause_time(self):
        """
        Randomizes a new pause time and returns its value of type `float`.
        """
        return self.random_generator.uniform(0.0, self._pause_time)

    def _assign_new_destination(self, node_id, node_speed):
        """
        Assigns a new destination point for a node of a given ID and picks its
        new speed value.  (See also: :meth:`_get_new_destination`)

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_speed**: an object representing the node's speed.
        """
        self._destinations[node_id]['destination'] = \
            self._get_new_destination()
        node_speed.get_new()
        if self.logger.isEnabledFor('DEBUG'):
            msg = 'A new destination has been selected for the node #%d:' \
                  ' (%f, %f) with the current speed equal to %f'
            self.logger.debug(
                msg % (node_id, self._destinations[node_id]['destination'][0],
                       self._destinations[node_id]['destination'][1],
                       fabs(node_speed.current)))

    def _assign_new_pause_time(self, node_id):
        """
        Assigns a new pause time for a node of a given ID and returns the
        value.  If the maximum pause time is set to `0`, `None` value is
        assigned and returned.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node.

        *Returns*:
            (`float`) a newly randomized pause time.
        """
        if self._pause_time > 0:
            pause_time = self._get_new_pause_time()
            self._destinations[node_id]['pause time'] = pause_time
        else:
            pause_time = 0.0
            self._destinations[node_id]['pause time'] = None
        if self.logger.isEnabledFor('DEBUG'):
            msg = 'The node #%d is now in its destination position (%f, %f)' \
                  ' with the pause time equal to %f'
            self.logger.debug(msg %
                (node_id, self._destinations[node_id]['destination'][0],
                self._destinations[node_id]['destination'][1], pause_time))
        return self._destinations[node_id]['pause time']

    def _parallel_trajectory(self, coordinate, destination, step_distance):
        """
        Computes the current position of a node when one of its coordinates is
        equal to the corresponding destination coordinate.  In such a case, the
        node moves on a straight line that is parallel to the horizontal or
        vertical axis of the simulation area.  (See also:
        :meth:`_diagonal_trajectory`.)

        *Parameters*:
            - **coordinate** (`float`): a value of the previous node's
              coordinate that is not equal to its corresponding destination
              coordinate;
            - **destination** (`float`): a value of the destination coordinate;
            - **step_distance** (`float`): a distance that the node has moved
              between the previous and current simulation steps.

        *Returns*:
            (`float`) a current value of the node's coordinate.
        """
        if destination > coordinate \
           and destination >= coordinate + step_distance:
            return coordinate + step_distance
        if destination < coordinate \
           and destination < coordinate - step_distance:
            return coordinate - step_distance
        return destination

    def _diagonal_trajectory(self, node_id, node_coordinates, step_distance):
        """
        Computes the current position of a node if its trajectory is not
        parallel to the horizontal or vertical axis of the simulation area.
        (See also: :meth:`_parallel_trajectory`.)

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.
            - **step_distance** (`float`): a distance that the node has moved
              between the previous and current simulation step.

        *Returns*:
            (`tuple`) current values of the node's horizontal and vertical
            coordinates.
        """
        horizontal_destination = self._destinations[node_id]['destination'][0]
        vertical_destination = self._destinations[node_id]['destination'][1]
        horizontal_distance = \
            fabs(horizontal_destination - node_coordinates[0])
        vertical_distance = fabs(vertical_destination - node_coordinates[1])
        distance = \
            sqrt(pow(horizontal_distance, 2.0) + pow(vertical_distance, 2.0))
        if step_distance >= distance:
            return (horizontal_destination, vertical_destination)
        horizontal_coordinate = \
            (horizontal_distance * step_distance) / distance
        vertical_coordinate = \
            (vertical_distance * horizontal_coordinate) / horizontal_distance
        if node_coordinates[0] < horizontal_destination:
            horizontal_coordinate = node_coordinates[0] + horizontal_coordinate
        else:
            horizontal_coordinate = node_coordinates[0] - horizontal_coordinate
        if node_coordinates[1] < vertical_destination:
            vertical_coordinate = node_coordinates[1] + vertical_coordinate
        else:
            vertical_coordinate = node_coordinates[1] - vertical_coordinate
        return (horizontal_coordinate, vertical_coordinate)

    def _step_move(self, node_id, node_speed, node_coordinates):
        """
        Computes a node's position at the current simulation step. If its
        trajectory is parallel to the horizontal or vertical axis of the
        simulation area, the :meth:`_steady_trajectory` method is used,
        otherwise the :meth:`_diagonal_trajectory` method is used.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_speed**: an object representing the node's speed;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.

        *Returns*:
            (`tuple`) current values of the node's horizontal and vertical
            coordinates.
        """
        horizontal_destination = self._destinations[node_id]['destination'][0]
        vertical_destination = self._destinations[node_id]['destination'][1]
        if node_coordinates[0] == horizontal_destination \
           and node_coordinates[1] == vertical_destination:
            return (horizontal_destination, vertical_destination)
        step_distance = fabs(node_speed.current) * self._time.simulation_period
        if node_coordinates[0] == horizontal_destination:
            return \
                (horizontal_destination,
                 self._parallel_trajectory(
                     node_coordinates[1], vertical_destination, step_distance))
        if node_coordinates[1] == vertical_destination:
            return \
                (self._parallel_trajectory(
                     node_coordinates[0], horizontal_destination,
                     step_distance),
                 vertical_destination)
        return self._diagonal_trajectory(node_id, node_coordinates,
                                         step_distance)

    def _pause(self, node_id, node_coordinates):
        """
        Decreases the current value of a node's pause time and returns the
        result of type `float`, or `None` if the pause time has expired.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.
        """
        self._destinations[node_id]['pause time'] -= \
            self._time.simulation_period
        if self._destinations[node_id]['pause time'] <= 0:
            self._destinations[node_id]['pause time'] = None
        else:
            if __debug__ and self.logger.isEnabledFor('DEBUG'):
                msg = 'The node #%d is still in its destination position' \
                      ' (%f, %f) with the pause time equal to %f'
                self.logger.debug(msg %
                    (node_id, node_coordinates[0], node_coordinates[1],
                     self._destinations[node_id]['pause time']))
        return self._destinations[node_id]['pause time']

    def get_current_position(self, node_id, node_speed, node_coordinates):
        """
        Calculates and returns a node's position at the current simulation step
        in accordance with the Random Waypoint mobility model.

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
            # print "%.30f    %.30f" % (coordinates[0], coordinates[1])
            if self._assign_new_pause_time(node_id) is not None:
                self._destinations[node_id]['destination'] = [None, None]
            else:
                self._assign_new_destination(node_id, node_speed)
        elif __debug__ and self.logger.isEnabledFor('DEBUG'):
            msg = 'The current position of the node #%d is (%f, %f) with the' \
                  ' current speed equal to %f'
            self.logger.debug(msg % (node_id, coordinates[0], coordinates[1],
                                     fabs(node_speed.current)))
        # print "%.30f    %.30f" % (coordinates[0], coordinates[1])
        return coordinates
