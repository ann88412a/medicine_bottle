#!/bin/sh
session_name="MedicationTalk_DB"
cd $(dirname $0)
ProjectPath=$(pwd)
echo "ProjectPath: $ProjectPath"

tmux kill-session -t $session_name 2>/dev/null

if [ $(tmux ls 2>/dev/null | grep $session_name | wc -l) -eq "0" ]
    then
        tmux new-session -s $session_name -d;
        sleep 30
        tmux new-window -t $session_name -n DB 'python3 server.py'
    else
        echo "Can't kill previous tmux session..."
fi
