#!/bin/bash
#

dataTgt='./data/ config.py'
pycTgt='modules/__pycache__ __pycache__'

rm -rf ${dataTgt}
rm -rf ${pycTgt}

exit $?

