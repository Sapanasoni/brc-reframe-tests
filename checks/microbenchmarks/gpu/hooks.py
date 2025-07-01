# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

#
# Hooks specific to the CSCS GPU microbenchmark tests.
#

# Adapted for Lawrencium

def set_gpu_arch(self):
    '''Set the compile options for the gpu microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    self.gpu_arch = None

    # Nvidia options
    self.gpu_build = 'cuda'
    #self.modules = ['cuda']

    if cp in {'lrcgpu:es1'}:
        self.gpu_arch = '75'
    elif cp in {'lrcgpu:es1V100'}:
        self.gpu_arch = '70'
    elif cp in {'lrcgpu:es1A40'}:
        self.gpu_arch = '86'
    elif cp in {'lrcgpu:es1GRTX2080TI'}:
        self.gpu_arch = '75'

def set_num_gpus_per_node(self):
    '''Set the GPUs per node for the GPU microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    self.num_cpus_per_task = 2
    if cp in {'lrcgpu:es1r8'}:
        self.num_gpus_per_node = 4
    elif cp in {'lrcgpu:es1V100'}:
        self.num_gpus_per_node = 2
    elif cp in {'lrcgpu:es1A40'}:
        self.num_gpus_per_node = 4
    elif cp in {'lrcgpu:es1GRTX2080TI'}:
        self.num_gpus_per_node = 4
    else:
        self.num_gpus_per_node = 1
    self.num_tasks = 1
    self.num_tasks_per_node = 1
