from django.conf.urls import url
from .views import reg,delete,Select_by_id,update_by_id,Create
urlpatterns =[
    url(r'^reg$',reg),
    url(r'^delete$',delete),
    url(r'^Select_by_id$',Select_by_id),
    url(r'^update_by_id$',update_by_id),
    url(r'^Create$',Create),
]