from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from apps.core.models import Teacher, Research, Projects, Articles, GeneratedImage
# Register your models here.

admin.site.register(ContentType)
admin.site.register(Teacher)
admin.site.register(Research)
admin.site.register(Projects)
admin.site.register(Articles)
admin.site.register(GeneratedImage)