from django.conf.urls import url

from digits_operators_recognizer.resolver import views
from rest_framework.urlpatterns import format_suffix_patterns

# Here we specify available URL addresses
urlpatterns = [
	url(r'^images/$', views.ImageList.as_view()),
	url(r'^images/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
	url(r'^images/create/$', views.ImageCreate.as_view()),
]

# Adding this lets you use filename extensions on URLs to provide an endpoint for a given media type.
# For example you can get endpoint data in json representation or html static file
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
