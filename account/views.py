import os

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
            if User.objects.filter(Q(username=username) | Q(email_id=email_id)).exists():
                response = {
                    'message': 'username or email already taken',
                    'status': False,
                    'result': None
                }
                return JSONResponse(response, status=status.HTTP_409_CONFLICT)

            user = User.objects.create(username=username, email_id=email_id, first_name=first_name, last_name=last_name,
                                       profile_picture_url=profile_picture_url, password=password)

            result = UserAccountSerializer(instance=user).data
            result['token'] = Token.objects.create(user=user).key
            response = {
                'message': 'user created successfully',
                'status': True,
                'result': result
            }
            return JSONResponse(response)
        except Exception as e:
            response = {
                'message': 'An Error occurred',
                'status': False,
                'exception': e.message
            }
            return JSONResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
