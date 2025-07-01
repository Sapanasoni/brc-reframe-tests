# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm

from hpctestlib.python.numpy.numpy_ops import numpy_ops_check


@rfm.simple_test
class numpy_perf_singlethread(numpy_ops_check):
    """
    the performance limit here is pretty high to comfortable allow openBLAS
    """
    valid_prog_environs = ['builtin']
    valid_systems = ['lrc:lr3',
                     'lrc:lr6',
                     'lrc:lr7',
                     'lrc:lr8',]
    modules = ['python']
    num_tasks_per_node = 1
    use_multithreading = False
    all_ref = {
        'zen4@128c': {
            'dot': (2, None, 0.1, 's'),
            'svd': (1.0, None, 0.1, 's'),
            'cholesky': (0.5, None, 0.1, 's'),
            'eigendec': (7.5, None, 0.1, 's'),
            'inv': (1.0, None, 0.1, 's'),
        },
        'icelake@56c': {  
            'dot': (2, None, 0.1, 's'),
            'svd': (1.0, None, 0.1, 's'),
            'cholesky': (0.5, None, 0.1, 's'),
            'eigendec': (7.5, None, 0.1, 's'),
            'inv': (1.0, None, 0.1, 's'),
        },
        'cascadelake@32c': {
            'dot': (2.0, None, 0.1, 's'),
            'svd': (1.0, None, 0.1, 's'),
            'cholesky': (0.5, None, 0.1, 's'),
            'eigendec': (7.5, None, 0.1, 's'),
            'inv': (1.0, None, 0.1, 's'),
        },
        'sandybridge@16c': {
            'dot': (10.0, None, 0.1, 's'),
            'svd': (3.0, None, 0.1, 's'),
            'cholesky': (1.0, None, 0.1, 's'),
            'eigendec': (15.0, None, 0.1, 's'),
            'inv': (2.5, None, 0.1, 's'),        },
    }
    @run_after('setup')
    def set_num_cpus_per_task(self):
        self.num_cpus_per_task = self.current_partition.processor.num_cores
        self.env_vars = {
            'OMP_NUM_THREADS': 1
        }

    @run_before('performance')
    def set_perf_ref(self):
        arch = self.current_partition.processor.arch
        pname = self.current_partition.fullname
        num_cores = self.current_partition.processor.num_cores
        self.reference = {
            pname: self.all_ref[f'{arch}@{num_cores}c']
        }

@rfm.simple_test
class numpy_perf_threaded(numpy_ops_check):
    valid_prog_environs = ['builtin']
    valid_systems = ['lrc:lr7', 'lrc:lr8']
    modules = ['python']
    num_tasks_per_node = 1
    use_multithreading = False
    all_ref = {
        'zen4@128c': {
            'dot': (0.1, None, 0.1, 's'),
            'svd': (0.4, None, 0.1, 's'),
            'cholesky': (0.1, None, 0.1, 's'),
            'eigendec': (3.0, None, 0.1, 's'),      
            'inv': (0.2, None, 0.1, 's'),          
        },
        'icelake@56c': {                            # lr7
            'dot': (0.12, None, 0.1, 's'),           
            'svd': (0.5, None, 0.1, 's'),           
            'cholesky': (0.1, None, 0.1, 's'),      
            'eigendec': (3.4, None, 0.1, 's'),      
            'inv': (0.2, None, 0.1, 's'),          
        },
        'sandybridge@16c': {
            'dot': (1.2, None, 0.1, 's'),   
            'svd': (1.4, None, 0.1, 's'),   
            'cholesky': (0.5, None, 0.1, 's'), 
            'eigendec': (15, None, 0.1, 's'),
            'inv': (0.5, None, 0.1, 's'),   
        },
    }
    
    @run_after('setup')
    def set_num_cpus_per_task(self):
        self.num_cpus_per_task = self.current_partition.processor.num_cores
        self.env_vars = {
            'OMP_NUM_THREADS': self.num_cpus_per_task
        }

    @run_before('performance')
    def set_perf_ref(self):
        arch = self.current_partition.processor.arch
        pname = self.current_partition.fullname
        num_cores = self.current_partition.processor.num_cores
        self.reference = {
            pname: self.all_ref[f'{arch}@{num_cores}c']
        }
