function [ bPt ] = BBox( fname )

%fname = '20161121-04-marked.bmp';
%fname = '20161121-06-marked.bmp';
%fname = 'in4483-marked.bmp';
%fname = 'in4484-marked.bmp';
%fname = 'in4488-marked.bmp';


srcimg = imread(fname); %height x width x depth
height = size(srcimg,1);
width = size(srcimg,2);
% optimg = rgb2ycbcr(srcimg);
R = srcimg(:,:,1);
G = srcimg(:,:,2);
B = srcimg(:,:,3);
bbox_index = find((R == 34 & G == 177 & B == 76) | (R == 237 & G == 28 & B == 36) | (R==63 & G==72 & B==204));
bbox = zeros(height, width);
visited = zeros(height, width);
bbox(bbox_index) = 1;
bPt = zeros(0,6);

for i = 1:height
    for j = 1:width
        %% find seed
        if bbox(i, j) == 0
            continue;
        end
        visited(i, j) = 1;
        %Neighbor is visited
        if isempty(find(visited(Neighbor(i, j, height, width))==1)) == 0 
            continue;
        end
        %% find corner
        P1 = [i j]; % Upper Left Point
        
        tmp_i = i;
        tmp_j = j;
        while tmp_i < height && bbox(tmp_i+1, tmp_j)
            tmp_i = tmp_i + 1;           
        end
        P2 = [tmp_i tmp_j]; %2 Lower Left Point 
        
        tmp_i = i;
        tmp_j = j;
        while tmp_j < width && bbox(tmp_i, tmp_j+1)
            tmp_j = tmp_j + 1;           
        end
        P3 = [tmp_i tmp_j]; %3 Upper Right Point
        
        bPt = [bPt;P1 P2 P3];
    end
end

end

