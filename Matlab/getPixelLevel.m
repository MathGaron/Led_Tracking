function [ output ] = getPixelLevel( video )
%GETPIXELLEVEL Summary of this function goes here
%   Detailed explanation goes here
[x,y] = getPixel(video(:,:,1));
output = squeeze(video(x,y,:));
plot(output);

end

