# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

# Adapted from CSCS: github.com/eth-cscs/cscs-reframe-tests

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class GSL_Library_Check(rfm.RegressionTest):
    def __init__(self):
        self.descr = f'Test GSL Library compilation and linking'
        self.valid_systems = ['lrc', 'brc']
        self.valid_prog_environs = ['gcc', 'intel']
        self.modules = ['gsl']
        
        self.sourcesdir = 'src'
        self.sourcepath = 'gsl_bessel_example.c'
        self.executable = 'gsl_bessel_example'
        self.build_system = 'Make'
        self.sanity_patterns = sn.assert_found('-1.77596771314338', self.stdout)