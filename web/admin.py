from .models import RecentMusic, group, playlist, song , songususer
from django.contrib import admin

admin.site.register(group)
admin.site.register(songususer)
admin.site.register(playlist)
admin.site.register(song)
admin.site.register(RecentMusic)

