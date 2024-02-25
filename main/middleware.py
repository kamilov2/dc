# import hashlib
# from django.http import HttpResponseForbidden
# from .models import Profile
# from django.shortcuts import render



# class UniqueDeviceMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         device_info = f"{request.META.get('HTTP_USER_AGENT')}_{request.META.get('REMOTE_ADDR')}"
#         device_id = hashlib.sha256(device_info.encode()).hexdigest()

#         if not request.session.get('device_id'):
#             profile, created = Profile.objects.get_or_create(device_id=device_id, name=device_info)
#             request.session['device_id'] = device_id

#             if created:
#                 print(f"New profile created: {profile}")
#             else:
#                 print(f"Existing profile retrieved: {profile}")

#         request.device_id = device_id
#         response = self.get_response(request)
#         return response



# class BlockOtherDevicesMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):       
#         current_device_id = getattr(request, 'device_id', None)
#         profile = Profile.objects.filter(device_id=current_device_id).first()

#         if profile and profile.permission:  
#             response = self.get_response(request)
#             return response
#         else:
#             return HttpResponseForbidden('Siz admin tomonidan bloklangan usersiz!')


# middleware.py

import sentry_sdk
from django.http import JsonResponse

def sentry_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            response = JsonResponse({'error': 'Internal Server Error'}, status=500)
        return response

    return middleware

