from django.urls import path
from apps.core.views import costumer, home, modules, about, profile, logs
from apps.security.models import User
from django.http import HttpResponse

def print_user_permissions(request):
    user = User.objects.get(username= request.user.username)  # Reemplaza 'nombre_de_usuario' con el nombre del usuario que quieres verificar
    permissions = user.get_all_permissions()
    print("Permisos del usuario {}: {}".format(user.username, permissions))
    
    return HttpResponse("Permisos impresos en la consola.")


app_name = 'core'
urlpatterns = [
    path('print_user_permissions/', print_user_permissions, name='print_user_permissions'),
    path('costumer/', costumer.CostumerList.as_view(), name= "costumer"),
    path('costumer/new_costumer/', costumer.CostumerCreate.as_view(), name="new_costumer"),
    path('costumer/update_costumer/<int:pk>/', costumer.CostumerUpdate.as_view(), name="update_costumer"),
    path('costumer/delete_costumer/<int:pk>/', costumer.CostumerDelete.as_view(), name="delete_costumer"),
    path('', home.HomeTemplateView.as_view(), name ="home"),
    path('modules/', modules.ModulesTemplateView.as_view(), name="modules"),
    path('about/', about.AboutTemplateView.as_view(), name="about"),
    path('profile/', profile.ProfileTemplateView.as_view(), name= "profile"),
    path('login/', logs.LoginView.as_view(), name= "login"),
    path('register/', logs.RegisterView.as_view(), name= "register"),
    path('logout/', logs.LogoutView.as_view(), name= "logout"),
    path('withoutpermissions/', logs.NoPermissions.as_view(), name= "withoutpermissions"),
]
