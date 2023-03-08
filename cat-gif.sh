#!/bin/bash

# check that a name argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <name>"
  exit 1
fi

# set the name of the PNG files
name="$1"

# set the delay time (in 1/100th of a second) between frames
delay=10

# find all PNG files matching the pattern "<name>-<index>.png"
files=(images/arnold_cat-"$name"-*.png)

# set max size of the images
max_size=256

# loop through the files and rescale them to a maximum size of 512 pixels
for file in "${files[@]}"; do
  # determine the original size of the file
  size=$(identify -format "%wx%h" "$file")
  
  # if the width or height is larger than 512 pixels, rescale the image
  if [[ $size =~ ([0-9]+)x([0-9]+) ]]; then
    width=${BASH_REMATCH[1]}
    height=${BASH_REMATCH[2]}
    if (( width > max_size || height > max_size )); then
      convert "$file" -resize "${max_size}x${max_size}>" "$file"
    fi
  fi
  # add an index in the corner of the image
  # convert "$file" -gravity northeast -pointsize 12 -fill white -annotate -10+10 "%[scene]" "$file"
done

# create the GIF using ImageMagick's convert command
convert -delay "$delay" "${files[@]}" -loop 0 -gravity northeast -pointsize 12 -fill white -annotate +10+10 "%[scene]" "${name}.gif"

# print a message indicating that the conversion is complete
echo "Conversion complete: ${name}.gif"
