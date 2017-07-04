from skimage import img_as_ubyte
from skimage.io import imread
from skimage.filters import gaussian, threshold_sauvola, threshold_minimum
from skimage.morphology import square, erosion, skeletonize, thin
# from skimage.measure import find_contours
import cv2

' Preprocess requested image '
def preprocess(image_abs_path):

	' Convert color(3-channel deep) image into grayscale(1-channel deep) - reduce data dimensionality '
	grayscale_img = imread(image_abs_path, as_grey=True)

	' Apply Gaussian Blur - remove noises '
	gaussian_blur = gaussian(grayscale_img, sigma=1)

	' Apply minimum threshold '
	thresh_sauvola = threshold_minimum(gaussian_blur)

	' Convert minimum threshold output array values to either 1 or 0(white or black) '
	binary_img = gaussian_blur > thresh_sauvola

	' Apply dilation - remove noises left after binarization step '
	# dilated_img = binary_dilation(binary_img)
	' Apply erosion - make patterns thicker '
	eroded_img = erosion(binary_img, selem=square(5))

	return eroded_img

def extract_patterns(image_abs_path):

	max_intensity = 1

	' Convert scikit-image to opencv-like image '
	binary_img = preprocess(image_abs_path)
	# cv2.imshow('binary_img', binary_img)
	# cv2.waitKey(0)
	#
	' Inverse colors: black --> white | white --> black '
	binary_inv_img = max_intensity - binary_img
	# cv2.imshow('binary_inv_img', binary_inv_img)

	' Find contours - extract each separate pattern from image '
	_, contours, _ = cv2.findContours(img_as_ubyte(binary_inv_img), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

	' Sort contours - make pattern order from left to right by X coord '
	contours = sorted(contours, key=lambda cont: cv2.boundingRect(cont)[0])

	patterns = []
	' Iterate throught list of extracted contours '
	for cont in contours:

		' Remove noise objects from image '
		if cv2.contourArea(cont) > 40:

			[x, y, w, h] = cv2.boundingRect(cont)

			' Cut off pattern found in an image '
			pattern = binary_inv_img[y: y + h, x: x + w]

			' Make each pattern 1-pixel thick '
			pattern_skeleton = thin(pattern)

			# pattern_skeleton = max_intensity - pattern_skeleton
			# print(pattern_skeleton)
			pattern_skeleton = img_as_ubyte(pattern_skeleton)
			pattern_skeleton = 255 - pattern_skeleton
			cv2.imshow('pattern_skeleton', pattern_skeleton)
			cv2.waitKey(0)

			patterns.append(pattern_skeleton)

	return patterns

if __name__ != '__main__':

	pass
