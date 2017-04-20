import glob
import xgboost as xgb
from PIL import Image
import cv2    
import random
import numpy as np
from scipy import ndimage as ndi
from sklearn.cross_validation import train_test_split  
from sklearn.externals import joblib
from sklearn.metrics import roc_curve, auc
from sklearn.decomposition import PCA 
from skimage import data
from skimage.util import img_as_float
from skimage.filters import gabor_kernel
import matplotlib.pyplot as plt
def est_entro_MLE(samp):
    """Maximum likelihood estimate of Shannon entropy (in bits) of the input
    sample

    This function returns a scalar MLE of the entropy of samp when samp is a
    vector, or returns a (row-) vector consisting of the MLE of the entropy
    of each column of samp when samp is a matrix.

    Input:
    ----- samp: a vector or matrix which can only contain integers. The input
                data type can be any interger classes such as uint8/int8/
                uint16/int16/uint32/int32/uint64/int64, or floating-point
                such as single/double.
    Output:
    ----- est: the entropy (in bits) of the input vector or that of each
               column of the input matrix. The output data type is double.
    """
    samp = np.asarray(samp)
    samp = samp.astype(np.float)
    samp = formalize_sample(samp)
    [n, wid] = samp.shape
    n = float(n)

    f = fingerprint(samp)
    prob = np.arange(1, f.shape[0] + 1) / n
    prob_mat = - prob * np.log2(prob)
    return prob_mat.dot(f)

def formalize_sample(samp):
    samp = np.array(samp)
    if np.any(samp != np.fix(samp)):
        raise ValueError('Input sample must only contain integers.')
    if samp.ndim == 1 or samp.ndim == 2 and samp.shape[0] == 1:
        samp = samp.reshape((samp.size, 1))
    return samp

def fingerprint(samp):
    """A memory-efficient algorithm for computing fingerprint when wid is
    large, e.g., wid = 100
    """
    wid = samp.shape[1]

    d = np.r_[
        np.full((1, wid), True, dtype=bool),
        np.diff(np.sort(samp, axis=0), 1, 0) != 0,
        np.full((1, wid), True, dtype=bool)
    ]

    f_col = []
    f_max = 0

    for k in range(wid):
        a = np.diff(np.flatnonzero(d[:, k]))
        a_max = a.max()
        hist, _ = np.histogram(a, bins=a_max, range=(1, a_max + 1))
        f_col.append(hist)
        if a_max > f_max:
            f_max = a_max

    return np.array([np.r_[col, [0] * (f_max - len(col))] for col in f_col]).T

cnt = 0
hist_size = 40
data = np.empty((6000,hist_size*3+4))
feature_size = hist_size*3+5
data_name = np.array([])
for filename in glob.glob("segmented/*.bmp"):
    image = cv2.imread(filename)    
    B,G,R = cv2.split(image)
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    histB = np.transpose(cv2.calcHist([B], [0], None, [hist_size], [0.0,256.0])).flatten()
    histG = np.transpose(cv2.calcHist([G], [0], None, [hist_size], [0.0,256.0])).flatten()      
    histR = np.transpose(cv2.calcHist([R], [0], None, [hist_size], [0.0,256.0])).flatten()
    image_entro = est_entro_MLE(np.array(GrayImage).flatten())
    rawname = filename.split('/')
    data_name = np.append(data_name,rawname[1])
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten()),image_entro[0]]),axis=0)
    cnt = cnt + 1

data = data[:cnt,:]
pca = joblib.load("model/xgboost.pca")
newData=pca.transform(data)
dtest = xgb.DMatrix(newData)
bst = xgb.Booster() #init model
bst.load_model("model/xgboost.model") # load data
preds = bst.predict(dtest)
with open('predicted.txt', 'w') as f:
    for i in range(preds.shape[0]):
        f.write(data_name[i] + ' '+ str(int(preds[i]>0.5)) + '\n')
