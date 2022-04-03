from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from ..models import CustomUser
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List Invites': '/my-invites/',
    }
    return Response(api_urls)


@login_required(login_url='api:api-overview')
@api_view(['GET'])
def api_invites(request):
    tasks = CustomUser.objects.filter(another_invite=CustomUser.objects.filter(phone=request.user).values('code_invite')[0]['code_invite'])
    serializer = UserSerializer(tasks, many=True)
    return Response(serializer.data)