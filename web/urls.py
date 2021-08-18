from web.views import (add_personal_playlist, add_playlist, 
                       add_recent_music, edit_profile, joingroup,
                       Dashboardpage, add_music, add_favorite,
                       delete_music, delete_playlist, favoritve,
                       group, leave_group, new_group, playlist_view,
                       profile, remove_member ,search ,personal,
                       in_group ,update_group
                        )
from django.urls import path

urlpatterns = [
    path('' , Dashboardpage , name="dashboard"),
    path('group/<int:id>' , in_group , name='ingroup'),
    path('group/' , group , name="group"),
    path('search/', search , name='search'),
    path('favorite/' , favoritve , name='favorite' ),
    path('personal/' , personal , name='personal' ),
    path('profile/<str:username>' , profile , name='profile'),
    path('group/addgroup/' , new_group , name='newgroup'),
    path('group/updategroup/<int:id>' , update_group , name='updategroup'),
    path('group/leavegroup/<int:id>' , leave_group , name='leavegroup'),
    path('group/removemember/<int:id>/<str:username>' , remove_member , name='removemember'),
    path('playlist/<int:id>' , playlist_view , name='inplaylist'),
    path('addtofav/<int:id>' , add_favorite , name="addfavorite"),
    path('addmusic/<int:id>' , add_music , name='addmusic'),
    path('deletemusic/<int:musicid>/<int:playlistid>' , delete_music , name="deletemusic") ,
    path('addplaylist/<int:id>' , add_playlist , name="addplaylist"),
    path('deleteplaylist/<int:id>' , delete_playlist , name="deleteplaylist"),
    path('join/<str:joincode>' , joingroup , name='joingroup'),
    path('editprofile/<str:username>' , edit_profile , name='editprofile'),
    path('addrecentmusic/' , add_recent_music , name='addrecentmusic') ,
    path('personal/playlist/add/' , add_personal_playlist , name="AddPersonalPlayList")
]
