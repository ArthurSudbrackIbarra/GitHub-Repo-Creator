#!/bin/bash

COMMAND=$1
PARAMETER=$2

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

if [ -z "$COMMAND" ]; then
    echo
    echo "No command passed."
    echo
    exit
fi

if [ -z "$PARAMETER" ]; then
    if [ $COMMAND = "choose" ]; then
        python $SCRIPT_DIR/.program-files/main.py $COMMAND
    fi
else
    if [ $COMMAND = "create" ] || [ $COMMAND = "save" ]; then
        FILE_PATH=$PWD/$PARAMETER
        python $SCRIPT_DIR/.program-files/main.py $COMMAND $FILE_PATH
    fi
    if [ $COMMAND = "authenticate" ] || [ $COMMAND = "delete" ]; then
        python $SCRIPT_DIR/.program-files/main.py $COMMAND $PARAMETER
    fi
fi
