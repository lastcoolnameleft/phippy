from django.contrib import admin
from .models import Toy, ToyLocation, ToyLocationLink, ToyLocationPhoto

admin.site.register(Toy)
admin.site.register(ToyLocation)
admin.site.register(ToyLocationLink)
admin.site.register(ToyLocationPhoto)
