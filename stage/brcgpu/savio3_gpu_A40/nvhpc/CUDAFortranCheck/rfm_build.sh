#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

module load nvhpc
nvfortran vecAdd_cuda.cuf -o ./CUDAFortranCheck
