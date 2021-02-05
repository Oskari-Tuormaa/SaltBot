#!/bin/bash

# /-/-/-/-/-/-/-/-/-/-
#
# This script starts the bot,
# and checks for updates on git
# at each time interval specified.
#
# The script will automatically
# pull, restart the server and
# normalize memes if new commits
# are added.
#
# /-/-/-/-/-/-/-/-/-/-

# Kill background processes on exit
trap "kill 0" EXIT

# Set working directory
cd SaltBot

# Function for starting server and saving PID
START_SERVER() {
	# Start server
	python3 main.py &

	# Get server PID
	SERVER_PID=$(ps aux |
		grep "python3 main.py" |
		grep -oP "^.*?\K\d+" |
		head -1)
}

CHECK_NORMALIZE_MEMES() {
	if [[ -n "$(diff -q sound_bytes/memes sound_bytes/memes_raw | grep 'Only in')" ]]; then
		rm sound_bytes/memes/*.mp3
		bash sound_bytes/normalize_memes.sh
	fi
}

# Check normalize memes
# CHECK_NORMALIZE_MEMES

# Initial startup of server
START_SERVER


while sleep $1; do
	# Pull repo, and set PULLED to reflect whether we pulled or not
	[[ -z "$(git pull | grep 'up to date')" ]] && PULLED=1 || PULLED=0

	if [[ PULLED -eq 1 ]]; then
		# Kill server
		kill $SERVER_PID

		# Normalize memes
		# CHECK_NORMALIZE_MEMES

		# Start server again
		START_SERVER
	fi
done

wait
