#!/bin/bash 

echo running iperf-client

#TODO: add your code

while true; 
do
  iperf -c 10.0.0.1 -t 0.3 -b 10M -u
  sleep 0.8
done

