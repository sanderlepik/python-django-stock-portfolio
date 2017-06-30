from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.update_stock_table, name='update_stock_table'),
]
