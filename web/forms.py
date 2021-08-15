from django import forms
from django.contrib.auth.models import User

from .models import group, playlist, song, songususer

class AddNewGroupForm(forms.ModelForm):
    class Meta:
        model = group
        fields = ['name' , 'description' , 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'name of group'}),
            'description' : forms.Textarea(attrs={'class': 'cutominput', 'placeholder' : 'Description ...'}),
            'avatar' : forms.FileInput(attrs={'class': 'imagefield'}),
        }

        labels = {
            'name' : '' ,
            'description' : '' ,
        }

class UpadateGroupForm(forms.ModelForm):
    class Meta:
        model = group
        fields = ['name' , 'description' , 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'name of group'}),
            'description' : forms.Textarea(attrs={'class': 'cutominput', 'placeholder' : 'Description ...'}),
            'avatar' : forms.FileInput(attrs={'class': 'imagefield'}),
        }

        labels = {
            'name' : '' ,
            'description' : '' ,
        }

class AddNewMusicForm(forms.ModelForm):
    class Meta:
        model = song
        fields = ['name' , 'file' , 'artist']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'name of music'}),
            'artist' : forms.TextInput(attrs={'class': 'cutominput', 'placeholder' : 'Artist'}),
            'file' : forms.FileInput(attrs={'class': 'imagefield'}),
        }

        labels = {
            'name' : '' ,
            'artist' : '' ,
        }


class AddNewPlayListForm(forms.ModelForm):
    class Meta:
        model = playlist
        fields = ['name' ,  'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'name of playlist'}),
            'avatar' : forms.FileInput(attrs={'class': 'imagefield'}),
        }

        labels = {
            'name' : '' ,
            'avatar' : 'cover image' ,
        }

class SearchInUsers(forms.Form):
    username = forms.CharField(max_length=264, label='' , widget= forms.TextInput(attrs={
        'type': "text" ,
        'class':"codeinput",
        'placeholder':"username ...",
    }))

class SearchInGroups(forms.Form):
    joincode = forms.CharField(max_length=100 , label='' , widget = forms.TextInput(attrs={
        'type': "text" ,
        'class':"codeinput",
        'placeholder':"joincode",
    }))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='' , widget= forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'email'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'cutominput', 'type': 'text' , 'placeholder' : 'username'}),            
        }

        labels = {
            'username' : '' ,
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = songususer
        fields = ['avatar']
        widgets = {
            'avatar' : forms.FileInput(attrs={'class': 'imagefield'}),           
        }

        labels = {
            'avatar' : 'profile' ,
        }