#!/bin/bash 

git_update() 
{
    git pull
}

start_bot() 
{
    python3 botrunner.py # edit this if /bin/python == python3
    readonly EXIT_CODE=$?
    if [ EXIT_CODE -eq 2 ]
    then
        start_bot
    fi
    if [ EXIT_CODE -eq 6 ]
    then 
        git_update
        start_bot
    fi
}

git_update
start_bot

