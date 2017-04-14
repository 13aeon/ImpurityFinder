% SVM for characters

%% preparation
% pic_num= 3661;
% pic_num= 1344;
pic_num= 5005;
c= 0.9;
a= 250;
str_out= 'D:\ѧϰ\2016-2017ѧ�꣨��������\03ͳ���źŴ���\����ҵ\out';
str_total= 'D:\ѧϰ\2016-2017ѧ�꣨��������\03ͳ���źŴ���\����ҵ\total';
str_test= 'D:\ѧϰ\2016-2017ѧ�꣨��������\03ͳ���źŴ���\����ҵ\test';

train_num= round(pic_num*c);
test_num= pic_num- round(pic_num*c);
index= sort(randperm(pic_num,train_num));
label= zeros(train_num,1);                  % label of training data
% addpath(genpath(str_out),genpath(str_test));
addpath(genpath(str_total));                % choose the set
test_pic= dir(strcat(str_total,'\*.bmp'));
[~,length]= size(ch_vector(imread(test_pic(1).name)));
data= zeros(train_num,length);

for i=1:train_num
    name= test_pic(index(i)).name;
    image= imread(name);
    label(i)= name(1)-'0';
    % place the characters to data
    data(i,:)= ch_vector(image);
end

%% train & test
SVMModel= fitcsvm(data,label,'KernelFunction','rbf','Standardize',true),%,'ClassName',[0 1]),

% adjust to different test set
index_t= setdiff([1:pic_num],index);      % get test data index
label_test= zeros(test_num,1);
test_data= zeros(test_num,length);

for i=1:test_num
    name= test_pic(index_t(i)).name;
    image= imread(name);
    label_test(i)= name(1)- '0';
    % place the characters
    test_data(i,:)= ch_vector(image); 
end

% index_t= [2800:2800+test_num-1];
% 
% test_num= train_num;
% test_data= zeros(test_num,length);
% label_test= zeros(test_num,1);
%  
% for i=1:test_num
%     name= test_pic(index(i)).name;
%     image= imread(name);
%     label_test(i)= name(1)- '0';
%     % place the characters
%     test_data(i,:)= ch_vector(image); 
% end

%% prediction & write into file
[test_out,score] = predict(SVMModel,test_data);
plotroc(label_test',score(:,2)');
[~,~,~,AUC]= perfcurve(label_test',score(:,2)',1);
write_result(test_pic,index_t,label_test);
AUC,


