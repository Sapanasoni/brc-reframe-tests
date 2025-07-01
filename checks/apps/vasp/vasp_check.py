# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# adapted from https://github.com/reframe-hpc/cscs-reframe-tests/blob/main/checks/apps/vasp/vasp_check.py

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class VASPCheck(rfm.RunOnlyRegressionTest):
    modules = ['vasp']
    executable = 'vasp_std'
    keep_files = ['OUTCAR']
    strict_check = False
    #use_multithreading = False

    num_nodes = parameter([1], loggable=True)
    allref = {
        1: {
            'lrcgpu:es1H100': {'elapsed_time': (200, None, 0.10, 's')},
            'lrcgpu:es1V100': {'elapsed_time': (400, None, 0.10, 's')},
            'lrc:lr6': {'elapsed_time': (640, None, 0.10, 's')},
            'lrc:lr7': {'elapsed_time': (550, None, 0.10, 's')},
            'lrc:lr8': {'elapsed_time': (850, None, 0.10, 's')},
            },
        2: {
            'lrc:lr4': {'elapsed_time': (1000, None, 0.10, 's')},
            'lrc:lr5': {'elapsed_time': (1000, None, 0.10, 's')},
            'lrc:lr6': {'elapsed_time': (320, None, 0.10, 's')},
            'lrc:lr7': {'elapsed_time': (280, None, 0.10, 's')},
            'lrc:lr8': {'elapsed_time': (650, None, 0.10, 's')},
            'lrcgpu:es1H100': {'elapsed_time': (200, None, 0.10, 's')},
        },
        6: {
            'lrc:lr6': {'elapsed_time': (50, None, 0.10, 's')},
            'lrc:lr7': {'elapsed_time': (40, None, 0.10, 's')},
        }
    }

    @performance_function('s')
    def elapsed_time(self):
        return sn.extractsingle(r'Elapsed time \(sec\):'
                                r'\s+(?P<time>\S+)', 'OUTCAR',
                                'time', float)

    @sanity_function
    def assert_reference(self):
        force = sn.extractsingle(r'1 F=\s+(?P<result>\S+)',
                                 self.stdout, 'result', float)
        return sn.assert_reference(force, -61.646438, -1e-5, 1e-5)

    @run_after('init')
    def setup_system_filtering(self):
        self.descr = f'VASP check ({self.num_nodes} node(s))'

        # setup system filter
        valid_systems = {
            1: ['lrc', 'lrcgpu'],
            2: ['lrc', 'lrcgpu'],
            6: ['lrc']
        }

        self.skip_if(self.num_nodes not in valid_systems,
                     f'No valid systems found for {self.num_nodes}(s)')
        self.valid_systems = valid_systems[self.num_nodes]

        # setup programming environment filter
        if self.current_system.name in ['lrcgpu']:
            print ("here")
            self.valid_prog_environs = ['nvhpc-mpi']
        else:
            self.valid_prog_environs = ['intel-mpi']


    @run_before('run')
    def setup_run(self):
        # set auto-detected architecture
        self.skip_if_no_procinfo()
        proc = self.current_partition.processor
        # replace launcher for intel-mpi
        if self.current_environ.name == 'intel-mpi':
            self.job.launcher = rfm.core.backends.getlauncher('srunpmi2')()

        # common setup
        self.num_tasks_per_node = proc.num_sockets
        self.num_cpus_per_task = proc.num_cores // self.num_tasks_per_node

        self.env_vars = {
            'OMP_NUM_THREADS': self.num_cpus_per_task,
        }

        if self.current_system.name in ['lrcgpu']:
            if self.current_partition.name in ['es1H100']:
                self.num_gpus_per_node = int(8 / self.num_nodes)
                self.num_tasks_per_node = 14
            elif self.current_partition.name in ['es1V100']:
                self.num_gpus_per_node = 2
                self.num_tasks_per_node = 4

            self.num_tasks_per_node = self.num_gpus_per_node
            #self.job.launcher.options = [f"--map-by node:PE={self.num_cpus_per_task} --bind-to core"]
            self.env_vars['OMP_NUM_THREADS'] = 1   # disable openmp threading for gpu testing

        self.num_tasks = self.num_nodes * self.num_tasks_per_node

        # setup performance references
        self.reference = self.allref[self.num_nodes]


            
                
