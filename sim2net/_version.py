#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012-2014 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
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
This package provides version information for the project.

The project's version number has the following form: `X.Y.Z`, where:

* `X` -- is a major version number,
* `Y` -- is a minor version number,
* `Z` -- is a maintenance version number.

Each number is increased by one at a time.  When one of the numbers is
increased, the less significant numbers are reset to zero in the following
way:

* if there are backwards incompatible changes then the major number is
  incremented and the minor and maintenance numbers are reset to zero;
* if there are new features (additions) implemented then the minor number
  is incremented and the maintenance number is reset to zero;
* if there are only implementation detail changes or bug fixes then the
  maintenance number is incremented (and there are no resets).
"""


__docformat__ = 'reStructuredText'

#: The project name.
__PROJECT_NAME = 'Simple Network Simulator'

#: The short project name.
__PROJECT_SHORT_NAME = 'sim2net'

#: The version number.
__VERSION_NUMBER = '3.1.2'  # apply also to the README.rst and setup.py files


def get_version():
    """
    Returns the current version number as a string.
    """
    return __VERSION_NUMBER

def project_information():
    """
    Returns the project information in the form of its name, short name, and
    the current version number as a string.
    """
    return ('%s (%s) version %s'
            % (__PROJECT_NAME, __PROJECT_SHORT_NAME, __VERSION_NUMBER))
