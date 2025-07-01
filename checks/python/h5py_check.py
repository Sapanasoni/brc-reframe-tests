import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class h5pyCheck(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = 'Check h5py installation (basic)'
        self.valid_systems = ['lrc', 'brc']
        self.valid_prog_environs = ['builtin']
        
        self.modules = ['python']
        self.executable = 'python'
        self.executable_opts = ['h5py_test.py']
        
        # set the following in case the test is run on a gpu node
        self.num_gpus_per_node = 1
        self.num_cpus_per_task = 2

        self.sanity_patterns = sn.assert_found(r'simple h5py test passed.', self.stdout)

