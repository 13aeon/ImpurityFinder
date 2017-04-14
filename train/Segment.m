%% constants
hsize = 250; %height
wsize = 250; %width

hstride = hsize; %no overlap
wstride = wsize;

srcdir = '..\image\test\';
optname = [];%[int2str(hsize) 'x' int2str(wsize)];
optdir = ['.\patch\test' optname '\'];
system(['mkdir ' optdir]);

dirOutput=dir(fullfile(srcdir,'*.bmp'));
fileNames={dirOutput.name}';



patchcnt = 0;


for i = 1:length(fileNames)
    splitName = strsplit(fileNames{i}, '-');
    %if strcmp(splitName{end}, 'marked.bmp')
    %    continue
    %end
    
    fprintf('%d, %s\n', i, fileNames{i});
    srcimg = imread(['..\image\test\'  fileNames{i}]); %height x width x depth
    splitName = strsplit(fileNames{i}, '.');
    rawName = splitName{1};
    %srcimg_marked = imread(['image\'  rawName '-marked.bmp']);
    bpt = BBox(['..\image\test_labeled\' fileNames{i}]);%BBox(['image\'  rawName '-marked.bmp']);
    num_box = size(bpt,1);
    imgHeight = size(srcimg, 1);
    imgWidth = size(srcimg, 2);
    
    for m = 1:hstride:imgHeight-hstride+1
        for n = 1:wstride:imgWidth-wstride+1
            tmpPatch = srcimg(m:m+hstride-1, n:n+wstride-1,:);
            label = 0;
            for j = 1:num_box
               if ~(bpt(j,1)>=m+hstride-1 || bpt(j,2)>=n+wstride-1 || bpt(j,3)<=m || bpt(j,6)<=n)
                   label = 1;
                   break
               end
            end
            patchName = [optdir num2str(label) '-' rawName '.' int2str(m) '.' int2str(n) '.bmp'];
            patchcnt = patchcnt + 1;
            imwrite(tmpPatch, patchName);
        end
    end

end