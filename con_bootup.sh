#!/bin/bash

# Start cron in the background which runs the cronjob_access_token.py
cron &

# Wait a bit to ensure cron starts
sleep 5

# Run the main script
python3 /app/main.py