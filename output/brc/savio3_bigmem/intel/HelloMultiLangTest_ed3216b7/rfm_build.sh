#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

module load intel-oneapi-compilers
icx hello.c -o ./HelloMultiLangTest_0
