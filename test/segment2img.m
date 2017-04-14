function segment2img(image_name)%% constants
fprintf('Segmenting %s. \n',image_name);
fid = fopen('predicted.txt');
file = textscan(fid,'%s','delimiter','\n');
content = char(file{1,1});
[read_num, ~] = size(content);
srcimg = imread(image_name);
splitName = strsplit(image_name, '\');
splitName = splitName{end};
splitName = strsplit(splitName, '.');
rawName = splitName{1};
for i = 1:read_num
    line = textscan(content(i,:),'%s','delimiter',' ');
    line = line{1};
    filename = line{1};
    label = line{2};
    if str2num(label) == 1
       pos = textscan(filename,'%s','delimiter','.');
       pos = pos{1};
       xpos = str2num(pos{2});
       ypos = str2num(pos{3});
       srcimg(xpos:xpos+250,ypos-1:ypos+1,1) = 34;
       srcimg(xpos-1:xpos+1,ypos:ypos+250,1) = 34;
       srcimg(xpos+249:xpos+251,ypos:ypos+250,1) = 34;
       srcimg(xpos:xpos+250,ypos+249:ypos+251,1) = 34;
       srcimg(xpos:xpos+250,ypos-1:ypos+1,2) = 177;
       srcimg(xpos-1:xpos+1,ypos:ypos+250,2) = 177;
       srcimg(xpos+249:xpos+251,ypos:ypos+250,2) = 177;
       srcimg(xpos:xpos+250,ypos+249:ypos+251,2) = 177;
       srcimg(xpos:xpos+250,ypos-1:ypos+1,3) = 76;
       srcimg(xpos-1:xpos+1,ypos:ypos+250,3) = 76;
       srcimg(xpos+249:xpos+251,ypos:ypos+250,3) = 76;
       srcimg(xpos:xpos+250,ypos+249:ypos+251,3) = 76;
    end
end
imwrite(srcimg, ['results\' rawName '.bmp']);
display(['Done! The output file is saved as results\' rawName '.bmp'])