from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import RecentMusic, group as thegroups, song 
from web.models import songususer ,playlist
from web.forms import (
    AddNewGroupForm, 
    SearchInGroups, 
    SearchInUsers,
    UpadateGroupForm,
    AddNewMusicForm,
    AddNewPlayListForm,
    ProfileUpdateForm,
    UserUpdateForm
)

def add_recent_music_to_context(user, context):
    context['recentmusics'] = user.recentmusic_set.all().order_by('-date')


@login_required
def Dashboardpage(request):
    this_user = request.user.user
    groups = this_user.groupss.all()
    suggested = song.objects.filter(is_suggested=True).latest()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empty ,
        'suggested' : suggested ,
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/Dashboard.html', context)

@login_required
def group(request):
    this_user = request.user.user
    groups = this_user.groupss.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'allgroups' : groups ,
        'isempt' : is_groups_empty,
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/group.html', context)

@login_required
def search(request):
    this_user = get_object_or_404(
                        songususer,
                        user__username=request.user.username
                        )
    groups = this_user.groupss.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    if 'username' in request.POST :
        form = SearchInUsers(request.POST)
        form2 = SearchInGroups()
        if form.is_valid():
            username = form.cleaned_data['username']
            results = User.objects.filter(username__contains=username)
            if results.count() == 0:
                results = 'empty'
            context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : is_groups_empty,
            'form' : form ,
            'form2' : form2,
            'resultforusers' : results ,
            'resultforgroups' : '',
            }
            add_recent_music_to_context(this_user, context)
            return render(request, 'web/search.html', context)
    elif 'joincode' in request.POST:
        form = SearchInUsers()
        form2 = SearchInGroups(request.POST)
        if form2.is_valid():
            joincode = form2.cleaned_data['joincode']
            results = thegroups.objects.filter(joincode=joincode)
            if results.count() != 0:
                results = results[0]
            else:
                results = 'empty'
            context = {
                'groups' : groups.order_by('-cdate')[0:3],
                'isempt' : is_groups_empty,
                'form' : form ,
                'form2' : form2,
                'resultforusers' : '' ,
                'resultforgroups' : results,
            }
            add_recent_music_to_context(this_user, context)
            return render(request, 'web/search.html', context)
    else:
        form = SearchInUsers()
        form2 = SearchInGroups()
        context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empty,
        'form' : form ,
        'form2' : form2,
        'resultforusers' : '' ,
        'resultforgroups' : '',
        }
        add_recent_music_to_context(this_user, context)
        return render(request, 'web/search.html', context)
    

@login_required
def favoritve(request):
    this_user =  get_object_or_404(
                        songususer, 
                        user__username=request.user.username
                        )
    groups = this_user.groupss.all()
    favoritve_playlists = this_user.favorites.all()
    is_groups_empty = False
    is_favPL_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    if favoritve_playlists.count() == 0 :
        is_favPL_empty = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empty,
        'isempt2' : is_favPL_empty,
        'playlists' : favoritve_playlists ,
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/Favorites.html', context)


@login_required
def personal(request):
    this_user =  request.user.user
    groups = this_user.groupss.all()
    private_group = thegroups.objects.get(is_private=True, owner=this_user)
    playlists = private_group.playlist_set.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    is_PL_empty = False
    if playlists.count() == 0 :
        is_PL_empty = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empty ,
        'playlists' : playlists ,
        'isPLempt' : is_PL_empty ,
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/personal.html', context)


@login_required
def profile(request ,username):
    this_user = get_object_or_404(songususer, user__username=username)
    groups = request.user.user.groupss.all()
    is_groups_empt = False
    if groups.count() == 0 :
        is_groups_empt = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empt,
        'thisuser' : this_user,
    }
    add_recent_music_to_context(this_user, context)
    return render(request , 'web/profile.html' , context)

@login_required
def in_group(request , id):
    this_group =  get_object_or_404(thegroups , id = id)
    this_user = request.user.user
    if this_user not in this_group.member.all():
        messages.success(request , 'Bad request !')
        return redirect('dashboard')
    playlists = this_group.playlist_set.all()
    members = this_group.member.all()
    is_groups_empty = False
    if playlists.count() == 0 :
        is_groups_empty = True  
    join_URL = (  str(request.build_absolute_uri('/'))
                + str(
                    reverse('joingroup', args=(this_group.joincode,))
                    )[1:]
                )
    context = {
        'thisgroup' : this_group,
        'owner' : this_group.owner,
        'playlists' : playlists,
        'isempt' : is_groups_empty,
        'members' : members,
        'join_url' : join_URL, 
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/ingroup.html', context)


@login_required
def new_group(request):
    this_user = get_object_or_404(songususer, user=request.user)
    groups = this_user.groupss.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    if request.method == 'POST':
        form = AddNewGroupForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            des = form.cleaned_data['description']
            image = form.cleaned_data['avatar']
            new_group = thegroups.objects.create(
                                            name=name,
                                            description=des,
                                            avatar=image,
                                            owner=this_user
                                            )
            new_group.member.add(this_user)
            new_group.save()
            return redirect('ingroup', new_group.id)
    else:
        form = AddNewGroupForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : is_groups_empty,
            'formtitle' : 'Add new group' ,
            'form' : form ,
            'addon' : ( '<a href=' 
                       + reverse('group') 
                       + ' class="mx-auto d-table my-3 mt-4" >cancel</a>')
        }
        add_recent_music_to_context(this_user, context)
        return render(request, 'web/Form.html', context)


