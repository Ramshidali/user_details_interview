from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Profile
from customer.views import encrypt_message
from api.user_details.serializers import ProfileSerializer

#get and ceate view
@api_view(['GET', 'POST'])
def customer(request):
    """
    List all code profiles, or create a new profile.
    """
    if request.method == 'GET':
        if Profile.objects.filter().exists():
            instances = Profile.objects.all()
            serializer = ProfileSerializer(instances, many=True)

            response_data = {
                "StatusCode": 200,
                "message" : "User details found",
                "success" : True,
                "profile" : serializer.data
                }
            return Response(response_data, status=status.HTTP_200_OK)
        else :
            response_data = {
                "StatusCode": 200,
                "message" : "user details not found",
                "success" : False,
                "profile" : []
                }
            return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        profile_serializer = ProfileSerializer(data=request.data)
        email = request.data["email"]
        password = request.data["password"]
        print(email,type(email))
        print(password,type(password))
        if not User.objects.filter(username=email).exists():
            if profile_serializer.is_valid():
                user_data = User.objects.create_user(
                    username=email,
                    password=password,
                )
                profile_serializer.save(
                    user = user_data,
                    password = encrypt_message(password)
                )
                response_data = {
                    "StatusCode": 200,
                    "message" : "user created successfully",
                    "success" : True,
                }
            return Response(profile_serializer, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "StatusCode": 200,
            "message" : "profile already exist",
            "success" : False,
            }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def edit_profile(request):
    """
    Retrieve, update or delete a code profile.
    params : user_id
    """
    if request.GET.get("user_id") :
        user_id = request.GET.get("user_id")

        try:
            profile = Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)

            response_data = {
                "StatusCode": 200,
                "message" : "profile details found",
                "success" : True,
                "profile" : serializer.data
                }
            return Response(response_data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)

            if profile_serializer.is_valid():
                profile = profile_serializer.save()

                response_data = {
                    "StatusCode": 200,
                    "message" : "profile Updated successfully",
                    "user_id" : profile.name,
                    "success" : True,
                }

            else :
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'DELETE':
            if Profile.objects.filter(pk=user_id).exists():
                instance = Profile.objects.get(pk=user_id)
                User.objects.filter(username=instance.email).delete()
                instance.delete()

                response_data = {
                    "StatusCode": 200,
                    "message" : "profile deleted successfully",
                    "success" : True,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else :
                response_data = {
                    "StatusCode": 200,
                    "message" : "no profile found with this user_id",
                    "success" : False,
                }

                return Response(response_data, status=status.HTTP_200_OK)
    else :
        response_data = {
            "StatusCode": 400,
            "message" : "invalid body request",
            "success" : False,
        }

        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)