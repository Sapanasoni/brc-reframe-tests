import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class R_Fibonacci(rfm.RunOnlyRegressionTest):
    descr = 'Print first 10 Fibonacci numbers'
    valid_systems = ['lrc', 'brc']
    valid_prog_environs = ['builtin']
    build_system = 'SingleSource'
    sourcepath = 'fib.R'
    modules = ['r']
    #executable = 'Rscript count_down.R > count_down.Rout'
    executable = 'R CMD BATCH --no-save --no-restore fib.R'

    @sanity_function
    def assert_sanity(self):
        return sn.assert_found(r'0 1 1 2 3 5 8 13 21 34', "fib.Rout")