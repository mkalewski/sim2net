import os
from setuptools import setup

setup(
    name='sim2net',
    version='3.1.2',
    author='Michal Kalewski  <mkalewski at cs.put.poznan.pl>',
    description='Simple Network Simulator (sim2net) is a discrete event '\
                'simulator of mobile ad hoc networks (MANETs).',
    long_description=open("README.rst").read(),
    url='https://github.com/mkalewski/sim2net',
    license='MIT License',
    packages=[
        'sim2net',
        'sim2net.area',
        'sim2net.cli',
        'sim2net.failure',
        'sim2net.mobility',
        'sim2net.packet_loss',
        'sim2net.placement',
        'sim2net.propagation',
        'sim2net.speed',
        'sim2net.utility'
    ],
    entry_points = {'console_scripts': ['sim2net=sim2net.cli.cli:main'],}
)