@login_required
def update_group(request , id):
    this_group = get_object_or_404(thegroups, id=id)
    if request.user.user != this_group.owner:
        messages.success(request, 'Bad request !')
        return redirect('dashboard') 
    if request.method == 'POST':
        form = UpadateGroupForm(request.POST,
                                request.FILES,
                                instance=this_group)
        if form.is_valid():
            form.save()
        return redirect('ingroup', this_group.id)
    else:
        form = UpadateGroupForm(instance=this_group)
        context = {
            'formtitle' : 'update group',
            'form' : form,
            'addon' : ( '<a href=' 
                       + reverse('deletegroup' , args=(id ,)) 
                       +' class="mx-auto d-table my-3 mt-4 deletebtn" >delete group</a><br>' 
                       +'<a href=' 
                       + reverse('ingroup' , args=(id ,)) 
                       +' class="mx-auto d-table my-3 mt-3" >cancel</a><br>'
                       ),
        }
        add_recent_music_to_context(request.user.user, context)
        return render(request, 'web/Form.html', context)


@login_required
def leave_group(request , id):
    this_user = request.user.user
    this_group = get_object_or_404(thegroups, id=id)
    if this_user not in this_group.member.all():
        messages.success(request , 'Bad request !')
        return redirect('dashboard') 
    marked_as_favorite = this_user.favorites.filter(group=this_group)
    for pl in marked_as_favorite :
        pl.favoritve.remove(this_user)
    this_group.member.remove(this_user)
    return redirect('dashboard')

@login_required
def remove_member(request , id , username):
    this_group = get_object_or_404(thegroups, id=id)
    bad_user = get_object_or_404(songususer, user__username=username)
    if this_group.owner.user != request.user :
        messages.success(request, 'Bad request !')
        return redirect('dashboard') 
    this_group.member.remove(bad_user)
    return redirect('ingroup', id)

@login_required
def playlist_view(request , id):
    this_user = request.user.user
    groups = this_user.groupss.all()
    this_playlist = get_object_or_404(playlist, id=id)
    musics = this_playlist.song_set.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True
    is_fav = False
    if this_user in this_playlist.favoritve.all() :
        is_fav = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_groups_empty,
        'this_playlist' : this_playlist ,
        'songs' : musics ,
        'isfav' : is_fav ,
    }
    add_recent_music_to_context(this_user, context)
    return render(request, 'web/inplaylist.html', context)


@login_required
def add_favorite(request , id):
    this_user = get_object_or_404(songususer, user=request.user)
    this_playlist = get_object_or_404(playlist , id=id) 
    if this_user in this_playlist.favoritve.all():
        this_playlist.favoritve.remove(this_user)
    else:
        this_playlist.favoritve.add(this_user)

    return redirect('inplaylist', id)

@login_required
def add_music(request , id):
    this_playlist = get_object_or_404(playlist , id=id)
    this_user = request.user.user
    if this_user not in this_playlist.group.member.all():
        if this_playlist.group.is_private :
            pass
        else:
            messages.success(request , 'Bad request !')
            return redirect('dashboard') 
    groups = this_user.groupss.all()
    is_groups_empty = False
    if groups.count() == 0 :
        is_groups_empty = True      
    if request.method == 'POST':
        form = AddNewMusicForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            artist = form.cleaned_data['artist']
            file = form.cleaned_data['file']
            new_song = song.objects.create(name=name,
                                           artist=artist,
                                           file=file,
                                           owner=this_user)
            new_song.playlist = this_playlist
            new_song.save()
            return redirect('inplaylist', id)
    else:
        form = AddNewMusicForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : is_groups_empty,
            'formtitle' : 'Add new Music' ,
            'form' : form ,
            'addon' : (  '<a href='
                       + reverse('inplaylist' , args=(id ,)) 
                       + ' class="mx-auto d-table my-3 mt-4" >cancel</a>'),
        }
        add_recent_music_to_context(this_user, context)
        return render(request, 'web/Form.html', context)

@login_required
def delete_music(request , musicid , playlistid):
    this_playlist = get_object_or_404(playlist , id= playlistid)
    this_user = request.user.user
    members = this_playlist.group.member.all()
    if this_user not in members:
        if this_playlist.group.is_private:
            pass
        else:
            messages.success(request , 'Bad request !')
            return redirect('dashboard') 
    
    this_music = get_object_or_404(song, id=musicid)
    this_music.delete()

    return redirect('inplaylist', playlistid)


