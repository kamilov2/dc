import time
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from asgiref.sync import async_to_sync
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from jose import jwt
from channels.db import database_sync_to_async
from django.core.serializers import serialize
from django.http import StreamingHttpResponse
from async_generator import async_generator, yield_
from django.db.models import Q
from .models import *
from .serializers import *

class AsyncExample(APIView):
    permission_classes = [AllowAny]

    @async_to_sync
    async def get(self, request):
        try:
            start_time = time.time()

            profiles = await self.get_profiles()

            response_data = self.get_streaming_data(profiles)

            jwt_payload = {"profiles": await self.serialize_profiles(profiles)}
            secret_key = settings.SECRET_KEY_JWT
            jwt_token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
            jwt_decode = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
            print(jwt_decode)

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"AsyncExample executed in {elapsed_time} seconds")

            return Response({"message": "Async response", "jwt_token": jwt_payload}, status=status.HTTP_200_OK)

        except Exception as e:
            await self.handle_error(request, e)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @database_sync_to_async
    def get_profiles(self):
        return Profile.objects.filter(permission=True).only('name', 'device_id', 'permission').defer('created_at', 'updated_at')[:1000]

    @database_sync_to_async
    def serialize_profiles(self, profiles):
        serializer = AsyncProfileSerializer(profiles, many=True)
        return serializer.data

    async def get_streaming_data(self, profiles):
        for profile in profiles:
            yield self.serialize_profiles([profile])

class Example(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            start_time = time.time()

            # Получите первые 1000 объектов, удовлетворяющих условию permission=True
            filtered_profiles = Profile.objects.filter(permission=True)[:1000]

            # Сериализуйте объекты Profile
            serializer = ProfileSerializer(filtered_profiles, many=True)
            serialized_data = serializer.data



            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Вывести подробности об ошибке в журнал
            import traceback
            traceback.print_exc()
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)