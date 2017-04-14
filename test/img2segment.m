function img2segment(image_name)%% constants
hsize = 250; %height
wsize = 250; %width

hstride = hsize; %no overlap
wstride = wsize;



patchcnt = 0;
splitName = strsplit(image_name, '\');
splitName = splitName{end};
splitName = strsplit(splitName, '.');
system(['mkdir segmented']);

fprintf('Processing %s. \n',image_name);
srcimg = imread(image_name); %height x width x depth
%srcimg_marked = imread(['image\'  rawName '-marked.bmp']);
imgHeight = size(srcimg, 1);
imgWidth = size(srcimg, 2);
rawName = splitName{1};
for m = 1:hstride:imgHeight-hstride+1
    for n = 1:wstride:imgWidth-wstride+1
        tmpPatch = srcimg(m:m+hstride-1, n:n+wstride-1,:);
        patchName = ['segmented\' rawName '.' int2str(m) '.' int2str(n) '.bmp'];
        patchcnt = patchcnt + 1;
        imwrite(tmpPatch, patchName);
    end
end
display('Done! All segments are saved in segmented folder.')
