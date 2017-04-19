%**************************************************************************
%                 图像检索――提取颜色特征
%HSV空间颜色直方图(将RGB空间转化为HSV空间并进行非等间隔量化，
%将三个颜色分量表示成一维矢量，再计算其直方图作为颜色特征
%function : Hist = ColorHistogram(Image)
%Image    : 输入图像数据
%Hist     : 返回颜色直方图特征向量256维
%**************************************************************************
function Hist = ColorHistogram(Image)
 % Image = imread('2.jpg');
[M,N,O] = size(Image);
[h,s,v] = rgb2hsv(Image);
H = h; S = s; V = v;
h = h*360;
 
%*************************************************
%                       修改
% for i = 1:M
%     for j=1:N
%         if v(i,j)<0.15
%             H(i,j) = 0;
%             S(i,j) = 0;
%             V(i,j) = 0;
%         end
%         if s(i,j)<0.1&v>0.8
%             H(i,j) = 0;
%             S(i,j) = 0;
%             V(i,j) = 1;
%         end
%     end
% end
%*************************************************
 
%将hsv空间非等间隔量化：
%  h量化成16级；
%  s量化成4级；
%  v量化成4级；
for i = 1:M
    for j = 1:N
        if h(i,j)<=15||h(i,j)>345
            H(i,j) = 0;
        end
        if h(i,j)<=25&&h(i,j)>15
            H(i,j) = 1;
        end
        if h(i,j)<=45&&h(i,j)>25
            H(i,j) = 2;
        end
        if h(i,j)<=55&&h(i,j)>45
            H(i,j) = 3;
        end
        if h(i,j)<=80&&h(i,j)>55
            H(i,j) = 4;
        end
        if h(i,j)<=108&&h(i,j)>80
            H(i,j) = 5;
        end
        if h(i,j)<=140&&h(i,j)>108
            H(i,j) = 6;
        end
        if h(i,j)<=165&&h(i,j)>140
            H(i,j) = 7;
        end
        if h(i,j)<=190&&h(i,j)>165
            H(i,j) = 8;
        end
        if h(i,j)<=220&&h(i,j)>190
            H(i,j) = 9;
        end
        if h(i,j)<=255&&h(i,j)>220
            H(i,j) = 10;
        end
        if h(i,j)<=275&&h(i,j)>255
            H(i,j) = 11;
        end
        if h(i,j)<=290&&h(i,j)>275
            H(i,j) = 12;
        end
        if h(i,j)<=316&&h(i,j)>290
            H(i,j) = 13;
        end
        if h(i,j)<=330&&h(i,j)>316
            H(i,j) = 14;
        end
        if h(i,j)<=345&&h(i,j)>330
            H(i,j) = 15;
        end
    end
end
for i = 1:M
    for j = 1:N
        if s(i,j)<=0.15&&s(i,j)>0
            S(i,j) = 0;
        end
        if s(i,j)<=0.4&&s(i,j)>0.15
            S(i,j) = 1;
        end
        if s(i,j)<=0.75&&s(i,j)>0.4
            S(i,j) = 2;
        end
        if s(i,j)<=1&&s(i,j)>0.75
            S(i,j) = 3;
        end
    end
end
for i = 1:M
    for j = 1:N
        if v(i,j)<=0.15&&v(i,j)>0
            V(i,j) = 0;
        end
        if v(i,j)<=0.4&&v(i,j)>0.15
            V(i,j) = 1;
        end
        if v(i,j)<=0.75&&v(i,j)>0.4
            V(i,j) = 2;
        end
        if v(i,j)<=1&&v(i,j)>0.75
            V(i,j) = 3;
        end
    end
end
 
%将三个颜色分量合成为一维特征向量：L = H*Qs*Qv+S*Qv+v；Qs,Qv分别是S和V的量化级数, L取值范围[0,255]
%取Qs = 4; Qv = 4
for  i = 1:M
    for j = 1:N
        L(i,j) = H(i,j)*16+S(i,j)*4+V(i,j);
    end
end
%计算L的直方图
for i = 0:255
    Hist(i+1) = size(find(L==i),1);
end
Hist = Hist/sum(Hist);
 
%*********************************************************
%修改使用颜色累加直方图：
%　　可以体现两种颜色在颜色轴上的距离和相似性之间的关系
%实验效果不好
%*********************************************************
% HH(1) = Hist(1);
% for i =1:255
%     HH(i+1) = HH(i)+Hist(i+1);
% end
% Hist = HH;
%*********************************************************