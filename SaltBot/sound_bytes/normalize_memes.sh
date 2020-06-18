#!/bin/bash

# Script that normalizes all .mp3 files in /memes_raw/, and places normalized .mp3 files in /memes/

DIR="$(dirname "${0}")"

for f in $DIR/memes_raw/*.mp3
do
  norm_gain=$(ffmpeg -i $f -af 'volumedetect' -f null /dev/null 2>&1 | grep -P '(?<=max_volume: ).*(?= dB)' -o)
  norm_gain=$(echo $norm_gain | sed 's/-//g')
  echo -en $f "\t:\t" $norm_gain " dB\n"
  ffmpeg -i $f -filter:a "volume=${norm_gain}dB" ${f/#$DIR\/memes_raw\//$DIR\/memes\/} -y -loglevel 8
done
