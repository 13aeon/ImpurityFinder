%**************************************************************************
%                 ͼ������D�D��ȡ��ɫ����
%HSV�ռ���ɫֱ��ͼ(��RGB�ռ�ת��ΪHSV�ռ䲢���зǵȼ��������
%��������ɫ������ʾ��һάʸ�����ټ�����ֱ��ͼ��Ϊ��ɫ����
%function : Hist = ColorHistogram(Image)
%Image    : ����ͼ������
%Hist     : ������ɫֱ��ͼ��������256ά
%**************************************************************************
function Hist = ColorHistogram(Image)
 % Image = imread('2.jpg');
[M,N,O] = size(Image);
[h,s,v] = rgb2hsv(Image);
H = h; S = s; V = v;
h = h*360;
 
%*************************************************
%                       �޸�
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
 
%��hsv�ռ�ǵȼ��������
%  h������16����
%  s������4����
%  v������4����
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
 
%��������ɫ�����ϳ�Ϊһά����������L = H*Qs*Qv+S*Qv+v��Qs,Qv�ֱ���S��V����������, Lȡֵ��Χ[0,255]
%ȡQs = 4; Qv = 4
for  i = 1:M
    for j = 1:N
        L(i,j) = H(i,j)*16+S(i,j)*4+V(i,j);
    end
end
%����L��ֱ��ͼ
for i = 0:255
    Hist(i+1) = size(find(L==i),1);
end
Hist = Hist/sum(Hist);
 
%*********************************************************
%�޸�ʹ����ɫ�ۼ�ֱ��ͼ��
%������������������ɫ����ɫ���ϵľ����������֮��Ĺ�ϵ
%ʵ��Ч������
%*********************************************************
% HH(1) = Hist(1);
% for i =1:255
%     HH(i+1) = HH(i)+Hist(i+1);
% end
% Hist = HH;
%*********************************************************