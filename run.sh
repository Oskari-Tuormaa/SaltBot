#!/bin/bash

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

# Initial startup of server
START_SERVER


while sleep $1; do
	# Pull repo, and set PULLED to reflect whether we pulled or not
	[[ -z "$(git pull | grep 'up to date')" ]] && PULLED=1 || PULLED=0

	if [[ PULLED == 1 ]]; then
		# Kill server
		kill $SERVER_PID

		# Normalize memes
		bash SaltBot/sound_bytes/normalize_memes.sh

		# Start server again
		START_SERVER
	fi
done

wait
