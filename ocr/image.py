from skimage import img_as_ubyte
from skimage.io import imread
from skimage.filters import gaussian, threshold_sauvola, threshold_minimum
from skimage.morphology import square, erosion, skeletonize, thin
# from skimage.measure import find_contours
import numpy as np
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
	eroded_img = erosion(binary_img, selem=square(3))

	return eroded_img

def interpolate_contour(contour, box_size):

	cont_width, cont_height = cv2.boundingRect(contour)[2:]
	cont_width -= 1
	cont_height -= 1
	# print('cont_width:', cont_width)
	# print('cont_height:', cont_height)

	# Get contour width : height ratio
	ratio = cont_width / cont_height

	scale = 1.0
	# Get scale
	if ratio < 1.0:
		scale = box_size / cont_height
	else:
		scale = box_size / cont_width

	# print('scale:', scale)
	# Interpolate contour and round coordinate values to int
	return (contour * scale).astype(dtype=np.int32)

def get_scale(parent_contour, parent_width, parent_height, box_size):

	ratio = parent_width / parent_height

	# Get scale
	if ratio < 1.0:
		return box_size / parent_height
	else:
		return box_size / parent_width

def shift(contour):

	x_min, y_min = contour.min(axis=0)[0]
	return np.subtract(contour, [x_min, y_min])

def get_family(outer_contour, contours):

	child_contours = [cont for idx, cont in enumerate(contours) if cont]
	return [outer_contour] + [contours]

def extract_patterns(image_abs_path):

	box_axis = 62
	max_intensity = 1

	' Convert scikit-image to opencv-like image '
	binary_img = preprocess(image_abs_path)
	# cv2.imwrite('thresh.png', img_as_ubyte(binary_img))

	' Inverse colors: black --> white | white --> black '
	binary_inv_img = max_intensity - binary_img
	# cv2.imshow('binary_inv_img', binary_inv_img)

	' Find contours - extract each separate pattern from image '
	_, contours, hierarchy = cv2.findContours(img_as_ubyte(binary_inv_img), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
	hierarchy = hierarchy[0]

	' Sort contours - make pattern order from left to right by X coord '
	# contours = sorted(contours, key=lambda cont: cv2.boundingRect(cont)[0])

	# Shift contours
	# shifted_contours = [shift(contour) for contour in contours]

	# Interpolate contours
	# contours = [interpolate_contour(shifted_cont, box_size=box_axis) for shifted_cont in contours]

	parents = [{'idx': idx, 'contour': contour} for idx, contour in enumerate(contours) if hierarchy[idx][3] == -1]

	cont_families = []
	for parent in parents:

		pattern = np.ones(shape=(112, 112), dtype=np.uint8) * 255

		parent_contour = parent['contour']
		parent_idx = parent['idx']

		family = {'parent': parent_contour}
		family['children'] = [contour for idx, contour in enumerate(contours) if hierarchy[idx][3] == parent_idx]

		x_min, y_min = parent_contour.min(axis=0)[0]
		x_max, y_max = parent_contour.max(axis=0)[0]

		parent_width = x_max - x_min
		parent_height = y_max - y_min

		# Shift family
		family['parent'] = np.subtract(family['parent'], [x_min, y_min])
		family['children'] = [np.subtract(child_cont, [x_min, y_min]) for child_cont in family['children']]

		# Get scale
		scale = get_scale(family['parent'], parent_width, parent_height, box_size=112)

		# Rescale family so it fits into 32x32 box
		family['parent'] = (family['parent'] * scale).astype(np.int32)
		family['children'] = [(child_cont * scale).astype(np.int32) for child_cont in family['children']]


		# Get margin
		new_parent_width = parent_width * scale
		new_parent_height = parent_height * scale
		margin_x = int((112 - new_parent_width) / 2)
		margin_y = int((112 - new_parent_height) / 2)


		# Center family within a 32x32 box
		family['parent'] = np.add(family['parent'], [margin_x, margin_y])
		family['children'] = [np.add(child_cont, [margin_x, margin_y]) for child_cont in family['children']]


		# Draw parent contour with children contours
		cv2.fillPoly(pattern, [family['parent']], (0))
		cv2.fillPoly(pattern, family['children'], (255))


		# Skeletonize pattern
		pattern_skeleton = thin(255 - pattern)
		print(pattern_skeleton)

		cv2.imshow('pattern', 255 - img_as_ubyte(pattern_skeleton))
		cv2.waitKey(0)

	patterns = []

			# [x, y, w, h] = cv2.boundingRect(cont)
			#
			# ' Cut off pattern found in an image '
			# pattern = binary_inv_img[y: y + h, x: x + w]
			#
			# ' Make each pattern 1-pixel thick '
			# pattern_skeleton = thin(pattern)
			#
			# # pattern_skeleton = max_intensity - pattern_skeleton
			# # print(pattern_skeleton)
			# pattern_skeleton = img_as_ubyte(pattern_skeleton)
			# pattern_skeleton = 255 - pattern_skeleton
			# # cv2.imshow('pattern_skeleton', pattern_skeleton)
			# # cv2.waitKey(0)
			# # cv2.imwrite('pattern_' + str(idx) + '.png', pattern_skeleton)
			#
			# patterns.append(pattern_skeleton)

	return patterns
