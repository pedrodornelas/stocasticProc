x = 0:0.01:7;
l = length(x);
y = ones(1,l);

for i=1:l
    if x(i)<1
        y(i)=0;
    elseif x(i)<2
        y(i)=1/2;
    elseif x(i)<3
        y(i)=1/2+(1/2)^2;
    elseif x(i)<4
        y(i)=1/2+(1/2)^2+(1/2)^3;
    elseif x(i)<5
        y(i)=1/2+(1/2)^2+(1/2)^3+(1/2)^4;
    elseif x(i)<6
        y(i)=1/2+(1/2)^2+(1/2)^3+(1/2)^4+(1/2)^5;
    else
        y(i)=1/2+(1/2)^2+(1/2)^3+(1/2)^4+(1/2)^5+(1/2)^6;
    end
end

plot(x,y)
axis padded

xlabel('x')
ylabel('F_X(x)')