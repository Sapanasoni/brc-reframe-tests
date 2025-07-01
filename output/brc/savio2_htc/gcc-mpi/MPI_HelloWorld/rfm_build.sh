#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

module load gcc
module load openmpi
mpicc mpi_hello_world.c -o ./MPI_HelloWorld
