import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class mpi4py_builtin(rfm.RunOnlyRegressionTest):
    descr = 'Test installation of mpi4py on a single nod (no benchmark)'
    valid_prog_environs = ['builtin']
    valid_systems = ['lrc', 'brc']
    modules = ['python']

    num_tasks = 6

    executable = 'python'
    executable_opts = ['mpi4py_test.py', str(num_tasks)]

    use_multithreading = False
    

    @sanity_function
    def assert_mpi4py_version(self):
        return sn.all([sn.assert_found(r'mpi4py version: \s+\S+', self.stdout),
                      sn.assert_found(r'MPI Vendor is: \s+\S+', self.stdout),
                      sn.assert_found(r'0 of '+str(self.num_tasks), self.stdout)
        ])

@rfm.simple_test
class mpi4py_intel(rfm.RunOnlyRegressionTest):
    descr = 'Test installation of mpi4py on a single nod (no benchmark)'
    valid_prog_environs = ['intel-mpi']
    valid_systems = ['lrc', 'brc']
    modules = ['python']

    num_tasks = 6

    executable = 'python'
    executable_opts = ['mpi4py_test.py', str(num_tasks)]

    use_multithreading = False
    

    @sanity_function
    def assert_mpi4py_version(self):
        return sn.all([sn.assert_found(r'mpi4py version: \s+\S+', self.stdout),
                      sn.assert_found(r'MPI Vendor is: \s+\S+', self.stdout),
                      sn.assert_found(r'0 of '+str(self.num_tasks), self.stdout)
        ])