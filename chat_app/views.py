from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, View, UpdateView
from django.contrib import messages
from .forms import UserRegisterForm, ProfilePhotoForm, CustomUser, SearchForm, MessageForm, ProfileChangeForm, UserToDoForm, UserToDo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from django.http import JsonResponse, HttpRequest, HttpResponse
import os
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'upload_pages/profile_update.html'
    form_class = ProfileChangeForm
    model = CustomUser
    success_url = reverse_lazy('user_profiles')

    @method_decorator(login_required)
    def dispatch(self, reuqest, *args, **kwargs):
        return super().dispatch(reuqest, *args, **kwargs)

    def get_object(self, quersyet = None):
        return self.request.user 
    


class UserRegisterView(TemplateView):
    template_name = 'authofication_pages/regsiter.html'

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Create Succses')
            return redirect('user_chats')
        
        return render(request, self.template_name, {'form':form})
    
class LoginView(TemplateView):

    template_name = 'authofication_pages/login.html'

    def get(self, request):

        return render(request, self.template_name)


    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are Logged Is Succses')
            return redirect('user_chats')
        return render(request, self.template_name, )
    

class UserProfilePhotoCreateView(TemplateView):

    template_name = 'upload_pages/photo_upload.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = ProfilePhotoForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        user_profile, created = CustomUser.objects.get_or_create(username = self.request.user)

        if not created and user_profile.profile_photo:
            messages.success(request, '')
        
        form = ProfilePhotoForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            return redirect('user_profiles')
        
        return render(request, self.template_name, {'form':form})

