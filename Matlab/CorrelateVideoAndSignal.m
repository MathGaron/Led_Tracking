function [ output ] = CorrelateVideoAndSignal( video, signal, fps )
%CORRELATEVIDEOANDSIGNAL Summary of this function goes here
%   Detailed explanation goes here
wb = waitbar(0,'Correlation Progress'); 
h=size(video,1);
w=size(video,2);
output = zeros(h,w);

%after correlation filter:
signalTime = size(signal,1)/fps;
signalFreq = signalTime /(fps/2);
    %pass band design
gap = 0.05*signalFreq;
[B,A] = butter(2,signalFreq-gap,'high');

for i = 1:h
    wb = waitbar((i)/(h),wb,['iteration: ',num2str(i)]);
    for j = 1:w
        correl = xcov(signal,squeeze(video(i,j,:)));
        %output(i,j) = max(filter(B,A,correl));
        output(i,j) = max(correl);
        %peaks = findpeaks(correl,'MinPeakDistance',size(signal,1));
        %peaks = peaks(peaks > 1);
        %if size(peaks,1) >= 5
        %    output(i,j) = mean(peaks);
        %end
    end
end
close(wb); 
end

