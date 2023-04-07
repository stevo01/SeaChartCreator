#!/bin/bash

# set -x

STOP_CONT="no"

# handler for term signal
function sighandler_TERM() {
    echo "signal SIGTERM received\n"

}


if [ "$#" -ne 1 ]; then
    echo "usage: <run>"
    echo "commands:"
    echo "    run: Runs openssh server"
    exit 1
fi

if [ "$1" = "run" ]; then
    # add handler for signal SIHTERM
    trap 'sighandler_TERM' 15

    cd /SeaChartCreator

    echo "wait for terminate signal"
    while [  "$STOP_CONT" = "no"  ] ; do
      sleep 1
    done

    exit 0
fi

echo "invalid command"
exit 1
