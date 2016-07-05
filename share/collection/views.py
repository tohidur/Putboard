from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CollectionForm, LinkForm
from .models import Collection, Link, Tag
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from selenium import webdriver

# Create your views here.

@login_required
def collection_create(request):
    form = CollectionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "collection_form.html", context)


def collection_list(request):
    # query_list = Collection.objects.active()
    # if request.user.is_superuser:
    #     query_list = Post.objects.all()

    query_list = Collection.objects.all()

    query = request.GET.get("q")
    if query:
        query_list = query_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)|
            Q(description__icontains=query)
        ).distinct()

    context = {
        "collection_list": query_list,
        "title": "Collections",
    }
    return render(request, "collection_list.html", context)


def collection_detail(request, slug=None):
    collection = get_object_or_404(Collection, slug=slug)
    instance = Link.objects.filter(collection=collection)
    
    query = request.GET.get("q")
    if query:
        instance = instance.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(link__icontains=query)
        ).distinct()

    print instance
    context = {
        "instance": instance,
        "slug": collection.slug,
    }
    return render(request, "collection_detail.html", context)


def link_add(request, slug=None):
    collection = get_object_or_404(Collection, slug=slug)
    form = LinkForm(request.POST or None)
    if request.POST:
    	title = request.POST.get('title')
    	link = request.POST.get('link')
        


        # driver = webdriver.PhantomJS()
        # driver.set_window_position(0, 0)
        # driver.set_window_size(1024, 720)
        # driver.get('http://'+link)
        # driver.save_screenshot("./static/images/" + title + '.png')
  #   	instance = Link.objects.create(
  #   		title=title,
  #   		link=link,
  #   		collection=collection,
		# )
  #       tags = request.POST.getlist('tags')
  #       for tag in tags:
  #       	instance.tags.add(tag)
  #       return HttpResponseRedirect(instance.collection.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "link_form.html", context)
