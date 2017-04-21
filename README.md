# ImpurityFinder

Software implementation to detect impurity in tabacco, with 2 different methods (color histogram + SVM or XGBoost).

Author:
Banghua Zhu, 13aeon.v01d@gmail.com

Liren Chen, clr14@mails.tsinghua.edu.cn

Jinhui Song, sjh14@mails.tsinghua.edu.cn

## Introduction 

ImpurityFinder is a image processing algorithms based solution for detecting impurity in tabacco. This is one of the projects for course Statistical Signal Processing in Tsinghua University.

Please notice that in order to run our algorithm, you only need to download the test folder. The train folder might be large because of the segmented images. 

## Pipeline and Details

Here we provide two packages of ImpurityFinder. In training folder, we provide all the source code for training. And in test folder, our trained classifier is provided to take a tabacco image as input, and give a processed image as output.

### Dependencies

- MATLAB R2015b (May also run on other versions, but only MATLAB R2015b is tested.)
- Python 2.7
- OpenCV lib for Python (Homepage: http://opencv.org/ Tutorial for installation: http://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html)


The following python packages are necessary:
- numpy
- scipy
- sklearn
- skimage
- matplotlib
- xgboost

It may be easy for one to get the first 5 packages installed. For xgboost, please see https://www.ibm.com/developerworks/community/blogs/jfp/entry/Installing_XGBoost_For_Anaconda_on_Windows?lang=zh and the source code is on https://github.com/dmlc/xgboost)


### Training part

In this part, we use `Segment.m` to segment the image into patches of size 250×250, label them 1 if they're in a bounding box of certain colors, and 0 otherwise, and save all the segmented pieces into patch/out/ (or test) folder.

Then one of `xgboosttrain.py`, `dnntrain.py`, `svmtrain.m` runs and saves the trained model into model folder. `rocplot.py` is used to plot the ROC curve.

### Testing part

In this part, we use the trained model from Training part to test on certain images. Take `..\image\20161121-04.bmp` as an example, the procedure can be done in command line as follows (Note that in windows, `rm -r segmented` should be replace with `del /F /S /Q segmented`):

```
matlab -nosplash -nojvm -nodesktop -r img2segment('..\image\20161121-04.bmp')
python xgboostclassify.py # This can be replaced with matlab -nosplash -nojvm -nodesktop -r svmtest.m
matlab -nosplash -nojvm -nodesktop -r segment2img('..\image\20161121-04.bmp')
rm -r segmented
```

Note that this set of command line can only deal with one image each time, and remember to delete the segmented folder before processing a second image. The .sh file for linux shell and .bat file for windows command line is provided. One only needs to change the variable 'filename' in the command line file to run ImpurityFinder on different images.

# Results:

## Analysis of Results

Most of the analysis of results can be seen in the pdf report. In train folder, we save the false positive rate and true positive rate as falsepos.npy and truepos.npy. One can utilize rocplot.py to read them and plot the corresponding ROC curve for our classifier. 
