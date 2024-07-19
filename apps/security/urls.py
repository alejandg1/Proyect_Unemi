from django.urls import path
from apps.security.views import user_management, management_options

app_name = "security"
urlpatterns = [
    path('', management_options.OptionsTemplateView.as_view(), name="options" ),
    path('users/', user_management.UserListView.as_view(), name="user" ),
    path('users/create/', user_management.UserCreateView.as_view(), name="user_create" ),
    path('users/update/<int:pk>/', user_management.UserUpdateView.as_view(), name="user_update" ),
    path('users/delete/<int:pk>/', user_management.UserDeleteView.as_view(), name="user_delete" ),
]