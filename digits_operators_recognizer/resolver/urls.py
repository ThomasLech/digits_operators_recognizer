from django.conf.urls import url
from digits_operators_recognizer.resolver import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^images/$', views.ImageList.as_view()),
	url(r'^images/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)