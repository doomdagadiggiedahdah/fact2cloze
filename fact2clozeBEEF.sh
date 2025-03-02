#!/bin/bash

PROGRAM_DIR="/home/mat/Documents/ProgramExperiments/fact2cloze"
LOG_FILE="$PROGRAM_DIR/log.log"

source $PROGRAM_DIR/f2cenv/bin/activate
python $PROGRAM_DIR/beef.py
deactivate
