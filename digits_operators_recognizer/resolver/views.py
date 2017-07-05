# 'DRF modules'
# # from rest_framework import viewsets
# from rest_framework.views import APIView

'DRF utils'
# from django.http import QueryDict

'For function-based views'
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view

# 'Encode base64'
# import base64
# from django.core.files.base import ContentFile

# from django.http import Http404



import os
from django.conf import settings

'Models'
from digits_operators_recognizer.resolver.models import Image

'Serializers'
from digits_operators_recognizer.resolver.serializers import ImageSerializer
from digits_operators_recognizer.resolver import serializers

'DRF modules'
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser

'Import OCR scripts'
from ocr import image, recognizer


class ImageList(ListAPIView):

	'List all images'

	serializer_class = serializers.ImageSerializer
	queryset = Image.objects.all()

	def get(self, request, fomart=None):

		serializer = ImageSerializer(self.queryset, many=True, context={'request': Request(request),})

		return Response(serializer.data)

class ImageDetail(RetrieveAPIView):

	'Retrieve an image instance'

	serializer_class = serializers.ImageSerializer
	permission_classes = (IsAdminUser,)
	queryset =  Image.objects.all()

class ImageCreate(CreateAPIView):

	'Create a new image instance'

	serializer_class = serializers.ImageSerializer

	def post(self, request):

		serializer = ImageSerializer(data=request.data)
		if serializer.is_valid():

			' Save request image in the database '
			serializer.save()

			' RUN OCR script '
			image_path = serializer.data.get('image')[1:]	# We need to remove slash from the beginning of the path
			image_abs_path = os.path.join(settings.BASE_DIR, image_path)

			' Extract patterns(digits and arithmetic operators) '
			patterns = image.extract_patterns(image_abs_path)

			' Run recognizer on each separate pattern '
			prediction = recognizer.recognize(patterns)

			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# class ImageList(APIView):
#
# 	'List images, or create a new image'
#
# 	def get(self, request, format=None):
#
# 		images = Image.objects.all()

# 		serializer = ImageSerializer(images, many=True, context={'request': Request(request),})
#
# 		return Response(serializer.data)
#
# 	def post(self, request, format=None):
#
# 		# 'Get BASE64 ENCODED IMAGE passed along with a request'
# 		# base64_img = request.data.get('image')
#
#
# 		# 'Extract image format and image itself from BASE64 STRING'
# 		# 'Example base64 slice: "data:image/png;base64,iVBORw..."'
# 		# img_format, base64_content = base64_img.split(';base64,')
# 		# 'Now img_format is "data:image/png" and base64_content is "iVBORw..."'
# 		# extention = img_format.split('/')[-1]
# 		# 'extension takes right side of "data:image/png" split by "/"'
# 		# 'Hence extension is "png"'
#
# 		# 'ContentFile is a File Object that CAN operate on a string of bytes'
# 		# raw_content = ContentFile(base64.b64decode(base64_content), name='temp.' + extention) # You can save this as file istance.
#
#
#
# 		# 'Convert python dictionary to QueryDict'
# 		# data = QueryDict('', mutable=True)
# 		# data.update(dict({'image': raw_content}))
#
#
# 		serializer = ImageSerializer(data=request.data)
# 		if serializer.is_valid():
#
# 			' Save request image in the database '
# 			serializer.save()
#
# 			' RUN OCR script '
# 			image_path = serializer.data.get('image')[1:]	# We need to remove slash from the beginning of the path
# 			image_abs_path = os.path.join(settings.BASE_DIR, image_path)
#
# 			' Extract patterns(digits and arithmetic operators) '
# 			patterns = image.extract_patterns(image_abs_path)
#
# 			' Run recognizer on each separate pattern '
# 			prediction = recognizer.recognize(patterns)
#
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class ImageDetail(APIView):
#
# 	'Retrieve, update or delete an image'
#
# 	def get_object(self, pk):
#
# 		try:
# 			return Image.objects.get(pk=pk)
# 		except Image.DoesNotExist:
# 			raise Http404
#
# 	def get(self, request, pk, format=None):
#
# 		image = self.get_object(pk=pk)
# 		serializer = ImageSerializer(image)
#
# 		return Response(serializer.data)
#
# 	def put(self, request, pk, format=None):
#
# 		image = self.get_object(pk=pk)
# 		serializer = ImageSerializer(image, data=request.data)
#
# 		if serializer.is_valid():
#
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# 	def delete(self, request, pk, format=None):
#
# 		image = self.get_object(pk=pk)
# 		image.delete()
#
# 		return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'DELETE'])
# def image_detail(request, pk, format=None):

# 	'\
# 	Retrieve, update or delete an image\
# 	'

# 	try:
# 		image = Image.objects.get(pk=pk)
# 	except Image.DoesNotExist:
# 		print('error')
# 		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

# 	if request.method == 'GET':

# 		serializer = ImageSerializer(image)

# 		return Response(serializer.data)

# 	elif request.method == 'PUT':

# 		data = JSONParser().parse(request)
# 		serializer = ImageSerializer(data=data)

# 		if serializer.is_valid():

# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)

# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 	elif request.method == 'DELETE':

# 		image.delete()

# 		return HttpResponse(status=status.HTTP_204_NO_CONTENT)
