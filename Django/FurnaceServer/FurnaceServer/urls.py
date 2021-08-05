"""FurnaceServer URL Configuration

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
from django.urls import path,include
from text.views import index,set_cookie,get_session,UsernameCountView

texturl = [
  path('index/',index),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/',include(texturl)),
    path('set_cookie/',set_cookie),
    path('get_session/',get_session),
    path('test/',UsernameCountView.as_view()),
]