class UserDetail(DetailView):
    model = CustomUser
    template_name = 'detail_pages/profiles.html'
    context_object_name = 'custom_user'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Search(View):

    @method_decorator(login_required)
    def dispatch(self, request, *arsg, **kwargs):
        return super().dispatch(request, *arsg, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        form = SearchForm(request.GET or None)
        users = None

        if request.method == 'GET':
            if form.is_valid():
                search_users = form.cleaned_data['search']
                users = CustomUser.objects.filter(username__icontains = search_users)
        
        return render(request, 'pages/search.html', {'form':form, 'users':users})



@login_required
def recommended_users(request):
    current_user = request.user
    current_user_city = current_user.country   
    recommended_users = CustomUser.objects.filter(country=current_user_city).exclude(id=current_user.id)
    return render(request, 'pages/recommended_users.html', {'recommended_users': recommended_users})



@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    chat_exists = Chat.objects.filter(participants=request.user).filter(participants=profile_user).exists()

    if request.method == 'POST':
        if not chat_exists:
            chat = Chat.objects.create(user = request.user)
            chat.participants.add(request.user, profile_user)
            return redirect('user_chats')
    
        else:
            return JsonResponse({'message': 'Вы не Сможете создать Чат Так Как Чат уже Сушествует'})

    return render(request, 'chat/user_profile.html', {'profile_user': profile_user, 'chat_exists': chat_exists})


from django.http import Http404


@login_required
def chat_room(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
 
    if request.user not in chat.participants.all():
        raise Http404("You are not allowed to view this chat")

    messages = chat.messages.all()
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            img_file = form.cleaned_data['img_file']
            Message.objects.create(chat=chat, author=request.user, content=content, img_file=img_file)
            return redirect('chat_room', chat_id=chat_id)

    return render(request, 'chat/chat_room.html', {'chat': chat, 'messages': messages, 'form': form})





@login_required
def user_chats(request):
    user_chats = Chat.objects.filter(participants=request.user)
    user = request.user
    get_followers = user.follow.all()
    return render(request, 'pages/home.html', {'user_chats': user_chats, 'followers':get_followers})



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


class MessageDeleteView(View):

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    
    
    def get(self, request, pk:int, *args, **kwargs):

        messages = get_object_or_404(Message, pk=pk)

        if request.user == messages.author:
            if messages.img_file:
                file_path = os.path.join(settings.MEDIA_ROOT, str(messages.img_file))
                os.remove(file_path)
            messages.delete()
        else:
            return JsonResponse({'message':'Вы не можете удалить сообшение у другого человека'})
        
        return JsonResponse({'messgaes': 'Messgae Delete Succsesfully'})
    


class ChatDeleteView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
        
        chat = get_object_or_404(Chat, pk=pk)

        if request.user == chat.user:
            chat.delete()
        else:
            return JsonResponse({'messgaes': 'Вы не Сможете Удалить Чат'})
        
        return redirect('user_chats') 


class UserProfileView(TemplateView):
    template_name = 'pages/user_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = CustomUser.objects.filter(username = self.request.user.username)
        return context



class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'upload_pages/message_upddate.html'
    form_class = MessageForm
    success_url = reverse_lazy('user_chats')

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs ):
        return super().dispatch(request, pk=pk, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(author=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        context['form'] = MessageForm(author=user, instance=self.object)
        return context
    


class SettingsView(TemplateView):

    template_name = 'pages/settings.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class SubscribeView(View):


        @method_decorator(login_required)
        def dispatch(self, request, pk:int, *args, **kwargs):
            return super().dispatch(request, pk, *args, **kwargs)
        
        def get(self, request, pk:int, *args, **kwargs):

            follow_to_user  = get_object_or_404(CustomUser, pk=pk)

            if request.user not in follow_to_user.follow.all():
                follow_to_user.follow.add(request.user)
            else:
                follow_to_user.follow.remove(request.user)
                follow_to_user.save()
                return JsonResponse({'message': 'Вы отписались '})
            return JsonResponse({'message': 'Вы успешно Подписались'})
        

class UserToDoFormView(TemplateView):
    template_name = 'pages/user_to_do.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = UserToDoForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = UserToDoForm(request.POST, request.FILES)
        if form.is_valid():
            new_todo_ = form.save(commit=False)
            new_todo_.user = request.user
            new_todo_.save()
            return redirect('to_do')
        
        return render(request, self.template_name, {'form':form})
    
@login_required
def user_to_do(request: HttpRequest) -> HttpResponse:
    to_do = UserToDo.objects.filter(user = request.user)    
    return render(request, 'pages/to_do.html', {'to_dos':to_do})


class GetSubscribers(TemplateView):
    template_name = 'pages/get_user_subscribers.html'

    @method_decorator(login_required)
    def dispatch(self, request, username, *args, **kwargs):
        return super().dispatch(request, username, *args, **kwargs)
    
    def get(self, reequest, username, *args, **kwargs):
        
        user = CustomUser.objects.get(username=username)
        context = user.follow.all()
        return render(reequest, self.template_name, {'context':context})


class UserToDoDelete(View):

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs):
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request, pk:int, *args, **kwargs):
        
        to_do = UserToDo.objects.get(pk=pk)

        if self.request.user == to_do.user:
            if to_do.img:
                file_path = os.path.join(settings.MEDIA_ROOT, str(to_do.img))
                os.remove(file_path)
            to_do.delete()  
        return redirect('to_do')
    

class UserToDoUpdateView(UpdateView):
    model = UserToDo
    template_name = 'pages/user_to_do.html'
    form_class = UserToDoForm
    success_url = reverse_lazy('to_do')

    @method_decorator(login_required)
    def dispatch(self, request, pk:int, *args, **kwargs ):
        return super().dispatch(request, pk=pk, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user 
        context['form'] = UserToDoForm(user=user, instance=self.object)
        return context
    
    def form_valid(self, form):
        to_do = form.instance
        
        file_path = os.path.join(settings.MEDIA_ROOT, str(to_do.img))

        if to_do.img:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Сохраняем обновленные данные
        return super().form_valid(form)
    


class PasswordChangeView(TemplateView):
    template_name = 'upload_pages/password_change.html'
    form_class = PasswordChangeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name,  {'form':form})
    
    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password Changed')
            return redirect('user_profiles')
        
        return render(request, self.template_name, {'form':form})
