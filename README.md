# SyntheticText
Synthetic Text data generation for training OCR

# EMNIST: an extension of MNIST to handwritten letters
(MNIST is a collection of handwritten digits from 0-9.)
Image of size 28 X 28


## Code Requirements
scipy 
numpy
PIL (Image)
opencv (cv2)
pandas
os

## Description
This API can be used to generate words with random handwritting at character level, which is will stored along with a corresponding text file with bounding box information. This can be used to generated Synthetic data for OCR training.

![alt text](https://github.com/shubham99bisht/SyntheticText/blob/master/data/example_1.jpeg)

## Execution

To run the code type, 

`python create_data.py`

There are two Input Methods:
  1. word(required) numberOfImage gap
  2. -f csv_name (For reading line wise data from csv) 
  3. Q/q to quit

Here, numberOfImage is the count of different images required for the corresponding word. Each Image will have random font for each character. And, gap is an integer value (-5 to 5) which controls the pixel width between two characters in an image.

Each line of the csv file should be in the same format. User can skip numberOfImage and gap parameters, default values will be used for then. See Example.csv for sample input lines.


## Demo
  
![alt text](https://github.com/shubham99bisht/SyntheticText/blob/master/data/Hello_3.jpeg)

![alt text](https://github.com/shubham99bisht/SyntheticText/blob/master/data/World_1.jpeg)


## Citing EMNIST:
	arXiv:1702.05373
