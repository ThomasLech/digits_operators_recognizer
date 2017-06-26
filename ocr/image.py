# from skimage.io import imread
# from skimage.filters import gaussian, threshold_sauvola
# from skimage.morphology import binary_dilation, dilation, square
import cv2

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

def preprocess(image_abs_path):

	max_intensity = 255

	' Load an color image in grayscale - reduce data dimensionality '
	grayscale_img = cv2.imread(image_abs_path, 0)

	' Apply Gaussian Blur effect to REMOVE NOISES from image '
	gaussian_blur = cv2.GaussianBlur(grayscale_img, ksize=(3, 3), sigmaX=0)

	' Apply threshold - make image only black and white '
	# binary_img = cv2.adaptiveThreshold(gaussian_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
	_, binary_img = cv2.threshold(gaussian_blur, 127, 255, cv2.THRESH_BINARY)

	' Inverse colors(black and white) '
	binary_inv_img = max_intensity - binary_img

	'  '
	dilated_img = cv2.dilate(binary_inv_img, kernel=(5, 5))

	' Find contours - extract each separate pattern from image '
	_, contours, _ = cv2.findContours(dilated_img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

	' Sort contours - make pattern order from left to right by X coord '
	contours = sorted(contours, key=lambda cont: cv2.boundingRect(cont)[0])

	valid_conts = []
	for cont in contours:

		' Remove noise objects from image '
		if cv2.contourArea(cont) > 10:

			[x, y, w, h] = cv2.boundingRect(cont)

			valid_conts.append(cont)

			pattern = binary_img[y: y + h, x: x + w]

			# cv2.imshow('pattern', pattern)
			# cv2.waitKey(0)

			' Skeletonize pattern '
			# skel_func

	print('VALID CONTOURS:', len(valid_conts))



	' Apply image dilation '
	# dilated_img = dilation(binary_sauvola, square(3))
	# dilated_img = binary_dilation(binary_sauvola)

	# plt.imshow(binary_sauvola, cmap='gray')
	# plt.show()

if __name__ != '__main__':

	print('Hello World!')