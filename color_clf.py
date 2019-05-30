import cv2
import glob
import numpy as np
from test_color import color_center

from sklearn.linear_model import LogisticRegression as logistic
import joblib

import datetime


color_liz = ['green', 'yellow', 'brown']

def learn():

    X = []
    Y = []

    imgs = glob.glob("mango_color/b*.png")
    for fname in imgs:
        img = cv2.imread(fname)
        c_color = color_center(img)
        print(fname, c_color)
        X.append(c_color)
        Y.append(2)

    imgs = glob.glob("mango_color/y*.png")
    for fname in imgs:
        img = cv2.imread(fname)
        c_color = color_center(img)
        print(fname, c_color)
        X.append(c_color)
        Y.append(1)

    imgs = glob.glob("mango_color/g*.png")
    for fname in imgs:
        img = cv2.imread(fname)
        c_color = color_center(img)
        print(fname, c_color)
        X.append(c_color)
        Y.append(0)

    X = np.array(X)
    Y = np.array(Y)

    clf = logistic(solver='lbfgs', multi_class='multinomial', max_iter=1000)
    clf.fit(X, Y)

    return clf

def classify(clf, color):
    return color_liz[clf.predict(color)[0]]

def load(clf_path):
    return joblib.load(clf_path)

def save(clf_path, clf):
    joblib.dump(clf, clf_path)
    return

if __name__ == '__main__':
    clf = learn()
    clf_path = 'color_clf.joblib'
    save(clf_path, clf)
    print("save classifier at", clf_path)

    test_img = cv2.imread("mango_color/y0.png")
    test_c_color = color_center(test_img).reshape(1, -1)
    pred_color = color_liz[clf.predict(test_c_color)[0]]

    cv2.imshow('test', test_img)
    print("predicted color of", test_c_color, "=", pred_color)
    cv2.waitKey(0)