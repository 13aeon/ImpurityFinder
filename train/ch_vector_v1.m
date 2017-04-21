function y= ch_vector_v1(image)
% return row vector of several characters of the image

En= entropy(rgb2gray(image));                     % Entropy: change to gray image
Er= max(xcorr(reshape(image,1,numel(image))));    % Correlation

BW= edge(rgb2gray(image),'sobel');                % binary image
S= bwarea(BW);                                    % area of BW

% ST= regionprops(BW,'Perimeter'); 
% Pm= ST(1).Perimeter;
% L= bweuler(BW,4);
% C= Pm^2/S;

hist= ColorHistogram(image);

% scaling
En= En/10;
Er= Er/10^9;
S= S/10000;

y=[ En, S, Er, hist(1:80)];

end
