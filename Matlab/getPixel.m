function [ x,y ] = getPixel( img )
%GETPIXEL Summary of this function goes here
%   Detailed explanation goes here
imshow(img);
[y,x] = ginput(1);
x = uint8(x);
y = uint8(y);

end

