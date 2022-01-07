import jwt
import datetime

from django.contrib.auth.models import User

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Address

from .serializers import AddressSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid Password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }

        token = jwt.encode(payload, 'SECRET', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Access for authorized user only')

        try:
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access for authorized user only')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        token = request.COOKIES.get('jwt')
        # print(request.data)
        recieved_payload= request.data.dict()

        if not token:
            raise AuthenticationFailed('Access for authorized user only')

        try:
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access for authorized user only')

        user = User.objects.filter(id=payload['id'])

        if recieved_payload.get('address', None) is not None:
            address = Address.objects.filter(user=user.first())
            address.update(description=recieved_payload['address'])
            return Response(AddressSerializer(address.first()).data)

        if recieved_payload.get('username', None) is not None or recieved_payload.get('email', None) is not None:
            user.update(**recieved_payload)
            return Response(UserSerializer(user.first()).data)

    def delete(self, request):
        token = request.COOKIES.get('jwt')
        recieved_payload = request.data.dict()

        if not token:
            raise AuthenticationFailed('Access for authorized user only')

        try:
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access for authorized user only')

        user = User.objects.filter(id=payload['id'], **recieved_payload)
        user.delete()

        return Response("Deleted")


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logged Out'
        }

        return response
