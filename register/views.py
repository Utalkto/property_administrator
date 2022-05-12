from traceback import print_tb
from urllib import request, response
from django.http import JsonResponse
from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_role(request, format=None):
    data = {'role': request.user.role.role}
    return Response(data, status=status.HTTP_200_OK)
    