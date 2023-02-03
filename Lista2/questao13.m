x=0:0.01:4;
l = length(x);
y = ones(1,l);

for i=1:l
    if x(i)<1
        y(i)=0;
    elseif x(i)<2
        y(i)=1/2;
    elseif x(i)<3
        y(i)=1/2+1/4;
    else
        y(i)=1;
    end
end
plot(x,y)
axis padded

xlabel('x')
ylabel('F_X(x)')

yticks([0.2, 0.4,1/2, 0.6, 1/2+1/4, 0.8, 1.0])