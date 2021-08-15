from web.views import AddPersonalPlayList, AddPlayList, addrecentmusic, editprofile, joingroup, Dashboardpage, AddMusic, addfavorite, deletemusic, deleteplaylist, favoritve ,group, leavegroup, newgroup, playlistshow, profile, removemember ,search ,personal ,ingroup ,updategroup
from django.urls import path

urlpatterns = [
    path('' , Dashboardpage , name="dashboard"),
    path('group/<int:id>' , ingroup , name='ingroup'),
    path('group/' , group , name="group"),
    path('search/', search , name='search'),
    path('favorite/' , favoritve , name='favorite' ),
    path('personal/' , personal , name='personal' ),
    path('profile/<str:username>' , profile , name='profile'),
    path('group/addgroup/' , newgroup , name='newgroup'),
    path('group/updategroup/<int:id>' , updategroup , name='updategroup'),
    path('group/leavegroup/<int:id>' , leavegroup , name='leavegroup'),
    path('group/removemember/<int:id>/<str:username>' , removemember , name='removemember'),
    path('playlist/<int:id>' , playlistshow , name='inplaylist'),
    path('addtofav/<int:id>' , addfavorite , name="addfavorite"),
    path('addmusic/<int:id>' , AddMusic , name='addmusic'),
    path('deletemusic/<int:musicid>/<int:playlistid>' , deletemusic , name="deletemusic") ,
    path('addplaylist/<int:id>' , AddPlayList , name="addplaylist"),
    path('deleteplaylist/<int:id>' , deleteplaylist , name="deleteplaylist"),
    path('join/<str:joincode>' , joingroup , name='joingroup'),
    path('editprofile/<str:username>' , editprofile , name='editprofile'),
    path('addrecentmusic/' , addrecentmusic , name='addrecentmusic') ,
    path('personal/playlist/add/' , AddPersonalPlayList , name="AddPersonalPlayList")
]
