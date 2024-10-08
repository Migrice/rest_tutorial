# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.conf import settings
import requests
from django.shortcuts import redirect, render
import jwt
from jwt import InvalidTokenError


# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)







# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer

# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




from django.shortcuts import redirect
from snippets.models import Snippet, TransportCompany
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, TransportCompanySerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session



class SnippetList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class=UserSerializer()
    
    


def login_view(request):
    authorization_url = (
        f"{settings.CASDOOR_AUTHORIZATION_ENDPOINT}?"
        f"response_type=code&client_id={settings.CASDOOR_CLIENT_ID}&"
        f"redirect_uri={settings.CASDOOR_REDIRECT_URI}&state=Tutorial"
    )
    return redirect(authorization_url)


def decode_access_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except InvalidTokenError:
        return None

def callback_view(request):
    code = request.GET.get('code')

    # Échanger le code contre un token
    token_response = requests.post(
        settings.CASDOOR_TOKEN_ENDPOINT,
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.CASDOOR_CLIENT_ID,
            'client_secret': settings.CASDOOR_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.CASDOOR_REDIRECT_URI,
        }
    )
    
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Récupérer les informations utilisateur
    userinfo_response = requests.get(
        settings.CASDOOR_USERINFO_ENDPOINT,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    userinfo = userinfo_response.json()
    decoded_token = decode_access_token(access_token)
    
    if decoded_token:
        username = decoded_token.get('name')
        email = decoded_token.get('email')
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email":email}
        )
        
        if created:
            user.set_unusable_password()
            user.save()

        if user is not None:
            login(request, user)
            
            return redirect('snippets')
            #return render(request, 'home.html', {'userinfo': userinfo})
        
        raise Exception("Failed to authenticate the user")
    
    raise Exception("Failed to access token")
     
    return redirect('snippets')
 


def logout_view(request):
    logout(request)
    # clear the user's session data
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('login')

@csrf_exempt
@api_view(['GET', 'POST'])
def transport_companies_list(request):
    """
    List all transport companies, or create a new one.
    """

    if request.user.is_authenticated:
        
        if request.method == 'GET':
            transports = TransportCompany.objects.all()
            serializer = TransportCompanySerializer(transports, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = TransportCompanySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    else:
        return redirect('login')