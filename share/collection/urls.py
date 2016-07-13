from django.conf.urls import url

from .views import (
    # collection_list,
    collection_create,
    collection_detail,
    # collection_update,
    # collection_delete,
    link_add,
    search_link,
    # likn_delete,
)

urlpatterns = [
    # url(r'^$', collection_list, name='list'),
    url(r'^create$', collection_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/add$', link_add, name='add'),
    url(r'^(?P<slug>[\w-]+)(?:/(?P<tag>[\w-]+))?/$', collection_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/search$', search_link, name="search_link"),
    # url(r'^(?P<slug>[\w-]+)/edit$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete$', post_delete),
]
