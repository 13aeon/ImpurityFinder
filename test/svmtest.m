clear
load 'model\out2total.mat'
str_out= 'segmented';

% set the path 
addpath(genpath(str_out),genpath(str_test));
% addpath(genpath(str_total));                % choose the set
test_pic= dir(strcat(str_out,'\*.bmp'));

% index_t= 1:5005;                          %  set the index
index_t= setdiff([1:pic_num],index);      
label_test= zeros(test_num,1);
test_data= zeros(test_num,length);

for i=1:test_num
    name= test_pic(index_t(i)).name;
    image= imread(name);
    label_test(i)= name(1)- '0';
    % place the characters
    test_data(i,:)= ch_vector_v1(image); 
end

[test_out,score]= predict(SVMModel,test_data);
% plotroc(label_test',score(:,2)');
[rpr,fpr,thresholds]= roc(label_test',score(:,2)');
[~,~,~,AUC]= perfcurve(label_test',score(:,2)',1);
idr= find(rpr> 0.9,1,'first');
output= score(:,2)> thresholds(idr);
write_result_v1(test_pic,index_t,output);
AUC,

% out to total: AUC only 0.8078