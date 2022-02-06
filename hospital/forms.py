from django import forms
from django.contrib.auth.models import User
from . import models



#admin cadastro form
class AdminCadastroForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

        
#recep form
class RecepcionistaUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class RecepcionistaForm(forms.ModelForm):
    class Meta:
        model=models.Recepcionista
        fields=['endereco','telefone','status','fotoperfil']
#doutor form
class DoutorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoutorForm(forms.ModelForm):
    class Meta:
        model=models.Doutor
        fields=['endereco','telefone','departamento','status','fotoperfil']



#paciente form
class PacienteUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PacienteForm(forms.ModelForm):
   
    assinadoDoutorId=forms.ModelChoiceField(queryset=models.Doutor.objects.all().filter(status=True),empty_label="Departamento", to_field_name="user_id")
    class Meta:
        model=models.Paciente
        fields=['endereco','telefone','status','sintomas','fotoperfil']



class CompromissoForm(forms.ModelForm):
    doutorId=forms.ModelChoiceField(queryset=models.Doutor.objects.all().filter(status=True),empty_label="Nome do Doutor(a) e Departamento", to_field_name="user_id")
    pacienteId=forms.ModelChoiceField(queryset=models.Paciente.objects.all().filter(status=True),empty_label="Nome do Paciente e Sintomas", to_field_name="user_id")
    class Meta:
        model=models.Compromisso
        fields=['descricao','status']


class PacienteCompromissoForm(forms.ModelForm):
    doutorId=forms.ModelChoiceField(queryset=models.Doutor.objects.all().filter(status=True),empty_label="Nome do Doutor(a) e Departamento", to_field_name="user_id")
    class Meta:
        model=models.Compromisso
        fields=['descricao','status']


class ContatoForm(forms.Form):
    Nome = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Mensagem = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


