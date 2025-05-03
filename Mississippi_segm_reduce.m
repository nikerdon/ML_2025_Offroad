close all
clear all
clc

img = imread("Миссиссиппи\Brown_field\00001\00001.png");
imshow(img)

im = and(and(and(img(:,:,1)>=135, img(:,:,1)<=161), and(img(:,:,2)>=83, img(:,:,2)<=161)), and(img(:,:,3)>=35, img(:,:,3)<=161));

figure
subplot(2,2,1),imshow(im);
title('im')

clean_black = bwareaopen(im,500,4);
clean_white = ~bwareaopen(~clean_black,500,4);

for i=1:size(im,1)
    for j=1:size(im,2)
        if im(i,j) + clean_black(i,j) == 1
            im(i,j) = 0;
        end
        if im(i,j) + clean_white(i,j) == 1
            im(i,j) = 1;
        end
    end
end

saveas(im,'00001_.png')