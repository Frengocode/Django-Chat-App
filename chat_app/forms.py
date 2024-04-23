from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from .models import CustomUser, Message, UserToDo


class UserRegisterForm(UserCreationForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'birthday_date', 'country', 'email', 'profile_info']

        widgets = {
            'birthday_date': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput()
        }


class ProfilePhotoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

        widgets = {
            'profile_photo': forms.FileInput()
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, label='Search...')



class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message'}))
    img_file = forms.FileInput()

    class Meta:
        model = Message
        fields = ['content', 'img_file']

    def __init__(self, *args, author=None, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = kwargs.get('instance').content if 'instance' in kwargs else None
        self.fields['img_file'].initial = kwargs.get('instance').img_file if 'instance' in kwargs else None
        self.author = author

    
class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'country', 'birthday_date', 'profile_info']


class UserToDoForm(forms.ModelForm):

    to_do = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message'}))

    class Meta:
        model = UserToDo
        fields = ['to_do', 'img']

    
    def __init__(self, *args, user = None, **kwargs):
        super(UserToDoForm, self).__init__(*args, **kwargs)
        self.user = user