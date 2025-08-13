from rest_framework import serializers
from .models import Guest, Movie, Reservation, Post


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name', 'mobile'] # pk çok yanlış bir şey, değiştireceğim. uuid, slug kullanacğaım


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    

