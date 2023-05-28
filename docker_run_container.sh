#!/bin/bash

if [ $1 == "jobs" ]; then
    echo "Running price jobs container...";
    docker run -t -d --network=host over-under-price-jobs/v1;
fi

if [ $1 == "run-interactive" ]; then
    echo "Running container interactively...";
    docker run -i -t over-under-price-jobs/v1:interactive sh;
fi