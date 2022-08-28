"""sims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('sims3.urls')),  # how to get the default welcome page : index.html
    # in Lib > site-packages > django > views > templates
    # path('', admin.site.urls),    # or path('', admin.site.urls) for the admin page
    # path('admin/', admin.site.urls),
    path('sims3/admin', admin.site.urls),
    # path('',include('sims3.urls')),
    path('sims3/', include('sims3.urls')),
]
