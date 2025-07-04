import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class PyTorchCIFAR10(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = 'PyTorch CIFAR10 performance comparison'
        self.valid_systems = ['lrc', 'lrcgpu', 'brc', 'brcgpu',]
        self.valid_prog_environs = ['builtin', 'builtin_gpu']

        self.modules = ['ml/pytorch']

        self.executable = 'python'
        self.executable_opts = ['cifar10.py']

        self.reference = {
            'lrcgpu:es1GRTX2080TI': {
                'tf_exec_time': (130, None, 0.1, 's'),
            },
            'lrc:lr4': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'lrc:lr5': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'lrc:lr6': {
                'tf_exec_time': (120, None, 0.1, 's'),
            },
            'lrcgpu:es1H100': {
                'tf_exec_time': (45, None, 0.1, 's'),
            },
            'lrcgpu:es1A40': {
                'tf_exec_time': (85, None, 0.1, 's'),
            },
            'lrcgpu:es1V100': {
                'tf_exec_time': (120, None, 0.1, 's'),
            },
            'lrc:lr7': {
                'tf_exec_time': (90, None, 0.1, 's'),
            },
            'lrc:lr8': {
                'tf_exec_time': (60, None, 0.1, 's'),
            },
            'brcgpu:savio2_gpu_1080TI': {
                'tf_exec_time': (125, None, 0.1, 's'),
            },
            'brcgpu:savio4_gpu_L40': {
                'tf_exec_time': (50, None, 0.1, 's'),
            },
            'brcgpu:savio3_gpu_GTX2080TI': {
                'tf_exec_time': (120, None, 0.1, 's'),
            },
            'brcgpu:savio3_gpu_V100': {
                'tf_exec_time': (127, None, 0.1, 's'),
            },
            'brcgpu:savio3_gpu_A40': {
                'tf_exec_time': (85, None, 0.1, 's'),
            },
            'brcgpu:savio3_gpu_TITAN': {
                'tf_exec_time': (115, None, 0.1, 's'),
            },
            'brcgpu:savio4_gpu_A5000': {
                'tf_exec_time': (90, None, 0.1, 's'),
            },
            'brc:savio2': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio2_bigmem': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio2_htc': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio2_knl': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio3': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio3_bigmem': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio3_xlmem': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio3_htc': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
            'brc:savio4_htc': {
                'tf_exec_time': (200, None, 0.1, 's'),
            },
        }

        self.num_gpus_per_node = 1
#        self.num_cpus_per_task = 4

        #self.perf_patterns = {
        #    'fit_evaluate_time': self.extract_fit_evaluate_time(),
        #}

    @sanity_function
    def check_output(self):
        return sn.assert_found(r'Time in seconds:\s+(?P<exec_time>\S+)', self.stdout)

    @performance_function('s')
    def tf_exec_time(self):
        return sn.extractsingle(r'Time in seconds:\s+(?P<exec_time>\S+)', self.stdout, 1, float)
