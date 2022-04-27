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
- [Cloud Helper](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/cloud_helper.py)
   - Parses the configuration [file](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/config/ibm_config_example.ini) and create the necessary resources to connect to cloud.
   - Create Cos Client, Cos Resource,and Clodant Client instance
   
- [Download Data](https://github.com/amundra02/ai_pipeline/blob/main/src/download_data.py)
- [Upload Data](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/upload_data.py)
#### Methods
<details>
  <summary>Get Cos Client Instance </summary>
   
  ##### Response
   
  ```
   client = get_cos_client()
  ```
   
   | Parameter | Description |
   | --- | ----------- |
   | client | cos client instance |
</details>  

<details>
  <summary>Get Cos resource Instance </summary>  
   
  ##### Response
   
  ```
   resource = get_cos_resource()
  ```
   
   | Parameter | Description |
   | --- | ----------- |
   | resource | cos resource instance |
</details>  

<details>
  <summary>Get cloudant instance and database to fetch data </summary>
   
  ##### Response
  ```
   cloudant, db = get_cloudant_client()
  ``` 
   | Parameter | Description |
   | --- | ----------- |
   | cloudant_client | Cloudant instance - allows access to Cloudant DB |
   | db | database name from where documents needs to be queried |
</details>  

<details>
  <summary>Get Cos Bucket to upload processed data</summary>  
   
  ##### Response
  ```
   bucket_name = get_upload_bucket()
  ```
   | Parameter | Description |
   | --- | ----------- |
   | bucket_name | Cos Bucket name |
</details>  

<details>
  <summary>Get clouant database name to upload processed metadata</summary>  
   
  ##### Response
  ```
   db_name = get_cloudant_processed_db()
  ```
   | Parameter | Description |
   | --- | ----------- |
   | db_name | Cloudant database name |
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
   | limit | specify the number of documents to limit the results to. Possible values: value ≥ 0 |
  
  ##### Response
  ```
   metadata, image_data, labels = get_data_ibm_cos(limit)
  ```
   | Parameter | Description |
   | --- | ----------- |
   | metadata | List of metadata files |
   | image_data | List of images (numpy array) |
   | labels | List of label for each image |
</details>  

<details>
  <summary>Download processed data from IBM Cloud Object storage</summary>
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | limit | specify the number of documents to limit the results to. Possible values: value ≥ 0 |
  
  ##### Response
  ```
   metadata, image_data, labels, annotations = get_data_ibm_cos(limit)
  ```
   | Parameter | Description |
   | --- | ----------- |
   | metadata | List of metadata files |
   | image_data | List of images (numpy array) |
   | labels | List of label for each image |
   | annotations | Annotation details for each image object |
</details>  

<details>
   <summary>Create and upload metadata document for processed image file to Cloudant database</summary>
  
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | metadata | metadata of image to be uploaded |
   | annotation_meta | Annotation details for image object |
   
   
  ##### Response
  ```
   response = upload_metadata(metadata, annotation_meta)
  ```
   
   | Parameter | Description |
   | --- | ----------- |
   | response | api response of post call |
</details>

<details>
  <summary>Write Image to COS</summary>
   Convert the numpy ndarray image data into Image object and store the data in cos bucket <br>
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | client | cos client instance |
   | bucket | cos bucket name where data is uploaded |
   | file | file name to upload |
   | image | image data to be uploaded |
  
  ##### Response
  ```
      write_image_cos(cos, bucket, file, image)
  ```
</details> 


### Data Preprocessing
Source Files:
- [Data Preprocessing](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/data_preprocessing.py)
  - Data resizing: Resized data by specifying the width and height. [OpenCv Method](https://docs.opencv.org/4.5.5/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d)
- [Data Annotation](https://github.com/amundra02/MSW_AI_Pipeline/blob/main/src/data_annotation.py)
  - Bounding Boxes: bounding box for images with singular object.
  - Methods: [Adaptive thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html), [Canny edge detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html), [Contour detection](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a)

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
   | method |contour detection method. Possible values - adaptive thresholding(0), edge detection (1); Default - 0 |
  
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
   
  Finds the coordinates of the rectangle which contains the object in a given contour and draws the [rectangle](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga103fcbda2f540f3ef1c042d6a9b35ac7) on an input image.
     
   
   ##### Request
   
   | Parameter | Description |
   | --- | ----------- |
   | contours | detected contours of an image|
   | image | Input image |
   | method | contour detection method. Possible values - adaptive thresholding(0), edge detection (1); Default - 0 |
  
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
