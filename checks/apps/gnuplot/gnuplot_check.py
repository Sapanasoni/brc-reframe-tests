# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Gnuplot_Check(rfm.RunOnlyRegressionTest):
    descr = 'Test that gnuplot is available'
    valid_systems = ['lrc:lr3']
    valid_prog_environs = ['builtin']
    modules = ['gnuplot']
    executable = 'gnuplot'
    executable_opts = ['-e "set term pdf" BesselJ.dem > besselj.pdf']
    postrun_cmds = ['ls besselj.pdf']

    @sanity_function
    def assert_success(self):
        return sn.assert_not_found(r'command not found', self.stderr) 