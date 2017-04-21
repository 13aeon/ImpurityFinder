function y= write_result_v1(test_pic,index,output)
% print classification result to result.txt; write in circle structure

file= fopen('predicted.txt','w');
sz= size(index);
num= sz(2);
for i=1:num
    name= test_pic(index(i)).name;
    str=num2str(output(i));
    fprintf(file,'%s %s\n',name,str);
end

y= 1;
end
 

