function [ mask ] = BackgroundSubstractionGaussian( mu,sig,img )
%BACKGROUNDSUBSTRACTIONGAUSSIAN Summary of this function goes here
%   Detailed explanation goes here
distance = abs(img-mu);
foreground = (distance./sqrt(sig))>30.5;

kernelErode = [1 0 0 1;
               0 1 1 0;
               0 1 1 0;
               1 0 0 1];
mask = imerode(foreground,kernelErode);
%mask = imerode(mask,kernelErode);
kernelDilate = [0 0 1 0;
               1 1 1 0;
               0 1 1 1;
               0 1 0 0];
for i=1:3
    mask = imdilate(mask,kernelDilate);
end

end

