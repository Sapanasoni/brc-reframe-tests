# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

"""
@rfm.simple_test
class Alltoall_Test(rfm.RegressionTest):
    valid_systems = ['lrc:lr3', 'lrc:lr3pmi2', 'lrc:lr7']
    descr = 'Alltoall OSU microbenchmark'
    build_system = 'Make'
    executable = './osu_alltoall'
    # The -m option sets the maximum message size
    # The -x option sets the number of warm-up iterations
    # The -i option sets the number of iterations
    executable_opts = ['-m', '8', '-x', '1000', '-i', '10000']
    valid_prog_environs = ['gcc-mpi', 'intel-mpi']
    num_tasks_per_node = 1
    num_tasks = 8

    reference = {
            'lrc:lr3' : {
                'latency': (5, None, 0.1, 'us')
                },
            }

    @run_before('compile')
    def set_makefile(self):
        self.build_system.makefile = 'Makefile_alltoall'

    @sanity_function
    def assert_found_8MB_latency(self):
        return sn.assert_found(r'^8', self.stdout)

    @run_before('run')
    def set_job_options(self):
        self.job.options = ['--qos=lr_normal']

    @run_before('performance')
    def set_performance_patterns(self):
        self.perf_patterns = {
                'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                    self.stdout, 'latency', float)
                }

#    @run_after('setup')
#    def set_intel_mpi_env_vars(self):
#        if self.current_environ.name in {'intel-mpi'}:
#            self.env_vars = {'I_MPI_OFI_PROVIDER':'mlx',
#                             'I_MPI_PMI_LIBRARY':'/usr/lib64/libpmi2.so',
#                             }

"""
class Pt2Pt_BaseTest(rfm.RegressionTest):
    def __init__(self):
        self.num_tasks = 2
        self.num_tasks_per_node = 1
        self.descr = 'P2P microbenchmark'
        self.build_system = 'Make'
        self.build_system.makefile = 'Makefile_p2p'
        self.valid_systems = ['lrc', 'lrcgpu','brc']
        self.valid_prog_environs = ['gcc-mpi', 'intel-mpi', 'nvhpc-mpi']
        self.exclusive_access = True
        self.sanity_patterns = sn.assert_found(r'^4194304', self.stdout)

    @run_before('run')
    def replace_launcher(self):
        if self.current_environ.name == 'intel-mpi':
            self.job.launcher = rfm.core.backends.getlauncher('srunpmi2')()

    @run_before('run')
    def setup_run(self):
        if self.current_system.name in ['lrcgpu']:
            self.num_gpus_per_node = 1
            self.num_tasks_per_node = 1
            self.num_cpus_per_task = 2

@rfm.simple_test
class Pt2Pt_CPU_Bandwidth(Pt2Pt_BaseTest):
    def __init__(self):
        super().__init__()
        self.executable = './p2p_osu_bw'
        self.executable_opts = ['-x', '100', '-i', '1000']
        self.reference = {
                'lrc:lr4': {
                    'bw': (6250, -0.1, None, 'MB/s')
                    },
                'lrc:lr5': {
                    'bw': (6250, -0.1, None, 'MB/s')
                    },
                'lrc:lr6': {
                    'bw': (6250, -0.1, None, 'MB/s')
                    },
                'lrc:lr6pmi2': {
                    'bw': (6250, -0.1, None, 'MB/s')
                    },
                'lrc:lr7': {
                    'bw': (12500, -0.1, None, 'MB/s')
                    },
                'lrc:lr8': {
                    'bw': (12500, -0.1, None, 'MB/s')
                },
                }
        
        self.perf_patterns = {
                'bw': sn.extractsingle(r'^4194304\s+(?P<bw>\S+)',
                    self.stdout, 'bw', float)
                }

@rfm.simple_test
class Pt2Pt_CPU_Latency(Pt2Pt_BaseTest):
    def __init__(self):
        super().__init__()
        self.executable_opts = ['-x', '100', '-i', '1000']

        self.executable = './p2p_osu_latency'
        self.reference = {
                'lrc:lr4': {
                    'latency': (2, None, 0.5, 'us')
                    },
                'lrc:lr5': {
                    'latency': (2, None, 0.5, 'us')
                    },
                'lrc:lr6': {
                    'latency': (2, None, 0.1, 'us')
                    },
                'lrc:lr6pmi2': {
                    'latency': (2, None, 0.1, 'us')
                    },
                'lrc:lr7': {
                    'latency': (2, None, 0.1, 'us')
                    },
                'lrc:lr8': {
                    'latency': (2, None, 0.1, 'us')
                },
                }

        self.perf_patterns = {
                'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                    self.stdout, 'latency', float)
                }

