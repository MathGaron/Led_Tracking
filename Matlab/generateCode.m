function [ output ] = generateCode( frameRate,codeSpeed, code )
%GENERATECODE Summary of this function goes here
%   Detailed explanation goes here
%   frameRate = fps (hz)
%   codeSpeed = led frequency (hz)
%   code = bit code ex : '011010010110'
%

code_dec = bin2dec(code);
frame_s = 1/frameRate;
code_s = 1/codeSpeed;
frame_per_bit = round(code_s/frame_s);
output = [];

for i=1:size(code,2)
    for j = 1:frame_per_bit
        output = cat(1,output,bitget(code_dec,i));
        
    end
end

end

