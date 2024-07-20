from django.urls import path
from apps.core.views import home, modules, about, profile, logs
# from apps.core.models import User
# from django.http import HttpResponse


# def print_user_permissions(request):
#     user = User.objects.get(username=request.user.username)
#     permissions = user.get_all_permissions()
#     print("Permisos del usuario {}: {}".format(user.username, permissions))
#
#     return HttpResponse("Permisos impresos en la consola.")


app_name = 'core'
urlpatterns = [
    path('', home.HomeTemplateView.as_view(), name="home"),
    path('modules/', modules.ModulesTemplateView.as_view(), name="modules"),
    path('about/', about.AboutTemplateView.as_view(), name="about"),
    path('profile/', profile.ProfileTemplateView.as_view(), name="profile"),
    path('login/', logs.LoginView.as_view(), name="login"),
    path('withoutpermissions/', logs.NoPermissions.as_view(),
         name="withoutpermissions"),
]
