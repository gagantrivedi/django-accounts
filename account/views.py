import os
from django.contrib.auth import authenticate
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q
from middleware.response import JSONResponse
from account.serializers import UserAccountSerializer
from account.models import User


class RegisterUserProfileView(APIView):
    def post(self, request):
        """ this method is used to register user profile """
        try:
            username = request.data['username']
            email_id = request.data['email_id']
            password = request.data['password']
            profile_picture_url = request.data['profile_picture_url']
            if 'first_name' in request.data:
                first_name = request.data['first_name'].strip()
            else:
                first_name = None
            if 'last_name' in request.data:
                last_name = request.data['last_name'].strip()
            else:
                last_name = None

            # check to see if user with the given email or username already exist
            # or the combination is in RESERVED_USERNAME_EMAIL_LIST
            if User.objects.filter(Q(username=username) | Q(email_id=email_id)).exists():
                response = {
                    'message': 'username or email already taken',
                    'status': False,
                    'result': None
                }
                return JSONResponse(response, status=status.HTTP_409_CONFLICT)

            user = User.objects.create(username=username, email_id=email_id, first_name=first_name, last_name=last_name,
                                       profile_picture_url=profile_picture_url, password=password)
            #TODO send email using celery
            response = {
                'message': 'user created successfully',
                'status': True,
                'result': None
            }
            return JSONResponse(response)
        except Exception as e:
            response = {
                'message': 'An Error occurred',
                'status': False,
                'exception': e.message
            }
            return JSONResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:

            result = UserAccountSerializer(instance=user).data
            result['token'] = Token.objects.create(user=user).key
            response = {
                'message': 'User Details Fetched Successfully',
                'status': True,
                'result': result
            }
            return JSONResponse(response)

        else:
            response = {
                'message': 'Provided Credentials Are Wrong',
                'status': False,
                'result': None
            }
            return JSONResponse(response, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()

        response = {
            'message': 'User Logged Ount Successfully',
            'status': True,
            'result': None
        }
        return JSONResponse(response)
