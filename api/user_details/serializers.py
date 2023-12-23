from rest_framework import serializers
from customer.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['name','email','employee']