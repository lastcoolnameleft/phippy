""" Form for Toyiehunt """
from django import forms
import datetime

class ToyForm(forms.Form):
    """ Form for Phippy Phinder.  """
    toy_id = forms.IntegerField(label='Toy #')
    name = forms.CharField(label='Toy name', max_length=100, disabled=False, required=False)
    location = forms.CharField(label='Location', max_length=100)
    date_time = forms.DateTimeField(label='Date/Time',
                                    initial=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
    lat = forms.FloatField(label='Latitude')
    lng = forms.FloatField(label='Longitude')
    comments = forms.CharField(widget=forms.Textarea(attrs={'cols': '50', 'rows': '5'}))
    image = forms.ImageField(required=False)