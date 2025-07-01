<<<<<<< HEAD
=======
# Savio Reframe Tests

## Requirement
* Requires `reframe >= 4.7.3` as we use custom location for cpu topology files

## Structure
* `config` consists of cluster configurations
* `checks` consists of reframe tests (most of them adapted for the lawrencium cluster from ETH-CSCS tests)
* `.gitlab-ci.yml` implements the CI using gitlab runner which runs on a login node and listens to changes to this repository.

## Examples of running tests manually

### Compilers HelloWorld Tests
``` bash
reframe -C config/lawrencium.py --system=lrc:lr6 -c checks/prgenv/compilers_helloworld.py -r
```
will run the tests of compiling and running hello world C/C++/Fortran programs. The `-r` at the end instructs reframe to tun these tests.

### Running all available tests in a folder
``` bash
reframe -C config/lawrencium.py --system=lrc:lr6 -c checks/prgenv/ -r -R
```
The `-R` command line argument recursively searches for all available tests in the specified folder.

### Running tests on es1
``` bash
reframe -C config/lrcgpu.py -c checks/apps/vasp/ --system=lrcgpu:es1H100 -r -R
```

## References
Several of the tests have been adapted from:
* https://github.com/eth-cscs/cscs-reframe-tests/tree/main/checks
* https://github.com/fasrc/reframe-fasrc/tree/main

>>>>>>> 62b4ff2 (Initial commit)
