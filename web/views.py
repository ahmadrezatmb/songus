
from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from web.forms import AddNewGroupForm, SearchInGroups, SearchInUsers ,UpadateGroupForm ,AddNewMusicForm ,AddNewPlayListForm ,ProfileUpdateForm, UserUpdateForm
from web.models import songususer ,playlist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import group as thegroups, song 
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



@login_required
def Dashboardpage(request):
    this_user =  get_object_or_404(
                        songususer, 
                        user__username = request.user.username)

    groups = this_user.groupss.all()
    suggested = song.objects.filter(issuggested=True).latest()

    is_empt = False
    if groups.count() == 0 :
        is_empt = True
    
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : is_empt ,
        'suggested' : suggested ,
        'recentmusics' : this_user.recentmusic.all()[::-1],
    }
    return render(request , 'web/Dashboard.html' , context)

@login_required
def group(request):
    this_user =  get_object_or_404(songususer , user__username = request.user.username)
    groups = this_user.groupss.all()
    
    
    is_empt = False
    if groups.count() == 0 :
        is_empt = True
    
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'allgroups' : groups ,
        'isempt' : is_empt,
        'recentmusics' : this_user.recentmusic.all()[::-1],
    }
    return render(request , 'web/group.html' , context)

@login_required
def search(request):
    this_user =  get_object_or_404(songususer , user__username = request.user.username)
    groups = this_user.groupss.all()
    
    
    isempt = False
    if groups.count() == 0 :
        isempt = True
    if 'username' in request.POST :
        form = SearchInUsers(request.POST)
        form2 = SearchInGroups()
        if form.is_valid():
            username = form.cleaned_data['username']
            results = User.objects.filter(username__contains = username)
            if results.count() == 0:
                results = 'empty'
            context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : isempt,
            'form' : form ,
            'form2' : form2,
            'resultforusers' : results ,
            'resultforgroups' : '',
            'recentmusics' : this_user.recentmusic.all()[::-1],
            }
            return render(request , 'web/search.html', context)
    elif 'joincode' in request.POST:
        form = SearchInUsers()
        form2 = SearchInGroups(request.POST)
        if form2.is_valid():
            joincode = form2.cleaned_data['joincode']
            results = thegroups.objects.filter(joincode = joincode)
 
            if results.count() != 0:
                results = results[0]
            else:
                results = 'empty'
            context = {
                'groups' : groups.order_by('-cdate')[0:3],
                'isempt' : isempt,
                'form' : form ,
                'form2' : form2,
                'resultforusers' : '' ,
                'resultforgroups' : results,
                'recentmusics' : this_user.recentmusic.all()[::-1],
            }
            return render(request , 'web/search.html', context)
    
    
    else:
        form = SearchInUsers()
        form2 = SearchInGroups()
        context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : isempt,
        'form' : form ,
        'form2' : form2,
        'resultforusers' : '' ,
        'resultforgroups' : '',
        'recentmusics' : this_user.recentmusic.all()[::-1],
        }
        return render(request , 'web/search.html', context)
    

@login_required
def favoritve(request):
    this_user =  get_object_or_404(songususer , user__username = request.user.username)
    groups = this_user.groupss.all()
    favoritveplaylists = this_user.favorites.all()
    
    isempt = False
    isempt2 = False
    if groups.count() == 0 :
        isempt = True
    if favoritveplaylists.count() == 0 :
        isempt2 = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : isempt,
        'isempt2' : isempt2 ,
        'playlists' : favoritveplaylists ,
        'recentmusics' : this_user.recentmusic.all()[::-1],
    }
    return render(request , 'web/Favorites.html' , context)

@login_required
def personal(request):
    this_user =  request.user.user
    groups = this_user.groupss.all()
    
    privategroup = thegroups.objects.get(isprivate = True , owner = this_user)
    playlists = privategroup.playlist_set.all()
    
    isempt = False
    if groups.count() == 0 :
        isempt = True
    
    isPLempt = False
    if playlists.count() == 0 :
        isPLempt = True


    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : isempt ,
        'recentmusics' : this_user.recentmusic.all()[::-1],
        'playlists' : playlists ,
        'isPLempt' : isPLempt ,
    }
    return render(request , 'web/personal.html' , context)

@login_required
def profile(request ,username):
    
    this_user = get_object_or_404(songususer , user__username = username)
    groups = request.user.user.groupss.all()
    
    
    isempt = False
    if groups.count() == 0 :
        isempt = True
    
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : isempt,
        'thisuser' : this_user ,
        'recentmusics' : request.user.user.recentmusic.all()[::-1],
    }
    return render(request , 'web/profile.html' , context)

