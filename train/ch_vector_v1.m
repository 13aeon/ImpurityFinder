function y= ch_vector_v1(image)
% return row vector of several characters of the image

BW= edge(rgb2gray(image),'sobel');
En= entropy(image);
S= bwarea(BW);
% L= bweuler(BW,4);
Er= max(xcorr(reshape(image,1,numel(image))));
hist= ColorHistogram(image);

% [H, theta, rho]= hough(BW,'RhoResolution',0.5,'ThetaResolution',0.5);
% p= houghpeaks(H,5);
% lines= houghlines(BW,theta,rho,p);
% iflines= length(lines);
% linear= max(max(H));

y=[En, S, Er, hist(1:80)];

end