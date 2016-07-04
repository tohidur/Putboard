from django.conf.urls import url

from .views import (
    collection_list,
    collection_create,
    collection_detail,
    # collection_update,
    # collection_delete,
    link_add,
    # likn_delete,
)

urlpatterns = [
    url(r'^$', collection_list, name='list'),
    url(r'^create$', collection_create, name="collection_create"),
    url(r'^(?P<slug>[\w-]+)/add$', link_add, name='link_add'),
    url(r'^(?P<slug>[\w-]+)/$', collection_detail, name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete$', post_delete),
]