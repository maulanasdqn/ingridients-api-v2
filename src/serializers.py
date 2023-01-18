from .models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Ingridients

class IngridientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingridients
		fields = ['qty', 'weight', 'name', 'categories']