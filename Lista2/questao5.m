x=0:0.01:1;
l = length(x);
y = ones(1,l);

for i=1:l
    if x(i)<1/2
        y(i)=x(i)+1/2;
    else
        y(i)=1;
    end
end
plot(x,y)
axis padded

xlabel('x')
ylabel('F_X(x)')