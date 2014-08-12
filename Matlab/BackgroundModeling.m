function [ mu,sig ] = BackgroundModeling( video )
%BACKGROUNDSUBSTRACTION Summary of this function goes here
%   Detailed explanation goes here
h = size(video,1);
w = size(video,2);

mu = zeros(h,w);
sig = zeros(h,w);

for i = 1:h
   for j = 1:w
       [mu(i,j),sig(i,j)] = normfit(single(squeeze(video(i,j,:)))); 
   end
end


end

