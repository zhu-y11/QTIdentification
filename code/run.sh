#!/bin/bash

DIR=`pwd -P`
export PYTHONPATH=$DIR

python $PYTHONPATH/preprocessing.py
python $PYTHONPATH/evaluation.py
