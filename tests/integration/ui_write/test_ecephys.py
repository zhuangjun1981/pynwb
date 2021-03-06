import unittest2 as unittest
import numpy as np
import json
from datetime import datetime
import os

from form.build import GroupBuilder, DatasetBuilder, LinkBuilder

from pynwb.ecephys import *

from . import base

class TestElectrodeGroupIO(base.TestMapRoundTrip):

    def setUpContainer(self):
        self.dev1 = Device('dev1', 'a test source')
        channel_description = ['ch1', 'ch2']
        channel_location = ['lo1', 'lo2']
        channel_filtering = ['fi1', 'fi2']
        channel_coordinates = ['co1', 'co2']
        channel_impedance = ['im1', 'im2']
        return ElectrodeGroup('elec1', 'a test source',
                                        channel_description,
                                        channel_location,
                                        channel_filtering,
                                        channel_coordinates,
                                        channel_impedance,
                                        'desc1',
                                        'loc1',
                                        self.dev1)

    def setUpBuilder(self):
        device_builder = GroupBuilder('dev1',
                            attributes={'neurodata_type': 'Device',
                                        'namespace': 'core',
                                        'help': 'A recording device e.g. amplifier',
                                        'source': 'a test source'},
                         )
        return GroupBuilder('elec1',
                            attributes={'neurodata_type': 'ElectrodeGroup',
                                        'namespace': 'core',
                                        'help': 'A physical grouping of channels',
                                        'source': 'a test source'},
                            datasets={
                                'channel_description': DatasetBuilder('channel_description', ['ch1', 'ch2']),
                                'channel_location': DatasetBuilder('channel_location', ['lo1', 'lo2']),
                                'channel_filtering': DatasetBuilder('channel_filtering', ['fi1', 'fi2']),
                                'channel_coordinates': DatasetBuilder('channel_coordinates', ['co1', 'co2']),
                                'channel_impedance': DatasetBuilder('channel_impedance', ['im1', 'im2']),
                                'description': DatasetBuilder('description', 'desc1'),
                                'location': DatasetBuilder('location', 'loc1')
                            },
                            links={
                                'device': LinkBuilder('device', device_builder)
                            }
                        )

    def addContainer(self, nwbfile):
        ''' Should take an NWBFile object and add the container to it '''
        nwbfile.set_device(self.dev1)
        nwbfile.set_electrode_group(self.container)

    def getContainer(self, nwbfile):
        ''' Should take an NWBFile object and return the Container'''
        return nwbfile.get_electrode_group(self.container.name)

class TestElectricalSeriesIO(base.TestMapRoundTrip):

    def setUpContainer(self):
        self.dev1 = Device('dev1', 'a test source')
        channel_description = ('ch1', 'ch2')
        channel_location = ('lo1', 'lo2')
        channel_filtering = ('fi1', 'fi2')
        channel_coordinates = ('co1', 'co2')
        channel_impedance = ('im1', 'im2')
        self.elec1 = ElectrodeGroup('elec1', 'a test source', channel_description, channel_location, channel_filtering, channel_coordinates, channel_impedance, 'desc1', 'loc1', self.dev1)
        data = list(zip(range(10), range(10, 20)))
        timestamps = list(map(lambda x: x/10, range(10)))
        return ElectricalSeries('test_eS', 'a hypothetical source', data, self.elec1, timestamps=timestamps)

    def setUpBuilder(self):
        device_builder = GroupBuilder('dev1',
                            attributes={'neurodata_type': 'Device',
                                        'namespace': 'core',
                                        'help': 'A recording device e.g. amplifier',
                                        'source': 'a test source'},
                         )
        elcgrp_builder = GroupBuilder('elec1',
                            attributes={'neurodata_type': 'ElectrodeGroup',
                                        'namespace': 'core',
                                        'help': 'A physical grouping of channels',
                                        'source': 'a test source'},
                            datasets={
                                'channel_description': DatasetBuilder('channel_description', ['ch1', 'ch2']),
                                'channel_location': DatasetBuilder('channel_location', ['lo1', 'lo2']),
                                'channel_filtering': DatasetBuilder('channel_filtering', ['fi1', 'fi2']),
                                'channel_coordinates': DatasetBuilder('channel_coordinates', ['co1', 'co2']),
                                'channel_impedance': DatasetBuilder('channel_impedance', ['im1', 'im2']),
                                'description': DatasetBuilder('description', 'desc1'),
                                'location': DatasetBuilder('location', 'loc1')
                            },
                            links={
                                'device': LinkBuilder('device', device_builder)
                            }
                        )
        data = list(zip(range(10), range(10, 20)))
        timestamps = list(map(lambda x: x/10, range(10)))
        return GroupBuilder('test_eS',
                                attributes={'source': 'a hypothetical source',
                                            'namespace': base.CORE_NAMESPACE,
                                            'comments': 'no comments',
                                            'description': 'no description',
                                            'neurodata_type': 'ElectricalSeries',
                                            'help': 'Stores acquired voltage data from extracellular recordings'},
                                datasets={'data': DatasetBuilder('data', data,
                                                                 attributes={'unit': 'volt',
                                                                             'conversion': 1.0,
                                                                             'resolution': 0.0}),
                                          'timestamps': DatasetBuilder('timestamps', timestamps,
                                                                 attributes={'unit': 'Seconds', 'interval': 1})},
                                links={'electrode_group': LinkBuilder('electrode_group', elcgrp_builder)})

    def addContainer(self, nwbfile):
        ''' Should take an NWBFile object and add the container to it '''
        nwbfile.set_device(self.dev1)
        nwbfile.set_electrode_group(self.elec1)
        nwbfile.add_raw_timeseries(self.container)

    def getContainer(self, nwbfile):
        ''' Should take an NWBFile object and return the Container'''
        return nwbfile.get_raw_timeseries(self.container.name)


class TestClusteringIO(base.TestMapRoundTrip):

    def setUpBuilder(self):
        return GroupBuilder('Clustering',
            attributes={
               'help': 'Clustered spike data, whether from automatic clustering tools (eg, klustakwik) or as a result of manual sorting',
               'source': "an example source for Clustering",
               'neurodata_type': 'Clustering',
               'namespace': base.CORE_NAMESPACE},
            datasets={
               'num': DatasetBuilder('num', [0, 1, 2, 0, 1, 2]),
               'times': DatasetBuilder('times', list(range(10,61,10))),
               'peak_over_rms': DatasetBuilder('peak_over_rms', [100, 101, 102]),
               'description': DatasetBuilder('description', "A fake Clustering interface")}
        )

    def setUpContainer(self):
        return Clustering("an example source for Clustering", "A fake Clustering interface", [0, 1, 2, 0, 1, 2], [100, 101, 102], list(range(10,61,10)))
