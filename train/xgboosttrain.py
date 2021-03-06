import glob
import xgboost as xgb
from PIL import Image
import cv2    
import random
import numpy as np
from scipy import ndimage as ndi
from sklearn.cross_validation import train_test_split  
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
from sklearn.decomposition import PCA 
from skimage import data
from skimage.util import img_as_float
from skimage.filters import gabor_kernel
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


random.seed(1313)
np.random.seed(13)
cnt = 0
hist_size = 40
data = np.empty((6000,hist_size*3+4))
label = []
feature_size = hist_size*3+5
param = {}
param['objective'] = 'binary:logistic'
param['eval_metric'] = 'auc'
param['max_depth'] = 8
param['alpha'] = 1 
param['gamma'] = 1
param['min_child_weight']=1.5
param['eta'] = 0.01
param['silent'] = 0
param['n_estimator'] = 50
param['verbose_eval'] = True
param['verbose'] = 1
num_round = 1000 
for filename in glob.glob("patch/out/*.bmp"):
    image = cv2.imread(filename)    
    B,G,R = cv2.split(image)
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    histB = np.transpose(cv2.calcHist([B], [0], None, [hist_size], [0.0,256.0])).flatten()
    histG = np.transpose(cv2.calcHist([G], [0], None, [hist_size], [0.0,256.0])).flatten()      
    histR = np.transpose(cv2.calcHist([R], [0], None, [hist_size], [0.0,256.0])).flatten()
    image_entro = est_entro_MLE(np.array(GrayImage).flatten())
    rawname = filename.split('-')
    rawname = rawname[0].split('/')
    label = np.append(label,int(rawname[1]))
    
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten()),image_entro[0]]),axis=0)
    cnt = cnt + 1
for filename in glob.glob("patch/test/*.bmp"):
    image = cv2.imread(filename)    
    B,G,R = cv2.split(image)
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    histB = np.transpose(cv2.calcHist([B], [0], None, [hist_size], [0.0,256.0])).flatten()
    histG = np.transpose(cv2.calcHist([G], [0], None, [hist_size], [0.0,256.0])).flatten()      
    histR = np.transpose(cv2.calcHist([R], [0], None, [hist_size], [0.0,256.0])).flatten()
    image_entro = est_entro_MLE(np.array(GrayImage).flatten())
    rawname = filename.split('-')
    rawname = rawname[0].split('/')
    label = np.append(label,int(rawname[1]))
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten()),image_entro[0]]),axis=0)
    cnt = cnt + 1
    '''
    if random.random() > 0.7:
        data_train[train_cnt,:] = np.append(np.concatenate((histB,histG,histR),axis=0),label)
        train_cnt = train_cnt + 1
    else:
        data_test[test_cnt,:] = np.append(np.concatenate((histB,histG,histR),axis=0),label)
        test_cnt = test_cnt + 1
    '''
data = data[:cnt,:]
pca=PCA(n_components=feature_size-1)
#print(data)
pca.fit(data)
newData=pca.transform(data)
joblib.dump(pca, 'xgboost.pca')
data_train = np.empty((5000,feature_size))
data_test = np.empty((4000,feature_size))
train_cnt = 0
test_cnt = 0
for i in range(cnt):
    if random.random() > 0.1:
        data_train[train_cnt,:] = np.append(newData[i,:],label[i])
        train_cnt = train_cnt + 1
    else:
        data_test[test_cnt,:] = np.append(newData[i,:],label[i])
        test_cnt = test_cnt + 1  
dtrain = xgb.DMatrix(data_train[:train_cnt,:-1],label = data_train[:train_cnt,-1])
dtest = xgb.DMatrix(data_test[:test_cnt,:-1],label = data_test[:test_cnt,-1])
watchlist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)
# make prediction
preds = bst.predict(dtest)
res = bst.eval(dtest)
false_positive_rate, true_positive_rate, thresholds = roc_curve(data_test[:test_cnt,-1],preds)
roc_auc = auc(false_positive_rate, true_positive_rate)
print(train_cnt,test_cnt)  

print(res)
np.save('falsepos.npy',false_positive_rate)
np.save('truepos.npy',true_positive_rate)
with open('roc_raw.txt', 'w') as f:
    for i in range(len(false_positive_rate)):
        f.write(str(false_positive_rate[i]) + ' '+ str(true_positive_rate[i]) + '\n')
bst.save_model('xgboost.model')
