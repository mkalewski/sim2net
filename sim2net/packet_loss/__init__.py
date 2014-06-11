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
This package provides a collection of packet loss model classes.

Packet loss occurs when a packet of data (or message) traveling across a
computer network fails to reach its destination(s).  In wireless communication,
the loss may be caused by wireless channel properties (e.g. signal degradation
due to multi-path *fading* or *shadowing*), packet collisions or faulty
networking hardware.  Thus, the purpose of packet loss models is to simulate
(potential) transmission failures in wireless communication.
"""


__docformat__ = 'reStructuredText'

__all__ = ['gilbert_elliott']