@login_required
def ingroup(request , id):
    this_group =  get_object_or_404(thegroups , id = id)
    this_user = request.user.user
    if this_user not in this_group.member.all():
        messages.success(request , 'Bad request !')
        return redirect('dashboard')
    playlists = this_group.playlist_set.all()
    members = this_group.member.all()
    
    isempt = False
    if playlists.count() == 0 :
        isempt = True
        
    join_url = str(request.build_absolute_uri('/')) + str(reverse('joingroup' , args=(this_group.joincode ,) ))[1:]
    print(join_url)
    context = {
        'thisgroup' : this_group ,
        'owner' : this_group.owner ,
        'playlists' : playlists,
        'isempt' : isempt ,
        'members' : members,
        'recentmusics' : this_user.recentmusic.all()[::-1],
        'join_url' : join_url , 
    }
    return render(request , 'web/ingroup.html'  , context)


@login_required
def newgroup(request):
    this_user = get_object_or_404(songususer , user = request.user)
    groups = this_user.groupss.all()
    isempt = False
    if groups.count() == 0 :
        isempt = True
    if request.method == 'POST':
        form = AddNewGroupForm(request.POST , request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            des = form.cleaned_data['description']
            image = form.cleaned_data['avatar']
            newgroup = thegroups.objects.create(name = name , description = des , avatar = image , owner = this_user)
            newgroup.member.add(this_user)
            newgroup.save()
            return redirect('ingroup' , newgroup.id)
    else:
        form = AddNewGroupForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : isempt,
            'formtitle' : 'Add new group' ,
            'form' : form ,
            'recentmusics' : this_user.recentmusic.all()[::-1],
            'addon' : '<a href=' + reverse('group') +' class="mx-auto d-table my-3 mt-4" >cancel</a>'
        }
        return render(request , 'web/Form.html' , context)


@login_required
def updategroup(request , id):
    this_group = get_object_or_404(thegroups , id = id)
    if request.user.user != this_group.owner:
        messages.success(request , 'Bad request !')
        return redirect('dashboard') 
    if request.method == 'POST':
        form = UpadateGroupForm(request.POST , request.FILES , instance=this_group)
        if form.is_valid():
            form.save()
        
        return redirect('ingroup' , this_group.id)
    else:
        form = UpadateGroupForm(instance=this_group)
        context = {
            'formtitle' : 'update group' ,
            'form' : form ,
            'recentmusics' : request.user.user.recentmusic.all()[::-1],
            'addon' : '<a href=' + reverse('ingroup' , args=(id ,)) +' class="mx-auto d-table my-3 mt-4" >cancel</a>' ,
        }
        return render(request , 'web/Form.html' , context)


@login_required
def leavegroup(request , id):
    this_user = request.user.user
    this_group = get_object_or_404(thegroups , id = id)
    if this_user not in this_group.member.all():
        messages.success(request , 'Bad request !')
        return redirect('dashboard') 
    markedasfavorted = this_user.favorites.filter(group = this_group)
    for pl in markedasfavorted :
        pl.favoritve.remove(this_user)
    this_group.member.remove(this_user)
    return redirect('dashboard')

@login_required
def removemember(request , id , username):
    this_group = get_object_or_404(thegroups , id = id)
    bad_user = get_object_or_404(songususer , user__username = username)
    if this_group.owner.user != request.user :
        messages.success(request , 'Bad request !')
        return redirect('dashboard') 
    this_group.member.remove(bad_user)
    return redirect('ingroup' , id)

@login_required
def playlistshow(request , id):
    # this_user =  get_object_or_404(songususer , user__username = request.user.username)
    this_user = request.user.user
    groups = this_user.groupss.all()
    this_playlist = get_object_or_404(playlist , id=id)
    musics = this_playlist.song_set.all()
    isempt = False
    if groups.count() == 0 :
        isempt = True

    isfav = False
    if this_user in this_playlist.favoritve.all() :
        isfav = True
    context = {
        'groups' : groups.order_by('-cdate')[0:3],
        'isempt' : isempt,
        'this_playlist' : this_playlist ,
        'songs' : musics ,
        'recentmusics' : this_user.recentmusic.all()[::-1],
        'isfav' : isfav ,
    }
    return render(request , 'web/inplaylist.html' , context)


@login_required
def addfavorite(request , id):
    this_user = get_object_or_404(songususer , user = request.user)
    this_playlist = get_object_or_404(playlist , id=id)
    
    if this_user in this_playlist.favoritve.all():
        this_playlist.favoritve.remove(this_user)
    else:
        this_playlist.favoritve.add(this_user)

    return redirect('inplaylist' , id)

@login_required
def AddMusic(request , id):
    this_playlist = get_object_or_404(playlist , id=id)
    this_user = request.user.user
    if this_user not in this_playlist.group.member.all():
        if this_playlist.group.isprivate :
            pass
        else:
            messages.success(request , 'Bad request !')
            return redirect('dashboard') 
    
    
    groups = this_user.groupss.all()

    isempt = False
    if groups.count() == 0 :
        isempt = True
        
    if request.method == 'POST':
        form = AddNewMusicForm(request.POST , request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            artist = form.cleaned_data['artist']
            file = form.cleaned_data['file']
            newsong = song.objects.create(name = name , artist = artist , file = file )
            newsong.playlist = this_playlist
            newsong.save()
            return redirect('inplaylist' , id)
    else:
        form = AddNewMusicForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : isempt,
            'formtitle' : 'Add new Music' ,
            'form' : form ,
            'recentmusics' : this_user.recentmusic.all()[::-1],
            'addon' : '<a href=' + reverse('inplaylist' , args=(id ,)) +' class="mx-auto d-table my-3 mt-4" >cancel</a>',
        }
        return render(request , 'web/Form.html' , context)

