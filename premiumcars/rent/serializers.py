from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Car, Rental


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'hp', 'price', 'image']


class RentalSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='pk')
    car_model = serializers.ReadOnlyField(source='car_id.model')
    user_firstname = serializers.ReadOnlyField(source='user_id.first_name')
    user_lastname = serializers.ReadOnlyField(source='user_id.last_name')
    user_email = serializers.ReadOnlyField(source='user_id.email')

    class Meta:
        model = Rental
        fields = ['id','car_model','total_price', 'user_id', 'user_firstname', 'user_lastname', 'user_email','borrow_date',
                  'return_date']


class RentalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental
        fields = ['car_id', 'total_price', 'borrow_date','return_date']


class RentalDeleteSerializer(serializers.ModelSerializer):
    rent_id = serializers.ReadOnlyField(source='rental_pk')

    class Meta:
        model = Rental


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
