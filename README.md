# Savio Reframe Tests

## Requirement
* Requires `reframe >= 4.7.3` as we use custom location for cpu topology files
* Current version this repo is tested on is 4.8.1

## Structure
* `config` consists of cluster configurations
* `checks` consists of reframe tests (most of them adapted for the lawrencium cluster from ETH-CSCS tests)
* `.gitlab-ci.yml` implements the CI using gitlab runner which runs on a login node and listens to changes to this repository.

## Examples of running tests manually
clone this repo to either home or scratch
git clone 
cd brc-reframe-tests

### Compilers HelloWorld Tests for CPUs on specific partition
``` bash
reframe -C config/savio.py --system=brc:savio2 -c checks/prgenv/compilers_helloworld.py -r
```
will run the tests of compiling and running hello world C/C++/Fortran programs. The `-r` at the end instructs reframe to tun these tests.
**Note**: This tests work by default for the scs slurm account if you wish to use different account please setup the env variable RFM_ACC_NAME before the run or using export. For example 
``` bash
RFM_ACC_NAME=ac_scsguest reframe -C config/savio.py --system=brc:savio2 -c checks/prgenv/compilers_helloworld.py -r
```
### Compilers HelloWorld Tests for CPUs on all partition
``` bash
reframe -C config/savio.py --system=brc -c checks/prgenv/compilers_helloworld.py -r
```
One more example: running a osu benchmark performance test on all partitions
``` bash
reframe -C config/savio.py --system=brc -c checks/microbenchmarks/mpi/osu/osu_tests.py -r
```

# To run the above test during maintenance using a reservation
``` bash
reframe -C config/savio.py --system=brc -c checks/prgenv/compilers_helloworld.py --distribute=idle+maintenance+reserved -J reservation=2025-06-27-storage-work -r
```
**Note**: The flag --distribute=idle+maintenance+reserved will distribute jobs to all nodes on the partition which is good for nodes testing and one check might be good enough for this testing as shown above with helloworld. Other tests can be run without the flag.

### Running tests on brcgpu partitions pytorch test and cuda test
``` bash
reframe -C config/savio.py --system=brcgpu -c checks/ml/pytorch/cifar10perf.py  -r 
```
``` bash
reframe -C config/savio.py --system=brcgpu -c checks/prgenv/cuda/cuda_samples.py -r
```
## References
Several of the tests have been adapted from:
* https://github.com/eth-cscs/cscs-reframe-tests/tree/main/checks
* https://github.com/fasrc/reframe-fasrc/tree/main

>>>>>>> 62b4ff2 (Initial commit)
