from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logOut),
    url(r'^favoriteItem/(?P<item_id>\d+)$', views.favoriteItem),
    url(r'^showItemPage/(?P<item_id>\d+)$', views.showItemPage),
    url(r'^addItem$', views.addItem),
    url(r'^addItemPage$', views.addItemPage),
    url(r'^dashboard$', views.dashboard),
    url(r'^cancelfavoriteItem/(?P<item_id>\d+)$', views.cancelfavoriteItem),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
]