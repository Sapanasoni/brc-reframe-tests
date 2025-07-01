# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class FFTWTest(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'Simple FFTW compile and run test using mpi'
        self.valid_systems = ['lrc']
        self.valid_prog_environs = ['gcc-mpi']
        self.modules = ['fftw']
        self.sourcepath = 'fftw_benchmark.c'
        self.build_system = 'SingleSource'
        self.build_system.cflags = ['-O2', '$(pkg-config --cflags fftw3)']
        self.build_system.ldflags = ['-lfftw3_mpi', '-lm', 
                                     '-Wl,-rpath,$(pkg-config --variable=libdir fftw3)',
                                     '$(pkg-config --libs fftw3)']
        
        #self.num_task_per_node = 12

    @performance_function('s')
    def fftw_exec_time(self):
        return sn.extractsingle(
            r'execution time:\s+(?P<exec_time>\S+)', self.stdout,
            'exec_time', float
        )

    @sanity_function
    def assert_finished(self):
        return sn.assert_eq(
            sn.count(sn.findall(r'execution time', self.stdout)), 1
        )
    
    @run_before('run')
    def configure_exec_mode(self):
        self.num_tasks = 48
        self.executable_opts = [f'144 {self.num_tasks} 200 1']
        self.reference = {
            'lrc:lr3': {
                    'fftw_exec_time': (4.0, None, 0.1, 's'),
                },
            'lrc:lr7': {
                    'fftw_exec_time': (1.2, None, 0.1, 's'),
                },
            }
