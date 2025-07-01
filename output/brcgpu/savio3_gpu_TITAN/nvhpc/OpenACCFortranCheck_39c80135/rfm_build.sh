#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

module load nvhpc
nvfortran -acc=gpu -cuda -Minfo=accel -gpu=cc70,cc75,cc86,cc90 vecAdd_openacc_nompi.f90 -o ./OpenACCFortranCheck
