# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2021 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class DGEMMTest(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'DGEMM performance test'
        self.sourcepath = 'dgemm.c'

        # the perf patterns are automatically generated inside sanity
        self.perf_patterns = {}
        self.valid_systems = ['lrc', 'brc']
        self.valid_prog_environs = ['gcc-mpi', 'intel-mpi']

        self.num_tasks = 2
        self.use_multithreading = True
        self.executable_opts = ['6144', '122288', '3072']
        self.build_system = 'SingleSource'
        self.build_system.cflags = ['-O3']
        self.sys_reference = {
            'lrc:lr6': (500, -0.1, None, 'Gflop/s'),       # some nodes give ~ 900 Gflops
            'lrc:lr5': (550, -0.1, None, 'Gflop/s'),
            'lrc:lr4': (300, -0.1, None, 'Gflop/s'),
            'lrc:lr7': (1100,-0.1, None, 'Gflop/s'),
        }

    @run_before('compile')
    def setflags(self):
        if self.current_environ.name.startswith('gcc'):
            if self.current_system.name.startswith('sl7'):
                self.modules = ['mkl']
            else:
                self.modules = ['intel-oneapi-mkl']
            self.build_system.cppflags = [
                '-DMKL_LP64', '-m64', '-I${MKLROOT}/include'
            ]
            self.build_system.cflags += ['-fopenmp']
            self.build_system.ldflags = ['-m64', '-L${MKLROOT}/lib/intel64', '-Wl,--no-as-needed',
            '-lmkl_intel_lp64', '-lmkl_gnu_thread', '-lmkl_core', '-lgomp', '-lpthread', '-lm', '-ldl']
        elif self.current_environ.name.startswith('intel'):
            self.modules = ['intel-oneapi-mkl']
            self.build_system.cflags = ['-qmkl=parallel']

    @run_before('run')
    def replace_launcher(self):
        if self.current_environ.name == 'intel-mpi':
            self.job.launcher = rfm.core.backends.getlauncher('srunpmi2')()

    @run_before('run')
    def set_tasks(self):
        self.num_cpus_per_task = 16

        if self.num_cpus_per_task:
            self.env_vars = {
                'OMP_NUM_THREADS': str(self.num_cpus_per_task)
            }        
    def set_memory_limit(self):
        self.job.options = ['--mem-per-cpu=4G']

    @sanity_function
    def eval_sanity(self):
        all_tested_nodes = sn.evaluate(sn.extractall(
            r'(?P<hostname>\S+):\s+Time for \d+ DGEMM operations',
            self.stdout, 'hostname'))
        num_tested_nodes = len(all_tested_nodes)
        failure_msg = ('Requested %s node(s), but found %s node(s)' %
                       (self.job.num_tasks, num_tested_nodes))
        sn.evaluate(sn.assert_eq(num_tested_nodes, self.job.num_tasks,
                                 msg=failure_msg))

        for hostname in all_tested_nodes:
            partition_name = self.current_partition.fullname
            ref_name = '%s:%s' % (partition_name, hostname)
            self.reference[ref_name] = self.sys_reference.get(
                partition_name, (0.0, None, None, 'Gflop/s')
            )
            self.perf_patterns[hostname] = sn.extractsingle(
                r'%s:\s+Avg\. performance\s+:\s+(?P<gflops>\S+)'
                r'\sGflop/s' % hostname, self.stdout, 'gflops', float)

        return True        
