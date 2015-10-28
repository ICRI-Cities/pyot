#!/bin/sh

# Autorun for iotnode.py

# Make sure dmesgs dont print to console
echo 4 > /proc/sys/kernel/printk

# Let everything start up
sleep 80

echo "-!- Beginning IoTNode tasks" > /dev/kmsg

# Run background tasks
cd /home/root/pyot
python main.py
