function [ output ] = getPixelCorrelation( video,code )
%GETPIXELCORRELATION Summary of this function goes here
%   Detailed explanation goes here
[x,y] = getPixel(video(:,:,1));
pixelValues = squeeze(video(x,y,:));
output = xcov(pixelValues,code);
plot(output)


end

