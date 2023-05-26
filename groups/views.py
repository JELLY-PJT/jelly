from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Group
from .serializers import UserGroupListSerializer, GroupSerializer


@api_view(['GET'])
def index(request):
    serializer = UserGroupListSerializer(request.user)
    return Response(serializer.data)


# class GroupDetail(APIView):
#     def get_object(self, )

#     def get(self, request):
#         pass