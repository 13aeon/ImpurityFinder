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
import matplotlib.pyplot as plt
random.seed(1313)
np.random.seed(13)
cnt = 0
hist_size = 40
data = np.empty((6000,hist_size*3+3))
label = []
feature_size = hist_size*3+4
param = {}
param['objective'] = 'binary:logistic'
param['eval_metric'] = 'auc'
param['max_depth'] = 7
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

    rawname = filename.split('-')
    rawname = rawname[0].split('/')
    label = np.append(label,int(rawname[1]))
    
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten())]),axis=0)
    cnt = cnt + 1
for filename in glob.glob("patch/test/*.bmp"):
    image = cv2.imread(filename)    
    B,G,R = cv2.split(image)
    GrayImage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    histB = np.transpose(cv2.calcHist([B], [0], None, [hist_size], [0.0,256.0])).flatten()
    histG = np.transpose(cv2.calcHist([G], [0], None, [hist_size], [0.0,256.0])).flatten()      
    histR = np.transpose(cv2.calcHist([R], [0], None, [hist_size], [0.0,256.0])).flatten()
    #print(GrayImage, kernels)  
    #g)abor_feats = np.transpose(compute_feats(GrayImage, kernels)).flatten() 
    #print(gabor_feats)
    rawname = filename.split('-')
    rawname = rawname[0].split('/')
    label = np.append(label,int(rawname[1]))
    data[cnt,:] = np.concatenate((histB,histG,histR,[np.cov(np.array(B).flatten()),np.cov(np.array(G).flatten()),np.cov(np.array(R).flatten())]),axis=0)
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

'''
plt.plot(false_positive_rate, true_positive_rate, 'b')
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.1,1.2])
plt.ylim([-0.1,1.2])
plt.savefig('roc.png')
'''
#print(preds)
print(res)
np.save('falsepos.npy',false_positive_rate)
np.save('truepos.npy',true_positive_rate)
bst.save_model('xgboost.model')
