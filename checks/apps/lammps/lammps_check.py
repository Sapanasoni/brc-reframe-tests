# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn


class LAMMPSCheck(rfm.RunOnlyRegressionTest):
    valid_prog_environs = ['gcc-mpi']
    modules = ['lammps']
    exclusive_access = True

    sourcesdir = 'src'

    @run_after('init')
    def setup_by_system(self):
        return

    @performance_function('timesteps/s')
    def perf(self):
        return sn.extractsingle(r'\s+(?P<perf>\S+) timesteps/s',
                                self.stdout, 'perf', float)

    @sanity_function
    def assert_energy_diff(self):
        #energy_reference = -4.6195
        #energy = sn.extractsingle(
        #    r'\s+100(\s+\S+){3}\s+(?P<energy>\S+)\s+\S+\s\n',
        #    self.stdout, 'TotEng', float)
        #energy_diff = sn.abs(energy - energy_reference)
        return sn.all([
            sn.assert_found(r'Total wall time:', self.stdout),
            #sn.assert_lt(energy_diff, 6e-4)
        ])


"""
@rfm.simple_test
class LAMMPSGPUCheck(LAMMPSCheck):
    descr = f'LAMMPS GPU check'
    valid_systems = ['lrc:es1r8']
    executable = 'lmp'
    executable_opts = ['-sf gpu', '-pk gpu 1', '-in in.lj']
    num_gpus_per_node = 1
    reference = {
            'lrc:es1r8': {'perf': (800., -0.10, None, 'timesteps/s')},
        }
    num_tasks = 2
    num_tasks_per_node = 2
"""

@rfm.simple_test
class LAMMPSCPUCheck(LAMMPSCheck):
    descr = f'LAMMPS CPU check'
    valid_systems = ['lrc', 'brc']
    reference = {
            'lrc:lr3': {'perf': (400., -0.1, None, 'timesteps/s')},
            'lrc:lr7': {'perf': (800., -0.1, None, 'timesteps/s')},
            'lrc:lr8': {'perf': (1600., -0.1, None, 'timesteps/s')},
        }
    @run_after('init')
    def setup_by_scale(self):
        self.executable = 'lmp'
        self.executable_opts = ['-in in.lj']
        self.num_tasks = 24
        self.num_tasks_per_node = 12
