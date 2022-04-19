#!/bin/bash


### Darknet script
SETUP_DIRECTORY=$HOME/Yolo

if [ -d "$SETUP_DIRECTORY" ]; then
 echo "Setup Directory: ${SETUP_DIRECTORY}"
else
mkdir -p $SETUP_DIRECTORY
echo "$SETUP_DIRECTORY directory is created"
fi

cd $SETUP_DIRECTORY || exit

## Opencv Setup
#Install CMake
#sudo apt update && sudo apt upgrade -y
sudo apt install cmake -y
sudo apt-get install gcc g++ -y
cmake_version=$(cmake --version)
echo "${cmake_version}"

#To support python3
sudo apt-get install python3-dev python3-numpy -y

#GTK Support
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev -y
sudo apt-get install libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev -y
sudo apt-get install libgtk-3-dev -y

#Optional Dependencies
sudo apt-get install libpng-dev -y
sudo apt-get install libjpeg-dev -y
sudo apt-get install libopenexr-dev -y
sudo apt-get install libtiff-dev -y
sudo apt-get install libwebp-dev -y

# Clone opencv source
sudo apt-get install git -y
git clone https://github.com/opencv/opencv.git
cd opencv || exit
git -C opencv checkout 4.x

#Create a new "build" folder and navigate to it
mkdir -p build && cd build || exit

#Configuring and Installing
cmake ../
make -j4
sudo make install

echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib' >> ~/.bashrc
source ~/.bashrc


#Install Darknet
cd $SETUP_DIRECTORY || exit
git clone https://github.com/AlexeyAB/darknet
cd darknet || exit
mkdir -p build_release && cd build_release || exit
cmake ..
cmake --build . --target install --parallel 8
cd .. || exit
make