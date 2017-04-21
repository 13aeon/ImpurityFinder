set image_path=..\image\20161121-04.bmp
matlab -nosplash -nojvm -nodesktop -r img2segment('%image_path%')
pause
matlab -nosplash -nojvm -nodesktop -r svmtest.m
pause
matlab -nosplash -nojvm -nodesktop -r segment2img('%image_path%')
pause
del /F /S /Q segmented