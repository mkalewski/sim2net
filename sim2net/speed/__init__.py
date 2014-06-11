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
This package provides a collection of speed distribution classes.

Speed is a scalar quantity that describes the rate of change of a node position
in a simulation area (see: :mod:`sim2net.area`).

.. note::

    In all speed distribution classes the quantity of speed should be
    considered as simulation area units per one *simulation time* unit (see:
    :mod:`sim2net._time`).

    For example, the value of speed equal to :math:`5` would mean *five units
    of simulation area per one unit of simulation time*.
"""


__docformat__ = 'reStructuredText'

__all__ = ['constant', 'normal', 'uniform']
