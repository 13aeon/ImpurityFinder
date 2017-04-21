import glob
import numpy as np
import cv2

imsize = 256

def makePosNeg():

    # count num
    pos_num = 0
    neg_num = 0
    for filename in glob.glob("out/*.bmp"):
        rawname = filename.split('-')
	rawname = rawname[0].split('/')
	label = int(rawname[1])
	if label:
	    pos_num += 1
	else:
	    neg_num += 1
    for filename in glob.glob("test/*.bmp"):
        rawname = filename.split('-')
	rawname = rawname[0].split('/')
	label = int(rawname[1])
	if label:
	    pos_num += 1
	else:
	    neg_num += 1
    # print pos_num
    # print neg_num

    # store image
    pos_image = np.empty((pos_num, imsize, imsize, 3))
    neg_image = np.empty((neg_num, imsize, imsize, 3))
    pos_cnt = 0
    neg_cnt = 0
    for filename in glob.glob("out/*.bmp"):
        tmp_image = cv2.imread(filename) 
	tmp_image = cv2.resize(tmp_image, (imsize, imsize))
        rawname = filename.split('-')
	rawname = rawname[0].split('/')
	label = int(rawname[1])
	if label:
	    pos_image[pos_cnt,:,:,:] = tmp_image
	    pos_cnt += 1
	else:
	    neg_image[neg_cnt,:,:,:] = tmp_image
	    neg_cnt += 1
    for filename in glob.glob("test/*.bmp"):
        tmp_image = cv2.imread(filename) 
	tmp_image = cv2.resize(tmp_image, (imsize, imsize))
        rawname = filename.split('-')
	rawname = rawname[0].split('/')
	label = int(rawname[1])
	if label:
	    pos_image[pos_cnt,:,:,:] = tmp_image
	    pos_cnt += 1
	else:
	    neg_image[neg_cnt,:,:,:] = tmp_image
	    neg_cnt += 1
    np.save('pos_image.npy', pos_image)
    np.save('neg_image.npy', neg_image)

def loadSet():
    pos_image = np.load('pos_image.npy')
    neg_image = np.load('neg_image.npy')
    return pos_image, neg_image

class Loader(object):

    def __init__(self, batch_size=1):
        self.tmp = 0 
        self.batch_size = batch_size
        print('Data Loader initializing ...')
        
        pos_image, neg_image = loadSet()
        self.image = neg_image
        self.count = self.image.shape[0]
        self.label = np.zeros(self.count)

        self.steps_per_epoch = int(np.ceil(np.float(self.count) / np.float(batch_size)))

    def next_batch(self):
        if self.tmp + self.batch_size < self.count:
            x_batch = self.image[self.tmp:self.tmp + self.batch_size]
            y_batch = self.label[self.tmp:self.tmp + self.batch_size]
            self.tmp += self.batch_size
        else:
            x_batch = self.image[self.tmp:]
            y_batch = self.label[self.tmp:]
            self.tmp = 0 
        return (x_batch / 255.)*2-1, y_batch

class PosLoader(object):

    def __init__(self, batch_size=1):
        self.tmp = 0 
        self.batch_size = batch_size
        print('Data Loader initializing ...')
        
        pos_image, neg_image = loadSet()
        self.image = pos_image
        self.count = self.image.shape[0]
        self.label = np.zeros(self.count)

        self.steps_per_epoch = int(np.ceil(np.float(self.count) / np.float(batch_size)))

    def next_batch(self):
        if self.tmp + self.batch_size < self.count:
            x_batch = self.image[self.tmp:self.tmp + self.batch_size]
            y_batch = self.label[self.tmp:self.tmp + self.batch_size]
            self.tmp += self.batch_size
        else:
            x_batch = self.image[self.tmp:]
            y_batch = self.label[self.tmp:]
            self.tmp = 0 
        return (x_batch / 255.)*2-1, y_batch

