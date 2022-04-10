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
   client, bucket = initialize_cos_configuration()
  ```
   | Parameter | Description |
   | --- | ----------- |
   | client | cos client instance |
   | bucket | cos bucket name from where data is fetched |
</details>  

<details>
  <summary>Initialize IBM cloudant configuration </summary>
  This method parse the config file which includes all the realted credentials and details needed for creating Cloudant Client.
  
  ##### Response
  ```
   cloudant, db, processed_db = initialize_cloudant_configuration()
  ``` 
   | Parameter | Description |
   | --- | ----------- |
   | cloudant_client | Cloudant instance - allows access to Cloudant DB |
   | db | database name from where documents needs to be queried |
   | processed_db | database name where processed data documents need to be stored |
</details>  

<details>
  <summary>Read Image From COS</summary>
   Convert the downloaded streaming body objects to numpy ndarray <br>
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | client | cos client instance |
   | bucket | cos bucket name from where data is fetched |
   | file | file name to fetch |
  
  ##### Response
  ```
   image = read_image(cos, bucket, file)
  ```
  Returns 
   | Parameter | Description |
   | --- | ----------- |
   | image | file fetched from cos bucket in a numpy array  |

</details>  

<details>
  <summary>Download data from IBM Cloud Object storage</summary>
    Download the data from cos bucket as per the request
    
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | limit | specify the number of returned documents to limit the result to. Possible values: value ≥ 0 |
   | cloudant | cloudant instance to connect to cloudant |
   | cloudant_db | databse name from which documents need to be fetched |
   | processed | specify whether to fetch the processed data, default: False |
  
  ##### Response
  ```
   if processed:
      return metadata, image_data, labels, annotations
   return metadata, image_data, labels
  ```
   | Parameter | Description |
   | --- | ----------- |
   | metadata | List of metadata files |
   | image_data | List of images (numpy array) |
   | labels | List of label for each image |
   | annotations | Annotation details for each image object |
</details>  


### Data Preprocessing
Source Files:
- [Data Preprocessing](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/data_preprocessing.py)
- [Data Annotation](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/data_annotation.py)

#### Methods
<details>
  <summary>Resize image by specifying width, height, and interpolation method</summary>
  Resize the input image with the given parameters.
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | image | Input image file |
   | width | Output image width |
   | height | Output image height |
   | interpolation | Opencv Interpolation Method |
  
  ##### Response
  ```
   resized_image = resize(image, width, height, interpolation_method)
  ```
   | Parameter | Description |
   | --- | ----------- |
   | resized_image | Resized image |
</details>  

<details>
  <summary>Get Resized Data</summary>
  Resize the input data as per the specification
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | width | Output image width |
   | height | Output image height |
   | interpolation_method | Opencv Interpolation Method |
  
  ##### Response
  ```
   image_resize = ImageResize(width, height, interpolation_method)
   metadata, resized_data, labels = image_resize.get_resized_data()
  ```
   | Parameter | Description |
   | --- | ----------- |
   | metadata | List of metadata files |
   | resized_data | List of resized images (numpy array) |
   | labels | List of label for each image |
</details>  

<details>
  <summary>Find Contour in an Image</summary>
  This method finds all the contours in an input image based on the input method. It takes advantage of opencv methods to remove noise, detect edges, perform adaptive thresholding, and to detect contours.
     
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | image | Input image |
   | method | method through which contour should be detected. 
              Possible values - adaptive thresholding(0), edge detection (1);
              Default - 0 |
  
  ##### Response
  ```
   contours = find_contours(image, 0)
  ```
   | Parameter | Description |
   | --- | ----------- |
   | contours | detected contours |
</details>  

 <details>
  <summary>Draw bounding rectangle on an object in an image </summary>
  Finds the coordinates of the rectangle which contains the object in a given contour and draws the rectangle on an input image.
     
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | contours | detected contours of an image|
   | image | Input image |
   | method | method through which contour should be detected. 
              Possible values - adaptive thresholding(0), edge detection (1);
              Default - 0 |
  
  ##### Response
  ```
   drawn_image, coordinates = draw_bounding_rectangle(contours, image, 0)
  ```
   | Parameter | Description |
   | --- | ----------- |
   | drawn_image | Image with rectangle on the object |
   | coordinates | Coordinates of the drawn rectangle in the form <x, y, w, h> |
    
</details>  
    
   <details>
   <summary>Create the annotation deatils and upload the processed data</summary>
   Generate the metadata for processed image data and upload the new metadata in cloudant database with processed meta files.


   ##### Request

   | Parameter | Description |
   | --- | ----------- |
   | metadata | metadata file of an image |
   | image | Processed image file |
   | label | Label of processed image |
   | coordinates | Annotation coordinaes of image |

   ##### Response
   ```
    upload_processed_image(metadata, image, label, coordinates)
   ```
   </details>  
    
   <details>
   <summary>Get annotated data</summary>
   Get the annotated processed data

   ##### Response
   ```
    annotation = Annotation()
    annotated_data = annotation.get_annotated_data()
   ```
   </details>  


### Feature Engineering

### Algorithm Selection

### Training Infrastructure

### Model Deployment

### Continuous Improvement
