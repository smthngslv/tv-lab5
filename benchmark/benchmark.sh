#!/bin/bash

# CPU.
for threads in 2 10 100; do
  for i in {1..10}; do
    sysbench --threads=$threads --time=60 cpu --cpu-max-prime=64000 run
  done
done

# Multithreading.
for i in {1..10}; do
  sysbench --threads=64 threads --thread-yields=100 --thread-locks=2 run
done

# Multithread memory.
for threads in 2 10 100; do
  for i in {1..10}; do
    sysbench --threads=$threads --time=60 memory --memory-oper=write run
  done
done

# Memory.
for i in {1..10}; do
  sysbench memory --memory-block-size=1M --memory-total-size=10G run
done

# Disk.
sysbench fileio --file-total-size=150G prepare
for i in {1..10}; do
  sysbench fileio --file-total-size=150G --file-test-mode=rndrw  --time=120 --max-time=300 --max-requests=0 run
done
sysbench fileio --file-total-size=150G cleanup
