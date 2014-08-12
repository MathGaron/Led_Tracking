function [ boxes ] = blobDetection( mask )
%BLOBDETECTION Summary of this function goes here
%   Detailed explanation goes here
[L,num] = bwlabel(mask,8);
mesures = regionprops(L,'area','boundingbox');
boxes = [];
for i = 1:num
    if mesures(i).Area > 200
       boxes = cat(1,boxes,mesures(i).BoundingBox);
    end
end

imshow(mask);
hold on
for i = 1:size(boxes,1)
   rectangle('position',boxes(i,:),'EdgeColor','g'); 
end


end

