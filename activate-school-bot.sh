#! /bin/bash

echo "Program Start"

source env/bin/activate
python3 transcriber.py &
pid1=$!
python3 recorder.py &
pid2=$!

echo "transcriber.py PID: $pid1"
echo "recorder.py PID: $pid2"

echo $pid1 > pids.txt
echo $pid2 >> pids.txt