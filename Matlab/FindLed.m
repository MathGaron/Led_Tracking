function [ correlation ] = FindLed( videoString,signal,fps )
%FINDLED Summary of this function goes here
%   Detailed explanation goes here
grayVideo = getGrayscaleVideo(videoString);
correlation = CorrelateVideoAndSignal(grayVideo,signal,fps);
figure, imshow(grayVideo(:,:,1));
figure,ShowCorr2d(correlation);

end

