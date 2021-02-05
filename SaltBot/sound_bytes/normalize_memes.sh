#!/bin/bash

# Script that normalizes all .mp3 files in /memes_raw/, and places normalized .mp3 files in /memes/

DIR="$(dirname "${0}")"

to_normalize=$@

[[ -z $to_normalize ]] &&
	to_normalize=$(ls memes_raw/*.mp3 | sed 's!.*/!!')

echo $to_normalize

for f in $to_normalize; do
	path=$DIR/memes_raw/$f
  norm_gain=$(ffmpeg -i $path -af 'volumedetect' -f null /dev/null 2>&1 | grep -P '(?<=max_volume: ).*(?= dB)' -o)
  norm_gain=$(echo $norm_gain | sed 's/-//g')
  echo -en $path "\t:\t" $norm_gain " dB\n"
  ffmpeg -i $path -filter:a "volume=${norm_gain}dB" ${path/#$DIR\/memes_raw\//$DIR\/memes\/} -y -loglevel 8
done
