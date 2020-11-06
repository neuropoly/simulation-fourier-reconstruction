%% Ghosting
% Applies an offset every x line of the FFT 
close all
clear all

image = im2double(imread('brain_MRI.jpg'));

FFT = fft2(image);

FFT_mod = FFT;

input = inputdlg({'Apply offset every x line ? (1,2,3...)','Offset value to apply',...
    'Apply the offset on (magnitude/phase/both)'}, 'Ghosting order', 1 , {num2str(2),num2str(100), 'magnitude'},'on');

order = str2num(input{1});
offset = str2num(input{2});
type = input{3};
for x = 1:size(FFT,1)/order
    if type == "magnitude"
        FFT_mod(order*x,:) = (abs(FFT_mod(order*x,:))+offset).*exp(i*(angle(FFT_mod(order*x,:)))); % magnitude
    elseif type == "phase"
        FFT_mod(order*x,:) = (abs(FFT_mod(order*x,:))).*exp(i*(angle(FFT_mod(order*x,:))+offset)); % phase
    elseif type == "both"
        FFT_mod(order*x,:) = (abs(FFT_mod(order*x,:))+offset).*exp(i*(angle(FFT_mod(order*x,:))+offset)); % both
    else 
        errordlg('Wrong parameter set')
    end
end

image_mod = ifft2(FFT_mod);

figure('units','normalized','outerposition',[0 0 1 1],'name','Ghosting')
subplot(231)
imshow(image,[])
title('Original image')
subplot(234)
imshow(abs(image_mod))
title('Modified Image')
subplot(232)
imshow(log(abs(fftshift(FFT))),[])
title('Original FFT - Magnitude')
subplot(235)
imshow(log(abs(fftshift(FFT_mod))),[])
title('Modified FFT - Magnitude')
subplot(233)
imshow(angle(FFT),[])
title('Original FFT - Phase')
subplot(236)
imshow(angle(FFT_mod),[])
title('Modified image - Phase')

%% Offset on a band in k-space
close all
clear all

image = im2double(imread('brain_MRI.jpg'));
FFT = fft2(image);

offset = 200;
FFT_mod = FFT;
for x = 10:60
    FFT_mod(x,:) = FFT_mod(x,:) + offset;
end

FFT_mod = abs(FFT_mod).*exp(i*(angle(FFT)));
image_mod = ifft2(FFT_mod);

figure('units','normalized','outerposition',[0 0 1 1],'name','Ghosting')
subplot(231)
imshow(image,[])
title('Original image')
subplot(234)
imshow(image_mod)
title('Modified Image')
subplot(232)
imshow(log(abs(fftshift(FFT))),[])
title('Original FFT - Magnitude')
subplot(235)
imshow(log(abs(fftshift(FFT_mod))),[])
title('Modified FFT - Magnitude')
subplot(233)
imshow(angle(fftshift(FFT)),[])
title('Original FFT - Phase')
subplot(236)
imshow(angle(fftshift(FFT_mod)),[])
title('Modified image - Phase')

%% Aliasing 
close all
clear all

image = im2double(imread('brain_MRI.jpg'));

FFT = fft2(image);

for x = 1:length(FFT)/2
    FFT(2*x,:) = zeros(1,length(FFT(1,:)));
    FFT(:,2*x) = zeros(length(FFT(:,1)),1);
end

image_mod = ifft2(FFT);

figure('name','Aliasing')
subplot(121)
imshow(image_mod)
title('Image')
subplot(122)
imshow(abs(FFT))
title('FFT')

%% FFT reduction
close all
clear all

image = im2double(imread('brain_MRI.jpg'));

FFT = fft2(image);
[x,y] = size(FFT);
for i=0:x/2-1
    FFT(x-2*i,:) = [];
end
for i=0:y/2-1
    FFT(:,y-2*i)= [];
end

image_mod = ifft2(FFT);

figure('name','Reduction')
subplot(121)
imshow(image_mod)
title('Image')
subplot(122)
imshow(abs(FFT))
title('FFT')

%% Spike artifact
close all
clear all

image = im2double(imread('brain_MRI.jpg'));

FFT = fft2(image);
FFT(1,20) = 3*max(max(FFT));

image_mod = ifft2(FFT);

figure('name','Spike')
subplot(121)
imshow(image_mod)
title('Image')
subplot(122)
imshow(abs(FFT))
title('FFT')
