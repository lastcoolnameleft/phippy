""" Views for Django """
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from .models import Toy, ToyLocation, ToyLocationPhoto
from .forms import ToyForm
from track import media
from haversine import haversine

def index(request):
    """ / path """
    toy_location_list = ToyLocation.objects.all()
    toy_location_json = serializers.serialize('json', toy_location_list)
    map_data = {
        'width': '100%',
        'height': '800px',
        'focus_lat': 23,
        'focus_long': 10,
        'focus_zoom': 2,
        'location_list': toy_location_json,
        'toy_location_id': 0,
    }

    return render(request, 'toy/main.html', {'map': map_data})

def detail(request, toy_id):
    """ /toy/# path """
    toy = get_object_or_404(Toy, pk=toy_id)
    photos = ToyLocationPhoto.objects.filter(toy_location__toy_id=toy_id)

    # SCREW YOU DJANGO FOR NOT SUPPORT USING SELECT_RELATED + SERIALIZATION
    # https://medium.com/@PyGuyCharles/python-sql-to-json-and-beyond-3e3a36d32853
    # https://stackoverflow.com/questions/34666892/trying-to-serialize-a-queryset-that-uses-select-related-cant-obtain-fields-o
    # https://docs.djangoproject.com/en/2.1/topics/serialization/#serialization-of-natural-keys
    toy_location_list = ToyLocation.objects.filter(toy_id=toy_id)
    toy_location_json = serializers.serialize('json', toy_location_list, use_natural_foreign_keys=True)
    map_data = {
        'width': '100%',
        'height': '400px',
        'focus_lat': 0,
        'focus_long': 0,
        'focus_zoom': 2,
        'location_list': toy_location_json,
        'toy_location_id': 0,
    }
    toy_dropdown_list = Toy.objects.all()

    return render(request, 'toy/detail.html',
                  {'toy': toy, 'photos': photos, 'map': map_data,
                   'toy_location_list': toy_location_list, 'toy_list': toy_dropdown_list})

def location(request, toy_location_id):
    """ Show /toy/$toy_id """
    toy_location = get_object_or_404(ToyLocation, id=toy_location_id)

    photos = ToyLocationPhoto.objects.filter(toy_location_id=toy_location_id)

    toy_location_list = ToyLocation.objects.filter(toy_id=toy_location.toy_id)
    toy_location_json = serializers.serialize('json', toy_location_list, use_natural_foreign_keys=True)
    map_data = {
        'width': '100%',
        'height': '400px',
        'focus_lat': 0,
        'focus_long': 0,
        'focus_zoom': 15,
        'location_list': toy_location_json,
        'toy_location_id': toy_location_id,
    }
    toy_dropdown_list = Toy.objects.all()

    return render(request, 'toy/location.html',
                  {'photos': photos, 'map': map_data, 'toy': toy_location.toy,
                   'toy_location': toy_location, 'toy_location_list': toy_location_list,
                   'toy_list': toy_dropdown_list})

def toy_list(request):
    """ lists all toys """
    toys = Toy.objects.all()
    return render(request, 'toy/list.html', {'toy_list': toys})

def faq(request):
    """ shows faq """
    return render(request, 'toy/faq.html')

@login_required
def mark(request):
    """ Adds a toy, location, photo and link from webform """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ToyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_or_existing = form.cleaned_data['new_or_existing']
            name = form.cleaned_data['name']
            if ( new_or_existing == 'new'):
                toy = Toy(name=name, approved='Y',
                          create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          comments='')
                toy.save()
            else:
                toy = Toy.objects.get(name=name)

            toy_location = ToyLocation(toy=toy,
                                         latitude=form.cleaned_data['lat'],
                                         longitude=form.cleaned_data['lng'],
                                         location=form.cleaned_data['location'],
                                         date_time=form.cleaned_data['date_time'],
                                         comments=form.cleaned_data['comments'],
                                         user=request.user,
                                         approved='Y')
            toy_location.save()
            if request.FILES and request.FILES['image']:
                photo_info = media.handle_uploaded_file(request.FILES['image'], toy.id,
                                                        toy.name, form.cleaned_data['comments'])
                toy_location_photo = ToyLocationPhoto(toy_location=toy_location,
                                                      flickr_photo_id=photo_info['id'],
                                                      flickr_thumbnail_url=photo_info['sizes']['Small 320']['source'])
                toy_location_photo.save()


            # redirect to a new URL:
            return HttpResponseRedirect('/location/' + str(toy_location.id))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ToyForm()

    map_data = {
        'width': '100%',
        'height': '400px',
        'focus_lat': 35,
        'focus_long': -30,
        'focus_zoom': 1,
        'location_list': [],
        'toy_location_id': 0,
    }
    return render(request, 'toy/mark.html', {'form': form, 'map': map_data})

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

def login(request):
    """Home view, displays login mechanism"""
    return render(request, 'toy/login.html')

def profile(request):
    """ Show profile data """
    print(request.user.username)
    return render(request, 'toy/profile.html', {'user': request.user})