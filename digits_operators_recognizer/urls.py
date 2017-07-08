"""digits_operators_recognizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# 'Django Rest API urls'
# from rest_framework import routers
# 'Path to resolver app\'s views'
# from digits_operators_recognizer.resolver import views

# router = routers.DefaultRouter()
# router.register(r'images', views.ImageViewSet)

from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Here we include resolver app urls
    url(r'^api/', include('digits_operators_recognizer.resolver.urls')),
    # Address to admin site
    url(r'^admin/', admin.site.urls),
]

# This would allow us to serve media files (e.g. along with a static file) to clients
# In our case, it lets us preview uploaded images through our Browsable API
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
