from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm
from collection.models import Collection


def login_view(request):
    next_request = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next_request:
            return redirect(next_request)
        collection = Collection.objects.filter(user=request.user)
        link = collection.first().slug
        return redirect("/"+link+'/')
    return render(request, 'form.html', {'form': form, 'title': title})


def register_view(request):
    next_request = request.GET.get('next')
    title = 'Register'
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        if next_request:
            return redirect(next_request)
        collection = Collection.objects.filter(user=request.user)
        link = collection.first().slug
        return redirect("/"+link+"/")

    context = {
        'form': form,
        'title': title,
    }

    return render(request, 'form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