@login_required
def add_playlist(request , id):
    this_group = get_object_or_404(thegroups, id=id)
    this_user = request.user.user
    groups = this_user.groupss.all()

    if this_user not in this_group.member.all():
        messages.success(request, 'Bad request !')
        return redirect('dashboard')

    is_group_empty = False
    if groups.count() == 0 :
        is_group_empty = True
        
    if request.method == 'POST':
        form = AddNewPlayListForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['avatar']
            newplaylist = playlist.objects.create(name=name,
                                                  group=this_group,
                                                  avatar=file)
            newplaylist.save()
            return redirect('ingroup' , id)
    else:
        form = AddNewPlayListForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : is_group_empty,
            'formtitle' : 'Add new PlayList',
            'form' : form,
            'addon' : (  '<a href='
                       + reverse('ingroup' , args=(id ,)) 
                       + ' class="mx-auto d-table my-3 mt-4" >cancel</a>'),
        }
        add_recent_music_to_context(this_user, context)
        return render(request, 'web/Form.html', context)

@login_required
def delete_playlist(request , id):
    this_playlist = get_object_or_404(playlist , id=id)
    members = this_playlist.group.member.all()
    this_user = request.user.user
    if this_user not in members:
        if this_playlist.group.is_private:
            pass
        else:
            messages.success(request, 'Bad request !')
            return redirect('dashboard') 
    this_playlist.delete()
    return redirect('ingroup', this_playlist.group.id)

@login_required
def joingroup(request , joincode):
    this_user = request.user.user
    this_group = get_object_or_404(thegroups,
                                   joincode=joincode, 
                                   is_private=False)
    if this_user in this_group.member.all():
        messages.success(request, 'already joined!')
        return redirect('ingroup', this_group.id)
    this_group.member.add(this_user)
    messages.success(request, 'Hooray! new group added.')
    return redirect('ingroup', this_group.id)


@login_required
def edit_profile(request , username):
    this_user = get_object_or_404(songususer, user__username=username)
    if request.user.user != this_user:
        messages.success(request, 'Bad request !')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form_p = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance=this_user)
        form_u = UserUpdateForm(request.POST, instance=this_user.user)
        if form_p.is_valid() and form_u.is_valid():
            form_u.save()
            form_p.save()
            return redirect('profile', username)
    form_p = ProfileUpdateForm(instance=this_user)
    form_u = UserUpdateForm(instance=this_user.user)
    contex = {
        'form_p' : form_p,
        'form_u' : form_u,
    }
    add_recent_music_to_context(this_user, contex)
    return render(request, 'web/updateprofile.html', contex)


@csrf_exempt
def add_recent_music(request):
    if 'id' in request.POST:
        this_song = get_object_or_404(song, id=request.POST['id'])
        this_user = request.user.user
        this_user_recents = RecentMusic.objects.filter(owner=this_user)
       
        check_double = this_user_recents.filter(song=this_song)
        if check_double.count() != 0:
            return JsonResponse({'status' : 'ok'}, encoder=JSONEncoder)

        # old  version
        # if this_user.recent_music.all().count() == 3:
        #   this_user.recent_music.remove(this_user.recent_music.last())
        
        # new version
        if this_user_recents.count() == 3:
            this_user_recents.first().delete()

        # old  version
        # this_user.recent_music.add(this_song)

        # new version
        new_recent_music = RecentMusic.objects.create(
                                                song=this_song,
                                                owner=this_user)
        new_recent_music.save()
        this_user.save() 
        return JsonResponse({'status' : 'ok'}, encoder=JSONEncoder)
    else:
        return JsonResponse({'status' : 'error'}, encoder=JSONEncoder)


@login_required
def add_personal_playlist(request ):
    privategroup = get_object_or_404(thegroups, 
                                    owner=request.user.user, 
                                    is_private=True)
    this_user = request.user.user
    groups = this_user.groupss.all()

    is_groups_empty = False
    if groups.count() == 0:
        is_groups_empty = True
        
    if request.method == 'POST':
        form = AddNewPlayListForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['avatar']
            newplaylist = playlist.objects.create(name=name,
                                                  group=privategroup,
                                                  avatar=file)
            newplaylist.save()
            return redirect('personal')
    else:
        form = AddNewPlayListForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : is_groups_empty,
            'formtitle' : 'Add new PlayList' ,
            'form' : form ,
            'addon' : (  '<a href=' 
                       + reverse('personal') 
                       + ' class="mx-auto d-table my-3 mt-4" >cancel</a>'),
        }
        add_recent_music_to_context(this_user, context)
        return render(request, 'web/Form.html', context)

@login_required
def remove_group(request , id):
    this_group = get_object_or_404(thegroups, id=id)
    this_user = request.user.user
    if this_group.owner != this_user:
        messages.success(request, 'Bad Request!')
        return redirect('dashboard')
    this_group.delete()
    return redirect('group')