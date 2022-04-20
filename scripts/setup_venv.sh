#!/bin/bash

SETUP_DIRECTORY=$HOME/Yolo

if [ -d "$SETUP_DIRECTORY" ]; then
 echo "Setup Directory: ${SETUP_DIRECTORY}"
else
  mkdir -p $SETUP_DIRECTORY
  echo "$SETUP_DIRECTORY directory is created"
fi

cd $SETUP_DIRECTORY || exit

# installing the python3-venv package
sudo apt install python3-venv -y
python3 -m venv yolo
source yolo/bin/activate