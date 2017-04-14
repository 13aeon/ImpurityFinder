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
cnt = 0
hist_size = 40
data = np.empty((6000,hist_size*3+3))
feature_size = hist_size*3+4
data_name = np.array([])
for filename in glob.glob("segmented/*.bmp"):
    image = cv2.imread(filename)    
    B,G,R = cv2.split(image)
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    histB = np.transpose(cv2.calcHist([B], [0], None, [hist_size], [0.0,256.0])).flatten()
    histG = np.transpose(cv2.calcHist([G], [0], None, [hist_size], [0.0,256.0])).flatten()      
    histR = np.transpose(cv2.calcHist([R], [0], None, [hist_size], [0.0,256.0])).flatten()
    rawname = filename.split('/')
    data_name = np.append(data_name,rawname[1])
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten())]),axis=0)
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
