# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# Adapted from CSCS: github.com/eth-cscs/cscs-reframe-tests

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class NetCDF_Fortran_Check(rfm.RegressionTest):
    def __init__(self):
        self.descr = f'Test for NetCDF Fortran library'
        self.valid_systems = ['lrc', 'brc']
        self.valid_prog_environs = ['gcc-mpi', 'intel-mpi']

        self.modules = [f'netcdf-fortran']
        self.executable = f'simple_xy_wr'

        self.sourcesdir = 'src'
        self.sourcepath = 'simple_xy_wr.f90'
        self.build_system = 'Make'        
        self.sanity_patterns = sn.assert_found('SUCCESS writing example file', self.stdout)

    @run_before('run')
    def replace_launcher(self):
        if self.current_environ.name == 'intel-mpi':
            self.job.launcher = rfm.core.backends.getlauncher('srunpmi2')()
