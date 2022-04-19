#!/bin/bash

### Prepare Darknet Yolo with required data to be ready for training
SETUP_DIRECTORY=$HOME/Yolo
DARKNET_DATA_DIRECTORY=$SETUP_DIRECTORY/darknet/data

if [ -d "$DARKNET_DATA_DIRECTORY" ]; then
 echo "Darknet Data Directory: ${DARKNET_DATA_DIRECTORY}"
else
  echo "$DARKNET_DATA_DIRECTORY directory doesn't exist!"
  exit 1
fi

cd $SETUP_DIRECTORY || exit

#Clone MSW AI Pipeline Repository
git clone https://github.com/amundra02/MSW_AI_Pipeline.git
cd MSW_AI_Pipeline || exit
# Activate the virtual environment and install the required packages
pip install -r requirements.txt
python3 src/prepare_yolo_training.py --darknet_data_directory $DARKNET_DATA_DIRECTORY --data_limit 30 --train_backup $SETUP_DIRECTORY/backup