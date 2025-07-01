# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# Adapted from CSCS: github.com/eth-cscs/cscs-reframe-tests

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Boost_DateTime_Check(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'Test Boost datetime library'
        self.valid_systems = ['lrc', 'brc']
        self.valid_prog_environs = ['gcc-mpi']
        self.modules = ['boost']

        self.sourcesdir = 'src'
        self.sourcepath = 'date_time_example.cpp'
        self.executable = 'datetime'
        self.build_system = 'Make'
        self.sanity_patterns = sn.assert_found('2001-10-09', self.stdout)
