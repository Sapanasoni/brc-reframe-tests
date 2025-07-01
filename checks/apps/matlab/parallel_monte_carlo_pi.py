# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# Copyright 2023 FAS Research Computing Harvard University
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# from https://github.com/fasrc/reframe-fasrc/blob/main/checks/software/user_codes/Parallel_Computing/MATLAB/Example1/paralell_monte_carlo_pi.py
# Adapted for Lawrencium

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Matlab_Parallel_MonteCarloPi(rfm.RunOnlyRegressionTest):
    descr = 'Uses Matlab to compute Pi in parallel using Monte Carlo method'
    valid_systems = ['lrc', 'brc']
    valid_prog_environs = ['builtin']
    build_system = 'SingleSource'
    sourcepath = 'parallel_monte_carlo.m'
    modules = ['matlab']
    executable = 'matlab -nosplash -nodesktop -r parallel_monte_carlo'

    @run_before('run')
    def set_num_threads(self):
        self.num_cpus_per_task = 8

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'Starting parallel pool', self.stdout) or sn.assert_found(r'Maximum number of users for MATLAB reached.', self.stderr)
