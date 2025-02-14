#!/bin/bash

# Start cron in the background
cron &

# Wait a bit to ensure cron starts
sleep 5

# Run the main script
python3 /app/main.py