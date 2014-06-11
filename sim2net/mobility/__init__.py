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
This package provides a collection of mobility model classes.

Mobility models ([LNR04]_, [CBD02]_) are designed to describe the movement
pattern of mobile nodes, and how their location, velocity and acceleration
change over time.  Since mobility patterns may play a significant role in
determining the protocol performance, it is desirable for mobility models to
emulate the movement pattern of targeted real life applications in a reasonable
way.

The literature categorises mobility models as being either *entity* or *group
models*.  Entity models are used as a tool to model the behaviour of individual
mobile nodes, treated as autonomous, independent entities.  On the other hand,
the key assumption behind the group models is that individual nodes influence
each other's movement to some degree.  Therefore, group models have become
helpful in simulating the motion patterns of a group as a whole.


.. [LNR04]  Guolong Lin, Guevara Noubir, Rajmohan Rajamaran.  Mobility Models
   for Ad-Hoc Network Simulation.  In Proceedings of the *23rd Conference of
   the IEEE Communications Society* (INFOCOM 2004), pp. 463-473.  Hong Kong,
   March 2004.
.. [CBD02]  Tracy Camp, Jeff Boleng, Vanessa Davies.  A Survey of Mobility
   Models for Ad-Hoc Network Research.  In *Wireless Communications Mobile
   Computing.  Special Issue on Mobile Ad Hoc Networking: Research, Trends and
   Applications*, vol. 2(5), 483--502.  John Wiley & Sons, 2002.
"""


__docformat__ = 'reStructuredText'

__all__ = ['gauss_markov', 'nomadic_community', 'random_direction',
           'random_waypoint']
