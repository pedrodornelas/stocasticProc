x = 1:1:6;
l = length(x);
y = cos(x*pi/6);

mean = 0;
for i=1:l
    mean = mean + 1/6*y(i);
end

mean

moment2 = 0;
for i=1:l
    moment2 = moment2 + 1/6*(y(i))^2;
end

moment2

moment2-mean