#!/bin/bash

# Check if any process is running on port 5000
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Process found on port 5000. Stopping..."
    kill $(lsof -ti :5000)
    echo "Process on port 5000 stopped."
else
    echo "No process found on port 5000."
fi

# Check if any process is running on port 5001
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "Process found on port 5001. Stopping..."
    kill $(lsof -ti :5001)
    echo "Process on port 5001 stopped."
else
    echo "No process found on port 5001."
fi
