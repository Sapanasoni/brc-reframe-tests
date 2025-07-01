# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
from hpctestlib.sciapps.gromacs.benchmarks import gromacs_check


@rfm.simple_test
class lrc_gromacs_check(gromacs_check):
    valid_prog_environs = ['gcc-mpi']
    modules = ['gromacs']
    use_multithreading = False
    executable_opts += ['-dlb yes', '-ntomp 1', '-npme -1']

    num_nodes = parameter([1, 2], loggable=True)

    benchmark_info = parameter([
        ('HECBioSim/Crambin', -204107.0, 0.001),
    #    ('HECBioSim/Glutamine-Binding-Protein', -724598.0, 0.001),
    #    ('HECBioSim/hEGFRDimer', -3.32892e+06, 0.001),
    #    ('HECBioSim/hEGFRDimerSmallerPL', -3.27080e+06, 0.001),
    #    ('HECBioSim/hEGFRDimerPair', -1.20733e+07, 0.001),
    #    ('HECBioSim/hEGFRtetramerPair', -2.09831e+07, 0.001)
    ], fmt=lambda x: x[0], loggable=True)

    allref = {
        1: {
            'sm_86': {
                'HECBioSim/Crambin': (195.0, -0.1, None, 'ns/day'),
            },
            'sandybridge': {
                'HECBioSim/Crambin': (7.0, -0.1, None, 'ns/day'),
            },
            'icelake': {
                'HECBioSim/Crambin': (31.0, -0.1, None, 'ns/day'),
            },
        },
        2: {
            'sm_86': {
                'HECBioSim/Crambin': (202.0, -0.1, None, 'ns/day'),
            },
            'sandybridge': {
                'HECBioSim/Crambin': (12.0, -0.1, None, 'ns/day'),
            },
            'icelake': {
                'HECBioSim/Crambin': (65.0, -0.1, None, 'ns/day'),
            },
        },
    }

    @run_after('init')
    def setup_filtering_criteria(self):
        self.descr += f' ({self.num_nodes} node(s))'

        valid_systems = {
            'cpu': {
                1: ['lrc:lr3', 'lrc:lr7'],
                2: ['lrc:lr3', 'lrc:lr7'],
            },
            'gpu': {
                1: ['lrcgpu:es1'],
                2: ['lrcgpu:es1'],
            }
        }
        try:
            self.valid_systems = valid_systems[self.nb_impl][self.num_nodes]
        except KeyError:
            self.valid_systems = []

    @run_before('run')
    def setup_run(self):
        self.skip_if_no_procinfo()

        if self.nb_impl == 'gpu':
            self.num_gpus_per_node = 1
            self.num_cpus_per_task = 2

        proc = self.current_partition.processor

        partition_to_arch = {'es1A40': 'sm_86',
                             'es1r8' : 'sm_75',
                             'es1V100': 'sm_70',
                             'lr3': 'sandybridge',
                             'lr4': 'haswell',
                             'lr7': 'icelake',}

        arch = partition_to_arch[self.current_partition.name]

        try:
            found = self.allref[self.num_nodes][arch][self.bench_name]
        except KeyError:
            self.skip(f'Configuration with {self.num_nodes} node(s) of '
                      f'{self.bench_name} is not supported on {arch}')
        
        self.reference = {
            '*': {
                'perf': self.allref[self.num_nodes][arch][self.bench_name]
            }
        }

        # Setup parallel run
        self.num_tasks_per_node = proc.num_cores
        self.num_tasks = self.num_nodes * self.num_tasks_per_node
