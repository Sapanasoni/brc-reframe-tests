# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# Adapted for Lawrencium @ LBL
# code from hpctestlib.microbenchmarks.gpu.gpu_burn copied here too

import sys
import os

import reframe as rfm
import reframe.utility.typecheck as typ
import reframe.utility.sanity as sn

sys.path.append(os.path.abspath(os.path.join(__file__, '../../../..')))
import microbenchmarks.gpu.hooks as hooks

class gpu_burn_check(rfm.RegressionTest):
    '''GPU burn benchmark

    This benchmark runs continuously GEMM, either single or double precision,
    on a selected set of GPUs on the node where the benchmark runs.

    The floating point precision of the computations, the duration of the
    benchmark as well as the list of GPU devices that the benchmark will run
    on can be controlled through test variables.

    '''
    
    use_dp = variable(typ.Bool, value=True)
    duration = variable(int, value=50)
    devices = variable(typ.List[int], value=[])

    num_tasks = 1
    num_tasks_per_node = 1

    descr = 'GPU burn test'
    sourcesdir = '../src/gpu_burn'
    build_system = 'Make'
    executable = 'gpu_burn.x'
    
    gpu_build = variable(str, type(None), value=None)
    gpu_arch = variable(str, type(None), value=None)

    @run_before('compile')
    def setup_build(self):
        curr_part = self.current_partition
        curr_env = self.current_environ

        if self.gpu_build is None:
            # Try to set the build type from the partition features
            if 'cuda' in curr_env.features:
                self.gpu_build = 'cuda'
            elif 'hip' in curr_env.features:
                self.gpu_build = 'hip'
        
        gpu_devices = curr_part.select_devices('gpu')
        if self.gpu_arch is None and gpu_devices:
            # Try to set the gpu arch from the partition's devices; we assume
            # all devices are of the same architecture
            self.gpu_arch = gpu_devices[0].arch
        
        if self.gpu_build == 'cuda':
            self.build_system.makefile = 'makefile.cuda'
            if self.gpu_arch:
                cc = self.gpu_arch.replace('sm_', 'compute_')
                self.build_system.cxxflags = [f'-arch=compute_{cc}',
                                              f'-code=compute_{self.gpu_arch}']
        elif self.gpu_build == 'hip':
            self.build_system.makefile = 'makefile.hip'
            if self.gpu_arch:
                self.build_system.cxxflags = [
                    f'--amdgpu-target={self.gpu_arch}'
                ]
        else:
            raise ValueError(f'unknown build variant: {self.gpu_build!r}')
    
    @run_before('run')
    def set_exec_opts(self):
        if self.use_dp:
            self.executable_opts += ['-d']

        if self.devices:
            self.executable_opts += ['-D',
                                     ','.join(str(x) for x in self.devices)]
        
        self.executable_opts += [str(self.duration)]
    
    #@run_before('run')
    #def add_exec_prefix(self):
    #    self.executable = os.path.join(self.gpu_burn_binaries.stagedir,
    #                                   self.executable)

    @run_before('run')
    def set_num_gpus_per_node(self):
        if self.num_gpus_per_node is not None:
            return

        gpu_devices = self.current_partition.select_devices('gpu')
        if gpu_devices:
            self.num_gpus_per_node = gpu_devices[0].num_devices

    @sanity_function
    def assert_sanity(self):
        num_gpus_detected = sn.extractsingle(
            r'==> devices selected \((\d+)\)', self.stdout, 1, int
        )
        return sn.assert_eq(
            sn.count(sn.findall(r'GPU\s+\d+\(OK\)', self.stdout)),
            num_gpus_detected
        )

    def _extract_metric(self, metric):
        return sn.extractall(
            r'GPU\s+\d+\(OK\):\s+(?P<perf>\S+)\s+GF/s\s+'
            r'(?P<temp>\S+)\s+Celsius', self.stdout, metric, float
        )

    @performance_function('Gflop/s')
    def gpu_perf_min(self):
        '''Lowest performance recorded among all the selected devices.'''
        return sn.min(self._extract_metric('perf'))

    @performance_function('degC')
    def gpu_temp_max(self):
        '''Maximum temperature recorded among all the selected devices.'''
        return sn.max(self._extract_metric('temp'))


class lrc_gpu_burn_check_base(gpu_burn_check):
    use_dp = True
    duration = 120
    exclusive_access = True
    valid_systems = ['lrcgpu']
    valid_prog_environs = ['cuda']    

    @run_after('setup')
    def set_gpu_arch(self):
        hooks.set_gpu_arch(self)
        hooks.set_num_gpus_per_node(self)

@rfm.simple_test
class gpu_burn_double_precision(lrc_gpu_burn_check_base):
    use_dp = True
    reference = {
        'lrcgpu:es1': {
            'gpu_perf_min': (475, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1A40': {
            'gpu_perf_min': (500, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1V100': {
            'gpu_perf_min': (6700, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1GRTX2080TI': {
            'gpu_perf_min': (475, -0.10, None, 'Gflop/s'),
        },
    }


@rfm.simple_test
class gpu_burn_single_precision(lrc_gpu_burn_check_base):
    use_dp = False
    reference = {
        'lrcgpu:es1': {
            'gpu_perf_min': (9000, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1A40': {
            'gpu_perf_min': (20000, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1V100': {
            'gpu_perf_min': (14000, -0.10, None, 'Gflop/s'),
        },
        'lrcgpu:es1GRTX2080TI': {
            'gpu_perf_min': (12250, -0.10, None, 'Gflop/s'),
        },
    }

