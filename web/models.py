from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .utils import get_file_upload_path
from random import randint
def get_default_avatar_img():
    return 'defaultavatar/1024px-Circle-icons-profile.svg.png'

def random_string(num):
    final = ''
    li = 'abcdefghijklmnopqrstuxwzy1234567890'
    for i in range(1,num+1):
        random_index = randint(1,34)
        final += li[random_index]
    return final

def get_default_group_avatar_img():
    return 'defaultavatar/grouplogo.png'

def get_default_playlist_cover_img():
    return 'defaultavatar/sampleplaylistavatar.jpg'


class songususer(models.Model):
    user = models.OneToOneField(User , related_name='user' , on_delete=models.CASCADE )
    avatar = models.ImageField(upload_to = 'profiles' , null = True , blank = True , default = get_default_avatar_img )
    


    def __str__(self):
        return self.user.username

class group(models.Model):
    name = models.CharField(max_length=256)
    is_private = models.BooleanField(default=False , blank=True , null=True)
    description = models.TextField(blank=True , null=True)
    cdate = models.DateTimeField(auto_now_add=True)
    joincode = models.CharField(max_length=50 ,blank=True , null=True , unique=True)
    member = models.ManyToManyField(songususer , related_name='groupss' , null=True , blank=True)
    owner = models.ForeignKey(songususer , on_delete=models.CASCADE , null=True , blank=True)
    avatar = models.ImageField(upload_to = 'groupprofiles' , null = True , blank = True , default = get_default_group_avatar_img )
    
    def __str__(self):
        return self.name

    def NumOfPlayLists(self):
        return self.playlist_set.all().count()

    def save(self, *args, **kwargs):
        if self.joincode == None :
            randomstr = random_string(8)
            objs = group.objects.filter(joincode = randomstr)
            while(objs.count() != 0):
                randomstr = random_string(8)
                objs = group.objects.filter(joincode = randomstr)
            self.joincode = randomstr
        super(group, self).save(*args, **kwargs)


class playlist(models.Model):
    name = models.CharField(max_length=256)
    cdate = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(group , on_delete=models.CASCADE )
    avatar = models.ImageField(upload_to = 'playlistcover' , null = True , blank = True , default = get_default_playlist_cover_img )
    favoritve = models.ManyToManyField(songususer , related_name="favorites" , null = True , blank = True)
    def __str__(self):
        return self.name

    def NumOfSongs(self):
        return self.song_set.all().count()

    


class song(models.Model):
    file = models.FileField(_('File'), upload_to=get_file_upload_path, null=True, blank=True)
    name = models.CharField(max_length=256, blank=True, null= True)
    artist = models.CharField(max_length=256, blank=True, null= True)
    file_link = models.URLField(null=True, blank=True)
    playlist = models.ForeignKey(playlist, on_delete=models.CASCADE, blank=True, null= True)
    is_suggested = models.BooleanField(default=False, null=True, blank=True)
    recent_music = models.ManyToManyField(songususer, related_name='recent_music', null=True, blank=True)
    owner = models.ForeignKey(songususer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        get_latest_by = 'date'
    def __str__(self):
        return self.name
    def clean(self):
        cleaned_data = super().clean()
        
        if not self.file and not self.file_link:  # This will check for None or Empty
            raise ValidationError({'file': 'Even one of file or file link should have a value.'})
        if not self.file_link == None and self.file_link[-4:] != '.mp3':
            raise ValidationError({'file_link': 'only mp3 files accepted'})

class RecentMusic(models.Model):
    song = models.ForeignKey(song , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(songususer , on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.user.username