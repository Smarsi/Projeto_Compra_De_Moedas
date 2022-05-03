from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUsuario

class CustomUsuarioCreateForm(UserCreationForm): #Criação de Usuário

    class Meta:
        model = CustomUsuario
        fields = ('username', 'first_name', 'last_name', 'cpf', 'fone') #Exatamente os mesmos campos que definimos no REQUIRED_FIELDS do models.
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class CustomUsuarioChangeForm(UserChangeForm): #Edição de Usuário

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'cpf', 'fone')

