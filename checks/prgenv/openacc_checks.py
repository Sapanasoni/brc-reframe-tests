# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OpenACCFortranCheck(rfm.RegressionTest):
    #variant = parameter(['nompi', 'mpi'])
    # only include nompi variant now; can add mpi when we 
    # install nvhpc with mpi support or gcc+openmpi+openacc
    variant = parameter(['nompi'])
    valid_systems = ['lrcgpu', 'brcgpu']
    # currently there is no gcc-openacc but kept here if
    # we include this in the future
    valid_prog_environs = ['nvhpc']
    sourcesdir = 'src/openacc'
    build_system = 'SingleSource'
    num_gpus_per_node = 1
    num_tasks_per_node = 2
    num_cpus_per_task = 2

    @run_after('init')
    def set_numtasks(self):
        if self.variant == 'nompi':
            self.num_tasks = 1
            self.sourcepath = 'vecAdd_openacc_nompi.f90'
        else:
            self.num_tasks = 2
            self.sourcepath = 'vecAdd_openacc_mpi.f90'

    @run_before('compile')
    def set_variables(self):
        self.exclusive_access = False

    @run_before('compile')
    def setflags(self):
        self.build_system.fflags = ['-acc=gpu -cuda -Minfo=accel -gpu=cc70,cc75,cc86,cc90']

    @run_before('sanity')
    def set_sanity(self):
        result = sn.extractsingle(r'final result:\s+(?P<result>\d+\.?\d*)',
                                  self.stdout, 'result', float)
        self.sanity_patterns = sn.assert_reference(result, 1., -1e-5, 1e-5)
