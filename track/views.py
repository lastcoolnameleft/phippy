from django.shortcuts import render
from .models import Toy, ToyLocation

def index(request):
    """ / path """
    toy_location_list = ToyLocation.objects.all()
    #toy_location_json = serializers.serialize('json', toy_location_list)
    map_data = {
        'width': '100%',
        'height': '800px',
        'focus_lat': 23,
        'focus_long': 10,
        'focus_zoom': 2,
        'location_list': [], #toy_location_json,
        'toy_location_id': 0,
    }

    return render(request, 'toy/main.html', {'map': map_data})
