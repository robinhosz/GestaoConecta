from django.db import models
from django.contrib.auth.models import User



departamentos=[('Cardiologista','Cardiologista'),
('Dermatologista','Dermatologista'),
('Pediatria','Pediatria'),
('Imunologistas','Imunologistas'),
('Anestesiologistas','Anestesiologistas'),
('Cirurgião','Cirurgião')
]
class Doutor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fotoperfil= models.ImageField(upload_to='fotoperfil/DoutorFotoPerfil/',null=True,blank=True)
    endereco = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20,null=True)
    departamento= models.CharField(max_length=50,choices=departamentos,default='Cardiologista')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.departamento)

class Recepcionista(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fotoperfil= models.ImageField(upload_to='fotoperfil/RecepcionistaFotoPerfil/',null=True,blank=True)
    endereco = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20,null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name)

class Paciente(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    fotoperfil= models.ImageField(upload_to='fotoperfil/PacienteFotoPerfil/',null=True,blank=True)
    endereco = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20,null=False)
    sintomas = models.CharField(max_length=100,null=False)
    assinadoDoutorId = models.PositiveIntegerField(null=True)
    admitirData=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.sintomas+")"


class Compromisso(models.Model):
    pacienteId=models.PositiveIntegerField(null=True)
    doutorId=models.PositiveIntegerField(null=True)
    pacienteNome=models.CharField(max_length=40,null=True)
    doutorNome=models.CharField(max_length=40,null=True)
    compromissoData=models.DateField(auto_now=True)
    descricao=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PacienteAltaDetalhes(models.Model):
    pacienteId=models.PositiveIntegerField(null=True)
    pacienteNome=models.CharField(max_length=40)
    assinadoDoutorNome=models.CharField(max_length=40)
    endereco = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20,null=True)
    sintomas = models.CharField(max_length=100,null=True)

    admitirData=models.DateField(null=False)
    saidaData=models.DateField(null=False)
    diaPassado=models.PositiveIntegerField(null=False)

    custoQuarto=models.PositiveIntegerField(null=False)
    medicamentos=models.PositiveIntegerField(null=False)
    taxaDoutor=models.PositiveIntegerField(null=False)
    Outros=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

