#!/bin/bash 

git_update() 
{
    git pull
}

start_bot() 
{
    python3 botrunner.py # edit this if /bin/python == python3
    exit_code=$?
    echo exit_code
    if [ exit_code -eq 2 ]
    then
        start_bot
    fi
    if [ exit_code -eq 6 ]
    then 
        git_update
        start_bot
    fi
}

git_update
start_bot

