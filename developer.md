# Developer Guide

## Setup

Setup Python [virtual environment](https://docs.python.org/3/library/venv.html) with Python >= 3.7

1. Clone this repository
   ```bash
      git clone https://github.com/amundra02/ai_pipeline.git
   ```
2. Activate the virtual environment and install the required packages
   ```bash
      pip install -r requirements.txt
   ```
Peek inside the requirements file if you have everything already installed. Most of the dependencies are common libraries.

## Pipeline Buckets
- [Data Connections](#data-connections)
- [Data Preprocessing](#data-preprocessing)
- [Feature Engineering](#feature-engineering)
- [Algorithm Selection](#algorithm-selection)
- [Training Infrastructure](#training-infrastructure)
- [Model Deployment](#model-deployment)
- [Continuous Improvement](#continuous-improvement)

### Data Connections
Source Files
- [Initialize Configuration](https://github.com/amundra02/ai_pipeline/blob/main/src/initialize_configuration.py)
- [Download Data](https://github.com/amundra02/ai_pipeline/blob/main/src/download_data.py)
- [Upload Processed Data](https://github.com/amundra02/ai_pipeline/blob/main/src/upload_processed_data.py)
#### Methods
<details>
  <summary>Initialize IBM cos configuration </summary>
  This method parse the config file which includes all the realted credentials and details needed for creating COS Client.
  
  ##### Response
  ```
  configuration = Configuration()
  cos_client, bucket = configuration.initialize_cos_configuration()
  ```
  Returns 
  1. cos_client - ibm_boto3 Client
  2. bucket - str (from which data needs to be fetched)
</details>  

<details>
  <summary>Initialize IBM cloudant configuration </summary>
  This method parse the config file which includes all the realted credentials and details needed for creating Cloudant Client.
  
  ##### Response
  ```
   cloudant, db, processed_db = configuration.initialize_cloudant_configuration()
  ```
  Returns 
  1. cloudant_client - allows access to Cloudant DB
  2. db - database name from where documents needs to be queried
  2. processed db - database name where processed data documents need to be stored
</details>  

<details>
  <summary>Read Image From COS</summary>
  This method parse the config file which includes all the realted credentials and details needed for creating Cloudant Client.
  
  ##### Response
  ```
   cloudant, db, processed_db = configuration.initialize_cloudant_configuration()
  ```
  Returns 
  1. cloudant_client - allows access to Cloudant DB
  2. db - database name from where documents needs to be queried
  2. processed db - database name where processed data documents need to be stored
</details>  

### Data Preprocessing
<details>
  <summary></summary>
   ##### Request
    | Parameters |
    | :---       |
    |     |     |
</details>

### Feature Engineering

### Algorithm Selection

### Training Infrastructure

### Model Deployment

### Continuous Improvement
