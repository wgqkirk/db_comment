"""db_itrm URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from Db_Management import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$',views.turn_to_index),
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    #url(r'^table_search/', views.table_search),
    url(r'^table_comment_edit/', views.table_comment_edit),
    url(r'^download_excel',views.download_excel),
#    url(r'^switch/', views.switch),

    url(r'^test/',views.test)

]
