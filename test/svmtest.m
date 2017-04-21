clear
load 'model\out2total.mat'

[test_out,score]= predict(SVMModel,test_data);
% plotroc(label_test',score(:,2)');
[rpr,fpr,thresholds]= roc(label_test',score(:,2)');
[~,~,~,AUC]= perfcurve(label_test',score(:,2)',1);
idr= find(rpr> 0.9,1,'first');
output= score(:,2)> thresholds(idr);
write_result_v1(test_pic,index_t,output);
AUC,

% out to total: AUC only 0.8078