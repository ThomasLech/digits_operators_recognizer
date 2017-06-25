from skimage.io import imread
from skimage.filters import gaussian, threshold_sauvola
from skimage.morphology import binary_dilation, dilation, square

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def preprocess(image_abs_path):

	' Convert image to grayscale - reduce image dimensionality '
	grayscale_img = imread(image_abs_path, as_grey=True)

	' Apply Gaussian Blur effect to REMOVE NOISES from image '
	gaussian_blur = gaussian(grayscale_img)

	' Apply threshold to image(make it black and white) '
	' Sauvola algorithm - appears well suited for text recognition task '
	thresh_sauvola = threshold_sauvola(gaussian_blur)

	' Convert pixels\' corresponding values to either 0 or 1 '
	binary_sauvola = gaussian_blur > thresh_sauvola

	' Apply image dilation '
	# dilated_img = dilation(binary_sauvola, square(3))
	# dilated_img = binary_dilation(binary_sauvola)

	plt.imshow(binary_sauvola, cmap='gray')
	plt.show()

if __name__ != '__main__':

	print('Hello World!')