@login_required
def deletemusic(request , musicid , playlistid):
    this_playlist = get_object_or_404(playlist , id= playlistid)
    this_user = request.user.user
    members = this_playlist.group.member.all()
    if this_user not in members:
        if this_playlist.group.isprivate:
            pass
        else:
            messages.success(request , 'Bad request !')
            return redirect('dashboard') 
    
    this_music = get_object_or_404(song , id= musicid)
    this_music.delete()

    return redirect('inplaylist' , playlistid)


@login_required
def AddPlayList(request , id):
    this_group = get_object_or_404(thegroups , id=id)
    this_user = request.user.user
    groups = this_user.groupss.all()

    if this_user not in this_group.member.all():
        messages.success(request , 'Bad request !')
        return redirect('dashboard')

    isempt = False
    if groups.count() == 0 :
        isempt = True
        
    if request.method == 'POST':
        form = AddNewPlayListForm(request.POST , request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['avatar']
            newplaylist = playlist.objects.create(name = name , group = this_group , avatar = file )
            
            newplaylist.save()
            return redirect('ingroup' , id)
    else:
        form = AddNewPlayListForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : isempt,
            'formtitle' : 'Add new PlayList' ,
            'form' : form ,
            'recentmusics' : this_user.recentmusic.all()[::-1],
            'addon' : '<a href=' + reverse('ingroup' , args=(id ,)) +' class="mx-auto d-table my-3 mt-4" >cancel</a>',
        }
        return render(request , 'web/Form.html' , context)

@login_required
def deleteplaylist(request , id):
    this_playlist = get_object_or_404(playlist , id=id)
    members = this_playlist.group.member.all()
    this_user = request.user.user
    if this_user not in members:
        if this_playlist.group.isprivate:
            pass
        else:
            messages.success(request , 'Bad request !')
            return redirect('dashboard') 
    this_playlist.delete()
    return redirect('ingroup' , this_playlist.group.id)

@login_required
def joingroup(request , joincode):
    this_user = request.user.user
    this_group = get_object_or_404(thegroups , joincode = joincode , isprivate = False)
    if this_user in this_group.member.all():
        messages.success(request , 'already joined!')
        return redirect('ingroup' , this_group.id)
    this_group.member.add(this_user)
    messages.success(request , 'Hooray! new group added.')
    return redirect('ingroup' , this_group.id)


@login_required
def editprofile(request , username):
    this_user = get_object_or_404(songususer , user__username = username)
    if request.user.user != this_user :
        messages.success(request , 'Bad request !')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form_p = ProfileUpdateForm(request.POST , request.FILES ,instance=this_user)
        form_u = UserUpdateForm( request.POST ,instance=this_user.user)
        if form_p.is_valid() and form_u.is_valid():
            form_u.save()
            form_p.save()
            return redirect('profile' , username)
    form_p = ProfileUpdateForm(instance=this_user)
    form_u = UserUpdateForm(instance=this_user.user)
    contex = {
        'form_p' : form_p ,
        'form_u' : form_u ,
        'recentmusics' : this_user.recentmusic.all()[::-1],
    }
    return render(request , 'web/updateprofile.html' , contex)


@csrf_exempt
def addrecentmusic(request):
    if 'id' in request.POST :
        this_song = get_object_or_404(song , id = request.POST['id'])
        this_user = request.user.user
        if this_user.recentmusic.all().count() == 3 :
            print(this_user.recentmusic.last())
            this_user.recentmusic.remove(this_user.recentmusic.last())
        this_user.recentmusic.add(this_song)
        this_user.save() 
        return JsonResponse({'status' : 'ok'} , encoder= JSONEncoder)
    else :
        return JsonResponse({'status' : 'error'} , encoder= JSONEncoder)


@login_required
def AddPersonalPlayList(request ):
    privategroup = get_object_or_404(thegroups , owner = request.user.user , isprivate =True)
    this_user = request.user.user
    groups = this_user.groupss.all()

    isempt = False
    if groups.count() == 0 :
        isempt = True
        
    if request.method == 'POST':
        form = AddNewPlayListForm(request.POST , request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            file = form.cleaned_data['avatar']
            newplaylist = playlist.objects.create(name = name , group = privategroup , avatar = file )
            newplaylist.save()
            return redirect('personal')
    else:
        form = AddNewPlayListForm()
        context = {
            'groups' : groups.order_by('-cdate')[0:3],
            'isempt' : isempt,
            'formtitle' : 'Add new PlayList' ,
            'form' : form ,
            'recentmusics' : this_user.recentmusic.all()[::-1],
            'addon' : '<a href=' + reverse('personal') +' class="mx-auto d-table my-3 mt-4" >cancel</a>',
        }
        return render(request , 'web/Form.html' , context)