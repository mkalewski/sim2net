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
This package provides a collection of wireless signal propagation model
classes.

A wireless transmission may be distorted by many effects such as free-space
loss, refraction, diffraction, reflection or absorption.  Therefore, wireless
propagation models describe the influence of environment on signal quality
(mainly as a function of frequency, distance or other conditions) and calculate
the **signal-to-noise ratio** (*SNR*) at the receiver.  Then, it is assumed
that if the SNR value is higher than some prescribed threshold, the signal can
be received, and the packet that is carried by the signal can be successfully
received if the receiving node remains connected in this way with the sending
node at least for the duration of that packet transmission.
"""


__docformat__ = 'reStructuredText'

__all__ = ['path_loss']
