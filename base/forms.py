from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room #models'daki Room modelimiz
        fields = '__all__' #bütün değiştirilebilir alanları almak yerine alanları biz belirlemek istersek
        # fields = ['name', 'description', 'host'] vb. şeklinde de gösterebiliriz.