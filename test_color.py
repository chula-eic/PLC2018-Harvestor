import cv2
import numpy as np

from sklearn.cluster import KMeans
from collections import Counter

import datetime

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input
    returns the dominant color of the image as a list
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input
    >>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, 
                            interpolation = cv2.INTER_AREA)
    
    #reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)
    #subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)


def color_center(image, n = 10):

    h, w, cc = image.shape
    ch = int(h/2)
    cw = int(w/2)
    if n > ch : n = int(h/4)
    if n > cw : n = int(w/4)
    c_color = np.array([0, 0 ,0])
    count = 0
    for i in range(ch - n, ch + n + 1):
        for j in range(cw - n, cw + n + 1):
            color = image[i, j, :]
            c_color += color
            count += 1
    c_color = c_color / count

    return c_color


def read_test_data():

    img = cv2.imread('test_image/mango_y_c.png', 1)
    
    print('Original Dimensions : ',img.shape)
    
    scale_percent = 10 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (100, 100)
    # resize image
    resized_y = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    print('Resized Dimensions : ',resized_y.shape) 

    img = cv2.imread('test_image/mango_b_c.png', 1)
    
    print('Original Dimensions : ',img.shape)
    
    scale_percent = 10 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (100, 100)
    # resize image
    resized_b = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    print('Resized Dimensions : ',resized_b.shape) 

    return [resized_y, resized_b]

def get_color(image) :
    d_color = get_dominant_color(image, k=3)
    if d_color[0] > 175: return 'brown'
    else : return 'yellow'

if __name__ == '__main__':
    y, b = read_test_data()
    start = datetime.datetime.now()
    print(get_dominant_color(y))
    stop = datetime.datetime.now()
    print(stop - start)
    start = datetime.datetime.now()
    print(get_dominant_color(b))
    stop = datetime.datetime.now()
    print(stop - start)
