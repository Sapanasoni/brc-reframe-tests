import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class MPI_HelloWorld(rfm.RegressionTest):
    valid_systems = ['lrc', 'brc']
    # currently there is no gcc-openacc but kept here if
    # we include this in the future
    valid_prog_environs = ['gcc-mpi', 'intel-mpi']
    sourcesdir = 'src'
    build_system = 'SingleSource'

    @run_after('init')
    def set_numtasks(self):
        self.num_tasks = 2
        self.num_tasks_per_node = 1
        self.sourcepath = 'mpi_hello_world.c'

    @run_before('compile')
    def set_variables(self):
        self.exclusive_access = False

    @run_before('run')
    def replace_launcher(self):
        if self.current_environ.name == 'intel-mpi':
            self.job.launcher = rfm.core.backends.getlauncher('srunpmi2')()
            
#    @run_before('compile')
#    def setflags(self):
#        self.build_system.fflags = ['-acc=gpu -cuda -Minfo=accel -gpu=cc70,cc75,cc86,cuda12.2']

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello world from processor', self.stdout)
