#!/bin/sh

# Script to kill all python processes
#
# Michael Rosen
# mrrosen
# 16-10-2015

ps | grep python | grep -v grep | awk '{print $1}' | xargs kill