from django.urls import path
from apps.core.views import (
    collage, home, about, profile, logs, team, chat, asist)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'
urlpatterns = [
    path('', home.HomeTemplateView.as_view(), name="home"),
    path('asist/', asist.AsistTemplateView.as_view(), name="asist"),
    path('collage/', collage.CollageTemplateView.as_view(), name="collage"),
    path('profile/', profile.ProfileTemplateView.as_view(), name="profile"),
    path('about/', about.AboutTemplateView.as_view(), name="about"),
    path('login/', logs.LoginTemplateView.as_view(), name="login"),
    path('logout/', logs.Logout, name="logout"),
    path('clear/', logs.DelTemps, name="clear"),
    path('mkcol/', collage.MakeCollage, name="mkcol"),
    path('data_response/', about.TeacherDataResponse.as_view(),
         name="response"),
    path('team/', team.TeamTemplateView.as_view(), name="team"),
    path('chat/', chat.ChatTemplateView.as_view(), name="chat"),
    path('withoutpermissions/', logs.NoPermissions.as_view(),
         name="withoutpermissions"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
