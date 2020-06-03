from django.urls import path
from user.views import CreateUserView, CreateAuthenticationToken, \
    RetrieveAndUpdateView

app_name = 'user'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateAuthenticationToken.as_view(), name='token'),
    path('me/', RetrieveAndUpdateView.as_view(), name='me'),
]
