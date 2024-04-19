#!/bin/bash

# Navigate to the /usr/local/bin directory
cd /usr/local/bin

# Create a directory for FFMPEG if it doesn't already exist
mkdir -p ffmpeg
cd ffmpeg

# Download the latest FFMPEG static build
# Note: Adjust the link below if a different version is needed
wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz

# Extract the downloaded archive
tar -xJf ffmpeg-git-amd64-static.tar.xz

# Move into the directory containing the FFMPEG binary
# The directory name inside the tar may vary, adjust as needed
cd ffmpeg-git-*-amd64-static

# Optional: Remove the downloaded archive to save space
rm ../ffmpeg-git-amd64-static.tar.xz

# Check the installed version of FFMPEG
./ffmpeg -version

# Create a symlink to allow running FFMPEG from any location
ln -s "$(pwd)/ffmpeg" /usr/bin/ffmpeg

echo "FFMPEG installation is complete. You can now use ffmpeg from anywhere."
