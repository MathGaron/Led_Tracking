function [ gray,mask ] = getGrayscaleVideo( video_string )
%GETGRAYSCALEVIDEO Summary of this function goes here
%   Detailed explanation goes here
wb = waitbar(0,'Video Conversion'); 
obj = VideoReader(video_string);
video = read(obj);
wb = waitbar(0.5,wb,'Cropping and converting to gray');
[imdum rect] = imcrop(video(:,:,1));
gray = [];
for i=1:size(video,4)
    wb = waitbar(0.5 + 0.5*(i/size(video,4)),wb,['iteration: ',num2str(i)]);
    gray = cat(3,gray,imcrop(rgb2gray(video(:,:,:,i)),rect));
end
close(wb); 
end

