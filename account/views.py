from django.contrib.auth import authenticate
from rest_framework import status
from django.db import IntegrityError
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
                'message': 'Username or Email Already Taken',
                'status': False,
                'result': None
            }
            return JSONResponse(response, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, email_id=email_id, first_name=first_name,
                                        last_name=last_name,
                                        profile_picture_url=profile_picture_url, password=password)
        # TODO send email using celery
        response = {
            'message': 'user created successfully',
            'status': True,
            'result': None
        }
        return JSONResponse(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:

            result = UserAccountSerializer(instance=user).data
            result['token'] = Token.objects.create(user=user).key
            response = {
                'message': 'User  Logged In Successfully',
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
            'message': 'User Logged Out Successfully',
            'status': True,
            'result': None
        }
        return JSONResponse(response)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.query_params['user_id']
        user = User.objects.filter(id=user_id).first()
        if user:
            result = UserAccountSerializer(instance=user).data
            response = {
                'message': 'User Details Fetched Successfully',
                'status': True,
                'result': result
            }
            return JSONResponse(response)
        else:
            response = {
                'message': 'No User Exist With The Given Id',
                'status': False,
                'result': None
            }
            return JSONResponse(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def post(self, request):
        user_details = request.data['user_details']
        user = request.user
        try:
            for attr, value in user_details.iteritems():
                setattr(user, attr, value)
            user.save()
            response = {
                'message': 'User Details Updated Successfully',
                'status': True,
                'result': None
            }
            return JSONResponse(response)
        except IntegrityError:
            response = {
                'message': 'Username or Email Already Taken',
                'status': False,
                'result': None
            }
            return JSONResponse(response, status=status.HTTP_409_CONFLICT)



