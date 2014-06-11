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
This module provides an interface to the simulator for the :mod:`sim2net.cli`
command-line tool and its main entry point for conducting simulations.
"""


import inspect
import os
import sys

from sim2net._network import Network
from sim2net._version import project_information
from sim2net._time import Time
from sim2net.application import Application
from sim2net.utility import logger


__docformat__ = 'reStructuredText'


class Sim2Net(object):
    """
    This class is the main entry point for conducting simulations.

    Based on the given simulation configuration and application file, the class
    initializes and runs the simulation.
    """

    #:
    __CONFIGURATION_VALUES = [
        'simulation_frequency',
        'total_simulation_steps',
        'nodes_number',
        'transmission_range',
        'maximum_transmission_time']

    #:
    __CONFIGURATION_LISTS = [
        'packet_loss',
        'speed']

    #:
    __CONFIGURATION_OBJECTS = [
        'mobility',
        'propagation',
        'failure']

    def __init__(self, configuration, application_file):
        """
        """
        if configuration is None:
            raise ValueError('Parameter "configuration": a simulation'
                             ' configuration object expected but "None" value'
                             ' given!')
        if application_file is None:
            raise ValueError('Parameter "application": a name of an'
                             ' application file expected but "None" value'
                             ' given!')
        environment = dict()
        environment['time'] = Time()
        if 'logger_level' in configuration:
            self.__logger = \
                logger.create_logger(environment['time'],
                                     configuration['logger_level'])
        else:
            self.__logger = logger.create_logger(environment['time'])
        self.__logger.info(project_information())
        self.__logger.info('Initializing the simulation environment')
        for name in Sim2Net.__CONFIGURATION_VALUES:
            environment[name] = self.__get_value(name, configuration)
        environment['time'].setup(environment['simulation_frequency'])
        environment['area'] = \
            self.__get_element('area', configuration, environment)
        environment['initial_coordinates'] = \
            self.__get_element('placement', configuration,
                               environment).get_placement()
        for name in Sim2Net.__CONFIGURATION_LISTS:
            environment[name] = \
                self.__get_element(name, configuration, environment,
                                   environment['nodes_number'])
        for name in Sim2Net.__CONFIGURATION_OBJECTS:
            environment[name] = self.__get_element(name, configuration,
                                                   environment)
        environment['application'] = \
            self.__get_application_class(application_file)
        self.__total_simulation_steps = environment['total_simulation_steps']
        self.__network = Network(environment)

    def __report_error(self, element, name):
        """
        """
        message = 'Configuration %s %s is missing!' % (element, name)
        self.__logger.critical(message)
        raise Exception('%s  Please, check your configuration file.'
                        % message)

    def __get_value(self, name, configuration):
        """
        """
        try:
            return configuration[name]
        except KeyError, err:
            self.__report_error('element', err)

    def __get_arguments(self, name, configuration):
        """
        """
        try:
            if len(configuration[name]) > 1:
                return configuration[name][1]
            else:
                return dict()
        except KeyError, err:
            self.__report_error('element', err)

    def __get_element(self, name, configuration, environment, number=None):
        """
        """
        if number is None:
            number = 1
        arguments = self.__get_arguments(name, configuration)
        parameters = \
            (inspect.getargspec(configuration[name][0].__init__)[0])[1:]
        marguments = [marg for marg in parameters if marg not in arguments]
        try:
            for marg in marguments:
                arguments[marg] = environment[marg]
        except KeyError, err:
            self.__report_error('argument', '%s for element "%s"'
                                % (err, name))
        if number == 1:
            return configuration[name][0](**arguments)
        else:
            elements = list()
            for nelement in range(0, number):
                elements.append(configuration[name][0](**arguments))
            return elements

    def __get_application_class(self, application_file):
        """
        """
        directory, module_name = os.path.split(application_file)
        module_name = os.path.splitext(module_name)[0]
        path = list(sys.path)
        sys.path.insert(0, directory)
        module = __import__(module_name)
        sys.path[:] = path
        members = inspect.getmembers(module, inspect.isclass)
        for member in members:
            nested_members = inspect.getmro(member[1])
            if len(nested_members) > 1:
                if nested_members[1].__name__ == Application.__name__:
                    self.__logger.debug('Application class "%s" has been'
                                        ' loaded' % nested_members[0].__name__)
                    return nested_members[0]
        message = 'Cannot find any appropriate application class in file' \
                  ' "%s"!' % application_file
        self.__logger.critical(message)
        raise Exception('%s  Please, check your implementation.' % message)

    def run(self):
        """
        """
        self.__logger.info('Starting the simulation')
        for step in range(0, self.__total_simulation_steps):
            self.__network.step()
        self.__network.finalize()
        self.__logger.info('The simulation is finished')
