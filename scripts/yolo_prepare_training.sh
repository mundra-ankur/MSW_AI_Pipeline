#!/bin/bash

### Prepare Darknet Yolo with required data to be ready for training
SETUP_DIRECTORY=$HOME/Yolo
DARKNET_DIRECTORY=$SETUP_DIRECTORY/darknet
DARKNET_DATA_DIRECTORY=$DARKNET_DIRECTORY/data

if [ -d "$DARKNET_DATA_DIRECTORY" ]; then
 echo "Darknet Data Directory: ${DARKNET_DATA_DIRECTORY}"
else
  echo "$DARKNET_DATA_DIRECTORY directory doesn't exist!"
  exit 1
fi

cd $SETUP_DIRECTORY || exit

if [ -d "MSW_AI_Pipeline" ]; then
 cd MSW_AI_Pipeline || exit
else
  #Clone MSW AI Pipeline Repository
  git clone https://github.com/amundra02/MSW_AI_Pipeline.git
  cd MSW_AI_Pipeline || exit
  # Install the required packages
  pip install -r requirements.txt
fi

# Prepare Yolo for training
echo '-------------------------------------------------------------------------------'
echo "Do you wish to prepare training data for Yolo?
Before proceeding make sure you have config file in MSW_AI_Pipeline/config"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
          if [ ! -f config/ibm_config.ini ]; then
            echo "Config File not found!"
            echo "Please add the 'ibm_config.ini' in config directory and restart!"
            exit 1
          fi
          python3 src/prepare_yolo_training.py --darknet_data_directory $DARKNET_DATA_DIRECTORY --data_limit 30 --train_backup $SETUP_DIRECTORY/backup;
          break;;
        No ) exit 1;;
    esac
done


# Train Yolo
echo '-------------------------------------------------------------------------------'
echo "Do you wish to start training?"
select yn in "Yes" "No"; do
    case $yn in
        Yes )
          cd $DARKNET_DIRECTORY || exit
          #./darknet detector train <path to obj.data> <path to custom config> <pretrained_weights> -dont_show -map
          ./darknet detector train data/obj.data cfg/yolov4.cfg data/yolov4.conv.137 -dont_show -map;
          echo 'Training completed!'
          break;;
        No ) exit;;
    esac
done