from django.urls import path
from snippets.views import SnippetList, SnippetDetail, UserList, UserDetail, transport_companies_list, login_view, callback_view

urlpatterns = [
    
    path('snippets/', SnippetList.as_view(), name="snippets"),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('companies/',transport_companies_list, name="list-create-companies" ),
    path('login/', login_view, name='login'),
    path('callback/', callback_view, name='callback'),
    
]

