# BarnacleCounter

This is my submission for for the [Dartmouth DALI Lab 2025 Data Science Application]([url](https://dalilab.notion.site/2a99727739fb4a1b9c49548da435aa86#b7cca6cae95c47419246e08fdce12600))

# **Brief file descriptions**

CropBarnacles.ipynb - Barnacles are placed under a green square. This function uses OpenCV to detect the centroid green square, cropping to that size and returning the image as well as the dimensions. 

UNetTrainer.ipynb - Helper function for training the UNet Model. Barnacle masks are displayed as outlining edges. This function fills those edges in with contour detection from OpenCV, generating a binary mask of 0s and 1s for training. 

UNetModel.ipynb - Long file consisting of preprocessing, data augmentation, U-Net architecture, and the barnacle counter function. Given an input image, this function will display the amount of barnacles in the input image. 

Nearest2n.py - Simple function that, given a number val, returns the nearest 2^n to that number val. This is used to crop the image furthermore to a smaller size. The U-Net Conv2d and MaxPooling functions change the H x W dimension sizes by factors of 2. If dimension sizes are not factors of two, there may be issues with floating point numbers that cause conflict between matching dimensions in the U Net architecture pipeline. 

# **Performance Metrics**

**Pixel accuracy:** 0.9774

**Precision:** 0.9366

**Recall:** 0.9834

**F1score:** 0.9595

**Average ratio of 0s to 1s:** 2.5102

**Training ratio of 0s to 1s:** 2.6984

I created the last two metrics as a basic metric when tweaking the model:
  1. Average ratio of 0s to 1s was the average ratio of background pixels to barnacle pixels in the *predicted image*
  2. Training ratio is the background to barnacle pixels within the images in training

These two values should be as close as possible. 

In the early stages of the model, this metric provided an easy way to determine if my changes to the model were positively or negatively affecting the performance. 


# **How to Replicate**

Just load the files into your local repository, ensure you download the needed libraries in a virtual environment. Run each of the blocks of code in the *UNetModel.ipynb* file. The last function allows you to input an image file and the precision (how big contours need to be to be considered a barnacle) and will output the amount of barnacles in the image. 

*I do automate the cropping process, but I have ran everything at 512 x 512 because otherwise it would likely take eight hours to train the model. If you would like to try to run the model at a higher 2^n such as 1024, you just have to simply change one line of code to 1024. 

# **The ideation proceess**

## Cropping

To be honest, I spent a lot of time on this--by choice, however. I took up this project as a challenge to learn more intricately about PyTorch, data augmentation and several other deep learning and computer vision libraries. I walked into this project only scratching the surface, but now, as I am writing this, I have learned so much. 

My first challenge was automating the cropping process, since the only relevant barnacles are the ones within the square. OpenCV was the most practical library to use. I looked over the documentation and attempted to detect the range of greens which mark the boundaries for the square, using a function to detect square like contour edges. The contour with the largest area was considered the centroid square. 

Unfortunately, this was a pitfall because this only works for one image. I didn't want to spend too much time playing around with libraries so I decided to move forward.

## Preprocessing
The next challenge was preprocessing the data. I had the necessary cropped input image but I needed to mask a binary mask with the masked images. This was also quite simple using OpenCV, detecting the contour edges of the mask( which was easy due to the sharp contrast ), filling in the edges, resulting in a binary mask of 0s and 1s, where 0 represents background and 1s represents a pixel associated with a barnacle.

## Data augmentation
As mentioned before, the cropping only worked for one image. I used albumentations and OpenCV, with nested for loops to generate 600 images of varying noise, rotations, reflections, brightness and shifts. I would not be surprised if my model only worked for this one image since the weights are tailored specifically from 600 variations of one image. This is a major pitfall of the program.

## U-Net
The U-Net is fantastic for segmentation. The issue with traditional CNNs is that as you extract higher level features, the resolution dissolves, and vice versa. With skip connections, U-Nets take the best in either end of spectrums : images are funneled into the encoder, decreasing resolution yet with higher levels of features. These features are saved. As the values pass the bottle neck and into the decoder, spatial dimensions increase once again while features decrease. Skip connections connect the higher level features of the encoder to the higher resolution of the decoder.

I had issues with dimension mismatch. Looking closely at documentation, MaxPool2d decreases spatial dimensions by factor of the kernel_size. Conv2d extracts channel dimensions. Skip connections and concatenations were used to connect the encoder with the decoder and to maintain complementary dimension sizes. ConvTranpose2d, used within the decoder, had a reversal effect of funneling channel dimensions while changing spatial dimension sizes. 

I initially had horrible precision, recall, and accuracy at around 40%, 40%, 60%. This is perhaps where I spent the most time. Initially, the model was predicitng all background pixels. I blamed my data at first and increase augmenting. I used a scheduled learning rate. I increased epochs ( though they plateued relatively early on ). I addressed class imbalances by using a ratio of ~2.5 in my loss function. None of this worked. 

The brekathrough was simply increasing the layers of my U-Net. Surprisngly, it was the model that was the issue and not the data. My original model only extracted 64 features at the deepest level before funneling back up. I added two more layers to extract 512 features. My performance metrics shot up to where it is today. 



