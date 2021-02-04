#!/bin/bash

while sleep $1
do
	git pull | grep "up to date" || bash SaltBot/sound_bytes/normalize_memes.sh
done
