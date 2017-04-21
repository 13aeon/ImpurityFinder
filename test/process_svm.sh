image_path='..\image\20161121-04.bmp'
matlab -nosplash -nojvm -nodesktop -r img2segment('${image_path}')
matlab -nosplash -nojvm -nodesktop -r svmtest.m
matlab -nosplash -nojvm -nodesktop -r segment2img('${image_path}')
rm -r segmented
rm predicted.txt