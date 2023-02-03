x = 1:1:6;
l = length(x);
y = ones(1,l);

for i=1:l
    if x(i)==0
        y(i)=0;
    elseif x(i)==1
        y(i)=1/2;
    elseif x(i)==2
        y(i)=(1/2)^2;
    elseif x(i)==3
        y(i)=(1/2)^3;
    elseif x(i)==4
        y(i)=(1/2)^4;
    elseif x(i)==5
        y(i)=(1/2)^5;
    else
        y(i)=(1/2)^6;
    end
end

stem(x,y)
axis padded

xlabel('x')
ylabel('f_X(x)')

mean = 0;
for i=1:l
    mean = mean + x(i)*y(i);
end

mean

moment2 = 0;
for i=1:l
    moment2 = moment2 + (x(i))^2*y(i);
end

moment2