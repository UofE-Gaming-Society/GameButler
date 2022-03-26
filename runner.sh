#!/bin/sh 


git_update() 
{
    git pull
}

start_bot() 
{
    python3 botrunner.py # edit this if /bin/python == python3
    if [($? -eq 2) == 0]
    then
        start_bot()
    fi
    if [($? -eq 6) == 0]
    then 
        git_update()
        start_bot()
    fi
}

git_update()
start_bot()

