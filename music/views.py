from django.contrib.auth import authenticate, login
from .models import Album,Song
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from django.http import JsonResponse
from django.template import loader
from .forms import UserForm

# Create your views here.
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
def index(request):
    all_album=Album.objects.all()
    context = {'all_album':all_album}
    return render(request,'index.html',{'all_album':all_album})

def detail(request,album_id):
    user = request.user
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'detail.html', {'album': album, 'user': user})

    all_album=Album.objects.all()
    song_ids = []
    for album in Album.objects.filter():
        for song in album.song_set.all():
            song_ids.append(song.pk)
    users_songs = Song.objects.filter(pk__in=song_ids)
    
    return render(request,'detail.html',{'song_list': users_songs,})


        
def create_song(request,album_id):

    album=Album.objects.get(pk=album_id)
    return render(request, 'create_song.html', {'album': album})

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)    
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    albums = Album.objects.filter(user=request.user)
                    return render(request, 'index.html', {'albums': albums})

        return render(request, self.template_name,{'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'index.html', {'albums': albums})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


   
def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
    