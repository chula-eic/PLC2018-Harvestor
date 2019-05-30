import cv2
import glob
import numpy as np
from test_color import get_dominant_color

from sklearn.linear_model import LogisticRegression as logistic
import joblib

import datetime

X = []
Y = []

imgs = glob.glob("clf/mango_color/b*.png")
for fname in imgs:
    img = cv2.imread(fname)
    d_color = get_dominant_color(img)
    print(fname, d_color)
    X.append(d_color)
    Y.append(2)

imgs = glob.glob("clf/mango_color/y*.png")
for fname in imgs:
    img = cv2.imread(fname)
    d_color = get_dominant_color(img)
    print(fname, d_color)
    X.append(d_color)
    Y.append(1)

imgs = glob.glob("clf/mango_color/g*.png")
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