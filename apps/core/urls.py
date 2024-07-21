from django.urls import path
from apps.core.views import collage, home, about, profile, logs,team,chat
from django.conf.urls.static import static
from django.conf import settings
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
    path('collage/', collage.CollageTemplateView.as_view(), name="collage"),
    path('about/', about.AboutTemplateView.as_view(), name="about"),
    path('login/',logs.LoginTemplateView.as_view(),name = "login"),
    path('data_response/', about.TeacherDataResponse.as_view(), name="response"),
    path('team/', team.TeamTemplateView.as_view(), name="team"),
    path('chat/', chat.ChatTemplateView.as_view(), name="chat"),
    path('withoutpermissions/', logs.NoPermissions.as_view(),
         name="withoutpermissions"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
