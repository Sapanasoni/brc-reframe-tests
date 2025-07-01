# Adapted from reframe example
import os
username = os.environ['USER']
configdir = os.path.dirname(os.path.realpath(__file__))

from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher

# need this for running srun with --mpi=pmi2
@register_launcher('srunpmi2')
class Srun2Launcher(JobLauncher):
    def __init__(self):
        self.options = []
        self.use_cpus_per_task = True

    def command(self, job):
        ret = ['srun', '--mpi=pmi2']
        if self.use_cpus_per_task and job.num_cpus_per_task:
            ret.append(f'--cpus-per-task={job.num_cpus_per_task}')

        return ret        

site_configuration = {
    'general': [
        {
            'topology_prefix': configdir+"/topology",
        }
    ],
    'systems': [
        {
            'name': 'brc',
            'descr': 'Savio Cluster',
            'hostnames': ['.*'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'savio2',
                    'descr': 'rocky8 savio2',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio2', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi','intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio2_bigmem',
                    'descr': '4,n0[096-099].savio1,Intel Xeon E5-2670 v2,20,512 GB,FDR',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio2_bigmem', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi','intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio2_htc',
                    'descr': 'rocky8 savio2_htc',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio2_htc', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi','intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio2_knl',
                    'descr': 'rocky8 savio2_knl',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio2_knl', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi', 'intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
                {   
                    'name': 'savio3',
                    'descr': 'rocky8 savio3',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi', 'intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio3_bigmem',
                    'descr': 'rocky8 savio3_bigmem',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_bigmem', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi', 'intel', 'intel-mpi'],
                    'max_jobs': 10,
                },                                            
                {
                    'name': 'savio3_htc',
                    'descr': 'rocky8 savio3_htc',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_bigmem', '--account=ac_scsguest', '--qos=savio_debug'],
                    'environs': ['builtin', 'gcc', 'gcc-mpi', 'intel', 'intel-mpi'],
                    'max_jobs': 10,
                },
            ],
        },
        {
            'name': 'brcgpu',
            'descr': 'Savio Cluster',
            'hostnames': ['.*'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'savio4_gpu_L40',
                    'descr': 'savio4_gpu rocky8 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio4_gpu',
                               '--account=ac_scsguest',
                               '--qos=savio_lowprio',
                               '--mincpus=8',
                               ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:L40:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                        }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio4_gpu_A5000',
                    'descr': 'savio4 rocky8 nodes A5000',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio4_gpu',
                               '--account=ac_scsguest',
                               '--qos=a5k_gpu4_normal',
                               '--mincpus=4',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:A5000:{num_gpus_per_node}',
                                        '--cpus-per-task=4']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio3_gpu_TITAN',
                    'descr': 'savio3 rocky8 nodes TITAN',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_gpu',
                               '--account=ac_scsguest',
                               '--qos=savio_debug',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:TITAN:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio3_gpu_A40',
                    'descr': 'savio3  A40 GPU partition',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_gpu',
                               '--account=ac_scsguest',
                               '--qos=savio_debug',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:A40:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio3_gpu_V100',
                    'descr': 'savio3 V100 GPU partition',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_gpu',
                               '--account=ac_scsguest',
                               '--qos=savio_debug',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:V100:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },
                {
                    'name': 'savio3_gpu_GTX2080TI',
                    'descr': 'savio3 GTX2080TI GPU partition',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio3_gpu',
                               '--account=ac_scsguest',
                               '--qos=savio_debug',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:GTX2080TI:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                },           
                {
                    'name': 'savio2_gpu_1080TI',
                    'descr': 'savio2 1080TI GPU partition',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'time_limit': '40m',
                    'access': ['--partition=savio2_1080ti',
                               '--account=ac_scsguest',
                               '--qos=savio_debug',
                              ],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gres=gpu:GTX1080TI:{num_gpus_per_node}',
                                        '--cpus-per-task={num_cpus_per_task}']
                            }
                    ],
                    'environs': ['builtin_gpu', 'cuda', 'nvhpc'],
                    'max_jobs': 10,
                }

            ]
        }
    ],
    'environments': [
        {
            'name': 'nvhpc',
            'modules': ['nvhpc'],
            'cc': 'nvc',
            'cxx': 'nvc++',
            'ftn': 'nvfortran',
            'target_systems': ['brcgpu']
        },
        {
            'name': 'gcc-mpi',
            'modules': ['gcc', 'openmpi'],
            'cc': 'mpicc',
            'cxx': 'mpic++',
            'ftn': 'mpifort',
            'target_systems': ['brc']
        },
        {	
            'name': 'gcc',
            'modules': ['gcc'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['brc']
        },
        {
            'name': 'cuda',
            'modules': ['gcc','cuda'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['brcgpu'],
            #'env_vars': [['LD_LIBRARY_PATH','${CUDA_HOME}/lib64']],
        },
        {
            'name': 'intel',
            'modules': ['intel-oneapi-compilers'],
            'cc': 'icx',
            'cxx': 'icpx',
            'ftn': 'ifx',
            'target_systems': ['brc']
        },
        {
            'name': 'intel-mpi',
            'modules': ['intel-oneapi-compilers', 'intel-oneapi-mpi'],
            'cc': 'mpiicx',
            'cxx': 'mpiicpx',
            'ftn': 'mpiifx',
            'target_systems': ['brc'],
        },
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['brc']
        },
        {
            'name': 'builtin_gpu',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['brcgpu'],
        },
    ],
    'modes': [
        {
            'name': 'python311',
            'options': [
                '--exclude=mpi4py_intel',
            ]
        },
        {
           'name': 'anaconda3',
           'options': [
               '--map-module=python:anaconda3',
               '--exclude=mpi4py_builtin',
               '--exclude=mpi4py_intel',
           ]
        },
        {
            'name': 'python310',
            'options': [
                '--map-module=python:python/3.10',
                '--exclude=mpi4py_intel',
            ]
        },
        {
            'name': 'intelpython',
            'options': [
                '--map-module=python:intelpython',
                '--exclude=mpi4py_builtin',
                '--exclude=h5pyCheck',
            ]
        },
        {
            'name': 'brcgpu',
            'options': [
                '--system=brcgpu',
            ]
        },
        {
            'name': 'prgenvcuda',
            'options': [
                '--system=brcgpu',
                '--prgenv=cuda',
            ]
        },
        {
            'name': 'prgenvnvhpc',
            'options': [
                '--system=brcgpu',
                '--prgenv=nvhpc',
            ]
        },
    ],
}
