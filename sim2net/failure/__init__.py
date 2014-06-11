#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012-2013 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
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
This package provides a collection of process failure models.

A *process failure* occurs whenever the process does not behave according to
its algorithm, and here the term *process* means the *application* running on
one of the nodes in the simulated network.  To simulate such behaviors, process
failure models are used, and they differ in the nature and scope of faults.
Possible process failures may include ([CGR11]_): **crashes** (where a process
at some time may simply stop to execute any steps and never recovers);
**omissions** (where a process does not send or receive messages that it is
supposed to send or receive according to its algorithm); **crashes with
recoveries** (where a process *crashes* and never recovers or it keeps
infinitely often crashing and recovering); **eavesdropping** (where a process
leaks information obtained in its algorithm to an outside entity); and
**arbitrary** (where a process may deviate in any conceivable way from its
algorithm).


.. [CGR11]  Christian Cachin, Rachid Guerraoui, Luís Rodrigues.  Introduction
   to Reliable and Secure Distributed Programming, 2ed Edition.
   Springer-Verlag, 2011.
"""


__docformat__ = 'reStructuredText'

__all__ = ['crash']
