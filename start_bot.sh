#!/bin/bash

source venv/bin/activate
tmux new-session -d -s bot 'python main.py'
