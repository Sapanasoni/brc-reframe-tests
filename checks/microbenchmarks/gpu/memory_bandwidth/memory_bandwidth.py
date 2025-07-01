# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import reframe as rfm
from hpctestlib.microbenchmarks.gpu.memory_bandwidth import *

sys.path.append(os.path.abspath(os.path.join(__file__, '../../../..')))
import microbenchmarks.gpu.hooks as hooks


class SystemConfigLRC(rfm.RegressionMixin):
    # Inject external hooks
    @run_after('setup')
    def set_gpu_arch(self):
        hooks.set_gpu_arch(self)

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)


@rfm.simple_test
class gpu_bandwidth_check(GpuBandwidth, SystemConfigLRC):
    valid_systems = [
        'lrcgpu'
    ]
    valid_prog_environs = ['cuda']
    reference = {
        'lrcgpu:es1A40': {
            'h2d': (24.0, -0.1, None, 'GB/s'),
            'd2h': (24.0, -0.1, None, 'GB/s'),
            'd2d': (500.0, -0.1, None, 'GB/s')
        },
        'lrcgpu:es1V100': {
            'h2d': (11.3, -0.1, None, 'GB/s'),
            'd2h': (12.2, -0.1, None, 'GB/s'),
            'd2d': (500.0, -0.1, None, 'GB/s')
        },
        'lrcgpu:es1GRTX2080TI': {
            'h2d': (11.3, -0.1, None, 'GB/s'),
            'd2h': (12.2, -0.1, None, 'GB/s'),
            'd2d': (500.0, -0.1, None, 'GB/s')
        },
    }
    
