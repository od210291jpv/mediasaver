# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from models import ImageFile
from models import UserAccount
from Home.settings import PORTAL_URL
from django.http import HttpResponseForbidden
from models import ImageFile, UserAccount
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json

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
    images_list = []
    all_images = ImageFile.objects.all()
    for x in all_images:
        images_list.append([x.path.url, x.name, x.id])
    return JsonResponse({"publications": images_list})


def create_user(request):
    if request.method == "POST":
        body = json.loads(request.body)
        registered_usr = User.objects.filter(username=body['username'])
        if len(registered_usr) > 0:
            return HttpResponseForbidden("User already exists")
        else:
            user = User.objects.create_user(body['username'], body['email'], body['password'], is_active=False)
            user.save()
            user_acc = UserAccount(name=body['username'])
            user_acc.save()
            return JsonResponse({'state': 'ok'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def login(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = authenticate(username=body['Username'], password=body['Password'])
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


def get_my_posts(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if User.objects.filter(username=body['username']) and UserAccount.objects.filter(name=body['username']) is not None:
            images = ImageFile.objects.filter(publisher__name=body['username'])
            images_dict = {}
            counter = 0
            for x in images:
                images_dict[counter] = x.path.url
                counter += 1
            return JsonResponse(images_dict)
        else:
            return JsonResponse({'state': 'error', 'reason': 'authentication failed'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def get_my_favorites(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if UserAccount.objects.filter(name=body['Username']) is not None:
            images = ImageFile.objects.filter(favorite__name=body['Username'])
            images_list = []
            for x in images:
                images_list.append([x.path.url, x.name, x.id])
            return JsonResponse({"favorites": images_list})
        else:
            return JsonResponse({'state': 'error', 'reason': 'authentication failed'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def add_to_favorites(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = UserAccount.objects.get(name=body['username'])
        if user is not None:
            image = ImageFile.objects.get(id=body['image_id'])
            if image:
                image.favorite.add(user.id)
                return JsonResponse({'state': 'ok'})
            else:
                return JsonResponse({'state': 'error', 'reason': 'No image found'})
        elif user is None:
            return JsonResponse({'state': 'error', 'reason': 'authentication failed'})
        else:
            return JsonResponse({'state': 'error', 'reason': 'Error'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def remove_from_favorites(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = UserAccount.objects.get(name=body['username'])
        if user is not None:
            image = ImageFile.objects.get(id=body['image_id'])
            if image:
                image.favorite.remove(user.id)
                return JsonResponse({'state': 'ok'})
            else:
                return JsonResponse({'state': 'error', 'reason': 'No image found'})
        else:
            return JsonResponse({'state': 'error', 'reason': 'authentication failed'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def is_favorite(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        requested_image = ImageFile.objects.get(id=body['image_id'])
        if UserAccount.objects.filter(name=body['username']) is not None:
            images = ImageFile.objects.filter(favorite__name=body['username'])
            if requested_image and requested_image in images:
                return JsonResponse({'state': 'true'})
            else:
                return JsonResponse({'state': 'false'})
    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})


def remove_image(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = UserAccount.objects.get(name=body['username'])
        if user is not None:
            image = ImageFile.objects.get(id=body['image_id'])
            if image:
                ImageFile.objects.remove(id=image)

    else:
        return JsonResponse({'state': 'error', 'reason': 'incorrect request method'})
