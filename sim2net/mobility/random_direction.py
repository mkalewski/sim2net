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
This module provides an implementation of the Random Direction mobility model.

At the beginning of the simulation, with the use of the Random Direction
mobility model ([RMM01]_), a node first stops for some random *pause time*, and
then randomly selects a *direction* in which to move.  The direction is
measured in degrees, and at first, the node selects a degree between 0 and 359.
Next, it finds a destination point on the boundary of the simulation area in
this direction of travel and moves with a constant, but randomly selected
(between the *minimum* and *maximum* values), speed to its destination.  Once
it reaches the destination, it pauses, and then selects a new direction between
0 and 180 degree (the degree is limited because the node is already on the
boundary of the simulation area).  The node then identifies the destination on
the boundary in this line of direction, selects a new speed, and resumes
travel.  The whole process is repeated again and again until simulation ends.
The speed and destination of each node are chosen independently of other nodes.


.. [RMM01]  Elizabeth M. Royer, P. Michael Melliar-Smithy, Louise E. Moser.  An
   Analysis of the Optimum Node Density for Ad Hoc Mobile Networks.  In
   Proceedings of the *IEEE International Conference on Communications* (ICC
   2001), pp. 857--861, vol. 3.  Helsinki, Finland, June 2001.
"""


from sim2net.mobility._mobility import Mobility
from sim2net.mobility.random_waypoint import RandomWaypoint
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class RandomDirection(RandomWaypoint, Mobility):
    """
    This class implements the Random Direction mobility model, in which each
    node moves along straight lines from one destination point, on the boundary
    of the simulation area, to another.

    The nodes may also have *pause times* when they reach their destination
    points, and their speeds are selected at random between the *minimum* and
    *maximum speed* values.  (All random picks are uniformly distributed).

    .. note::

        The :meth:`get_current_position` method computes a position of a node
        at the current *simulation step* (see: :mod:`sim2net._time`), so it is
        presumed that the method is called at each step of the simulation.

    .. seealso::  :mod:`sim2net.mobility.random_waypoint`
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
        Mobility.__init__(self, RandomDirection.__name__)
        self._area = area
        self._time = time
        self._destinations = dict()
        check_argument_type(RandomDirection.__name__, 'initial_coordinates',
                            list, initial_coordinates, self.logger)
        check_argument_type(RandomDirection.__name__, 'pause_time', float,
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
        Randomizes a new destination point on the boundary of the simulation
        area and returns its coordinates as a `tuple`.
        """
        destinations = (self.random_generator.uniform(self._area.ORIGIN[0],
                                                      self._area.width),
                        self.random_generator.uniform(self._area.ORIGIN[1],
                                                      self._area.height))
        direction = self.random_generator.uniform(0.0, 4.0)
        if direction > 3.0:
            return (0.0, destinations[1])
        elif direction > 2.0:
            return (destinations[0], self._area.height)
        elif direction > 1.0:
            return (self._area.width, destinations[1])
        else: return (destinations[0], 0.0)
