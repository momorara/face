#!/bin/bash

# /dev/video* を使用しているプロセスのPIDを取得
PIDS=$(lsof -t /dev/video*)

# PIDが存在する場合のみ kill する
if [ -n "$PIDS" ]; then
    echo "Killing processes: $PIDS"
    kill -9 $PIDS
else
    echo "No processes found using /dev/video*"
fi