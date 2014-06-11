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
Synopsis
--------
``sim2net`` -- a console script to initialize and start simulations::

    sim2net [-h | -d | -v | -i DIRECTORY] CONFIGURATION APPLICATION

    positional arguments:
      CONFIGURATION         simulation configuration file
      APPLICATION           simulation application file

    optional arguments:
      -h, --help            show this help message and exit
      -d, --description     show description message and exit
      -i DIRECTORY, --initialize DIRECTORY
                            write configuration and application files to given
                            directory
      -v, --version         show version message and exit

Description
-----------
To start a simulation with the **sim2net** simulator, two files are necessary:
a configuration file (with the simulator settings) and an application file that
is run by every node in the simulated network (the application must implement
the :mod:`sim2net.application.Application` abstract class).  The easiest way to
obtain both files is to execute the ``sim2net`` command with the ``-i`` option,
eg.::

    sim2net -i .

After that, two files are created in the given directory: ``configuration.py``
and ``application.py``.  Both files may be edited -- for more information about
configuration parameters see :ref:`sim2net-code-documentation-packages`
section, and for more information about application implementation see the
:mod:`sim2net.application.Application` abstract class.

Next, to start the simulation, the ``sim2net`` command should be executed with
both files as arguments, eg.::

    sim2net ./configuration.py ./application.py

.. seealso:: :ref:`sim2net-code-documentation-packages`,
             :mod:`sim2net.application.Application`
"""


import argparse

from os.path import join, realpath, split
from shutil import copy
from sys import argv, exit, stdout
from traceback import print_exc

from sim2net._version import get_version, project_information
from sim2net.simulator import Sim2Net


__docformat__ = 'reStructuredText'

#: The POSIX exit status to signal failure.
__POSIX_EXIT_FAILURE = 1

#: The POSIX exit status to signal success.
__POSIX_EXIT_SUCCESS = 0

#: The description string.
__DESCRIPTION = """%s

Copyright (c) 2012-2014  Michal Kalewski  <mkalewski at cs.put.poznan.pl>

This program comes with ABSOLUTELY NO WARRANTY.
THIS IS FREE SOFTWARE, AND YOU ARE WELCOME TO REDISTRIBUTE IT UNDER THE TERMS
AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF THE
LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY FROM
HTTP://WWW.OPENSOURCE.ORG.
""" % project_information()


def main():
    """
    The entry point for the ``sim2net`` console command.
    """
    parser = argparse.ArgumentParser(
        prog='sim2net',
        usage=\
            'sim2net [-h | -d | -v | -i DIRECTORY] CONFIGURATION APPLICATION',
        description='%s' % project_information())
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--description',
        action='store_true',
        help='show description message and exit')
    group.add_argument(
        '-i', '--initialize',
        metavar='DIRECTORY',
        nargs=1,
        type=str,
        help='write configuration and application files to given directory')
    group.add_argument(
        '-v', '--version',
        action='store_true',
        help='show version message and exit')
    parser.add_argument(
        'configuration',
        metavar='CONFIGURATION',
        nargs='?',
        type=str,
        default=None,
        help='simulation configuration file')
    parser.add_argument(
        'application',
        metavar='APPLICATION',
        nargs='?',
        type=str,
        default=None,
        help='simulation application file')
    if len(argv) == 1:
        parser.print_help()
        exit(__POSIX_EXIT_FAILURE)
    args = parser.parse_args()
    if args.description:
        print __DESCRIPTION
        exit(__POSIX_EXIT_SUCCESS)
    if args.initialize:
        try:
            base_path = split(realpath(__file__))[0]
            copy(join(base_path, '_configuration_template.py'),
                 join(vars(args)['initialize'][0], 'configuration.py'))
            copy(join(base_path, '_application_template.py'),
                 join(vars(args)['initialize'][0], 'application.py'))
            exit(__POSIX_EXIT_SUCCESS)
        except Exception, err:
            print '***  [sim2net] CRITICAL - cannot write the files:\n'
            if __debug__:
                print_exc(file=stdout)
            else:
                print err
            exit(__POSIX_EXIT_FAILURE)
    if args.version:
        print get_version()
        exit(__POSIX_EXIT_SUCCESS)
    if vars(args)['configuration'] is None \
            or vars(args)['application'] is None:
        parser.print_usage()
        print 'sim2net: error: expected two arguments'
        exit(__POSIX_EXIT_FAILURE)
    try:
        configuration = dict()
        execfile(vars(args)['configuration'], configuration)
        sim2net = Sim2Net(configuration, vars(args)['application'])
        args = None
        configuration = None
    except Exception, err:
        print '***  [sim2net] CRITICAL - cannot initialize the simulator:\n'
        if __debug__:
            print_exc(file=stdout)
        else:
            print err
        exit(__POSIX_EXIT_FAILURE)
    try:
        sim2net.run()
    except Exception, err:
        print '***  [sim2net] CRITICAL - cannot continue:\n'
        if __debug__:
            print_exc(file=stdout)
        else:
            print err
        exit(__POSIX_EXIT_FAILURE)
    exit(__POSIX_EXIT_SUCCESS)

if __name__ == "__main__":
    main()
