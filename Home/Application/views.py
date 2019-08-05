# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from models import ImageFile
from Home.settings import PORTAL_URL
from django.http import HttpResponseForbidden
from models import ImageFile
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    return render(request, 'index_new.html', {'portal_url': PORTAL_URL})


def test(request):
    all_images = ImageFile.objects.all()
    # tracks = AudioFile.objects.all()
    return render(request, 'Base.html', {'tracks': all_images, 'portal_url': PORTAL_URL})


def images_list(request):
    all_images = ImageFile.objects.all().exclude(category='hidden')
    paginator = Paginator(all_images, 9)
    page = request.GET.get('page')
    try:
        all_images = paginator.page(page)
    except PageNotAnInteger:
        all_images = paginator.page(1)
    except EmptyPage:
        all_images = paginator.page(paginator.num_pages)
    return render(request, 'main.html', {'images': all_images})


def upload_image(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            if not errors:
                image = ImageFile(name=request.POST['image_name'], category='', likes=0, path=request.FILES['image_path'])
                image.save()
                return HttpResponseRedirect(reverse('images'))
    else:
        return render(request, 'upload_image.html', {})


def hidden_list(request):
    all_images = ImageFile.objects.filter(category = 'hidden')
    paginator = Paginator(all_images, 9)
    page = request.GET.get('page')
    try:
        all_images = paginator.page(page)
    except PageNotAnInteger:
        all_images = paginator.page(1)
        pass
    except EmptyPage:
        all_images = paginator.page(paginator.num_pages)
    return render(request, 'hidden.html', {'images': all_images})


def images_json(request):
    images_dict = {}
    counter = 0
    all_images = ImageFile.objects.all()
    for x in all_images:
        images_dict[counter] = x.path.url
        counter += 1
    return JsonResponse(images_dict)


def create_user(request):
    if request.method == "POST":
        registered_usr = User.objects.filter(username=request.POST['username'])
        if len(registered_usr) > 0:
            return HttpResponseForbidden("User already exists")
            pass
        else:
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'], is_active=False)
            user.save()
            return JsonResponse({'state': 'ok'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return JsonResponse({'state': 'ok'})
        else:
            return JsonResponse({'state': 'error', 'reason': 'account disabled'})
    else:
        # the authentication system was unable to verify the username and password
        return JsonResponse({'state': 'error', 'reason': 'authentication failed'})
