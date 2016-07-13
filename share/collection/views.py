import os
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CollectionForm, LinkForm
from .models import Collection, Link, Tag
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from urlparse import urlparse
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from django.http import HttpResponseForbidden
# Create your views here.

@login_required
def collection_create(request):
    """
    Gets the post requset of storinig collection form, save it,
     and create a directory for saving images of it's links.

    @param:     post resuest
    @return     redirect to recent created collection page.

    """
    form = CollectionForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        if not os.path.exists("./static/img/"+str(instance.id)+"/"):
            os.makedirs("./static/img/"+str(instance.id)+"/")
        return HttpResponseRedirect(instance.get_absolute_url())


def collection_detail(request, slug=None, tag=None):
    """
    """
    form_board = CollectionForm(None)
    form_link = LinkForm(None)
    query_list = Collection.objects.filter(slug=slug)
    if request.user.is_authenticated():
        query_list = Collection.objects.filter(user=request.user)
    if slug:
        collection = get_object_or_404(Collection, slug=slug)
    instance = Link.objects.filter(collection=collection)

    if collection.privacy==True and collection.user != request.user:
        return HttpResponseForbidden()

    tags = []
    for ins in instance:
        for x in ins.tags.all():
            if x not in tags:
                tags.append(x)
    if tag:
        instance = instance.filter(tags__name__icontains=tag)
    context = {
        "collection_list": query_list,
        "form_board": form_board,
        "form_link": form_link,
        "instance": instance,
        "slug": collection.slug,
        "collection": collection,
        "tags": tags,
    }
    return render(request, "board.html", context)


def search_link(request, slug=None):
    if request.GET:
        collection = get_object_or_404(Collection, slug=slug)
        instance = Link.objects.filter(collection=collection)
        query = request.GET.get("q")
        instance = instance.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(link__icontains=query)
        ).distinct()
        data = serializers.serialize('json', list(instance), fields=('link', 'title', 'domain', 'tags', 'img'))
        return HttpResponse(data, content_type="application/json")


@csrf_exempt
def link_add(request, slug=None):
    """
    Fetching Title and Screenshot(selenium webdriver, phantomjs) of the link & saving it,
    Cutting the domain name from the link string. Saving the title, link, img path, domain name in database,
    Fethcing img, compressing it and saving it back(PIL Image),
    Attaching the tags with link.

    @param request: Post request
    @param slug:    For getting the correnponding the collection(for foreign key field of Link model and 
                    creating a directory for the image by it's id)
    @return:    json response to the ajax request.

    """
    collection = get_object_or_404(Collection, slug=slug)
    print ('Working')
    if request.POST:
        link = request.POST.get('link')
        if not(link.startswith('http://') or link.startswith('https://')):
            link = 'http://'+link
        
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=any'])
        driver.set_window_position(0, 0)
        driver.set_window_size(1024, 720)
        driver.get(link)
        
        title = request.POST.get('title')
        if not title:
            title = driver.title.encode("utf-8")

        img_id = Link.objects.first()
        img_name = str(img_id.id + 1)
        img = "/static/img/images/" + img_name + ".png"
        domain = '{uri.netloc}'.format(uri=urlparse(link))
        if domain.startswith('www'):
            domain = domain[4:]

        instance = Link.objects.create(
            title=title,
            link=link,
            img= img,
            domain=domain,
            collection=collection,
        )
        driver.save_screenshot("./static/img/images/" + img_name + '.png')
        im = Image.open("./static/img/images/" + img_name + '.png')
        im = im.crop((0,0,1000,1000))
        im = im.resize((300, 300), Image.ANTIALIAS)
        im.save("./static/img/images/" + img_name + '.png')
        
        tags = request.POST.getlist('tags[]')
        for tag in tags:
            x, created = Tag.objects.get_or_create(name = tag)
            instance.tags.add(x)
        
        data = {
            'link': link,
            'title': title,
            'tags': tags,
            'image': img,
            'domain': domain,
            'id': instance.id,
            }
        return HttpResponse(json.dumps(data), content_type="application/json")
