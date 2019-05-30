import cv2
import glob
import numpy as np

from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as logistic
from collections import Counter
import joblib

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


X = []
Y = []

imgs = glob.glob("mango_color/b*.png")
for fname in imgs:
    img = cv2.imread(fname)
    d_color = get_dominant_color(img)
    print(fname, d_color)
    X.append(d_color)
    Y.append(2)

imgs = glob.glob("mango_color/y*.png")
for fname in imgs:
    img = cv2.imread(fname)
    d_color = get_dominant_color(img)
    print(fname, d_color)
    X.append(d_color)
    Y.append(1)

imgs = glob.glob("mango_color/g*.png")
for fname in imgs:
    img = cv2.imread(fname)
    d_color = get_dominant_color(img)
    print(fname, d_color)
    X.append(d_color)
    Y.append(0)

X = np.array(X)
Y = np.array(Y)

clf = logistic(solver='lbfgs', multi_class='multinomial')
clf.fit(X, Y)
clf_path = 'color_clf.joblib'
joblib.dump(clf, clf_path)
print("save classifier at", clf_path)

test_img = cv2.imread("mango_color/y0.png")
test_d_color = get_dominant_color(test_img)
pred_color = clf.predict(test_d_color)

cv2.imshow(test_img)
print("predicted color of", test_d_color, "=", pred_color)
cv2.waitKey(0)