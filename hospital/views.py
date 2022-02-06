from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('aposlogin')
    return render(request,'hospital/index.html')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('aposlogin')
    return render(request,'hospital/adminclick.html')

def recepcionistaclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('aposlogin')
    return render(request,'hospital/recepcionistaclick.html')    

def doutorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('aposlogin')
    return render(request,'hospital/doutorclick.html')



def pacienteclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('aposlogin')
    return render(request,'hospital/pacienteclick.html')




def admin_cadastro_view(request):
    form=forms.AdminCadastroForm()
    if request.method=='POST':
        form=forms.AdminCadastroForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/admincadastro.html',{'form':form})


def recepcionista_cadastro_view(request):
    userForm=forms.RecepcionistaUserForm()
    recepcionistaForm=forms.RecepcionistaForm()
    mydict={'userForm':userForm,'recepcionistaForm':recepcionistaForm}
    if request.method=='POST':
        userForm=forms.RecepcionistaUserForm(request.POST)
        recepcionistaForm=forms.RecepcionistaForm(request.POST,request.FILES)
        if userForm.is_valid() and recepcionistaForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            recepcionista=recepcionistaForm.save(commit=False)
            recepcionista.user=user
            recepcionista=recepcionista.save()
            my_recepcionista_group = Group.objects.get_or_create(name='RECEPCIONISTA')
            my_recepcionista_group[0].user_set.add(user)
        return HttpResponseRedirect('recepcionistalogin')
    return render(request,'hospital/recepcionistacadastro.html',context=mydict)

def doutor_cadastro_view(request):
    userForm=forms.DoutorUserForm()
    doutorForm=forms.DoutorForm()
    mydict={'userForm':userForm,'doutorForm':doutorForm}
    if request.method=='POST':
        userForm=forms.DoutorUserForm(request.POST)
        doutorForm=forms.DoutorForm(request.POST,request.FILES)
        if userForm.is_valid() and doutorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doutor=doutorForm.save(commit=False)
            doutor.user=user
            doutor=doutor.save()
            my_doutor_group = Group.objects.get_or_create(name='DOUTOR')
            my_doutor_group[0].user_set.add(user)
        return HttpResponseRedirect('doutorlogin')
    return render(request,'hospital/doutorcadastro.html',context=mydict)


def paciente_cadastro_view(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.assinadoDoutorId=request.POST.get('assinadoDoutorId')
            paciente=paciente.save()
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)
        return HttpResponseRedirect('pacientelogin')
    return render(request,'hospital/pacientecadastro.html',context=mydict)






def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_recepcionista(user):
    return user.groups.filter(name='RECEPCIONISTA').exists()    
def is_doutor(user):
    return user.groups.filter(name='DOUTOR').exists()
def is_paciente(user):
    return user.groups.filter(name='PACIENTE').exists()



def aposlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-painelcontrole')
    elif is_recepcionista(request.user):
        accountapproval=models.Recepcionista.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('recepcionista-painelcontrole')
        else:
            return render(request,'hospital/recepcionista_aguardo_aprovacao.html')
    elif is_doutor(request.user):
        accountapproval=models.Doutor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doutor-painelcontrole')
        else:
            return render(request,'hospital/doutor_aguardo_aprovacao.html')
    elif is_paciente(request.user):
        accountapproval=models.Paciente.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('paciente-painelcontrole')
        else:
            return render(request,'hospital/paciente_aguardo_aprovacao.html')









@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_painelcontrole_view(request):
    
    doutores=models.Doutor.objects.all().order_by('-id')
    pacientes=models.Paciente.objects.all().order_by('-id')
    recepcionistas=models.Recepcionista.objects.all().order_by('-id')
    
    doutorcount=models.Doutor.objects.all().filter(status=True).count()
    pendentedoutorcount=models.Doutor.objects.all().filter(status=False).count()
    
    recepcionistacount=models.Recepcionista.objects.all().filter(status=True).count()
    pendenterecepcionistacount=models.Recepcionista.objects.all().filter(status=False).count()

    pacientecount=models.Paciente.objects.all().filter(status=True).count()
    pendentepacientecount=models.Paciente.objects.all().filter(status=False).count()

    compromissocount=models.Compromisso.objects.all().filter(status=True).count()
    pendentecompromissocount=models.Compromisso.objects.all().filter(status=False).count()
    mydict={
    'doutores':doutores,
    'recepcionistas':recepcionistas,
    'pacientes':pacientes,
    'doutorcount':doutorcount,
    'pendentedoutorcount':pendentedoutorcount,
    'recepcionistacount':recepcionistacount,
    'pendenterecepcionistacount':pendenterecepcionistacount,
    'pacientecount':pacientecount,
    'pendentepacientecount':pendentepacientecount,
    'compromissocount':compromissocount,
    'pendentecompromissocount':pendentecompromissocount,
    }
    return render(request,'hospital/admin_painelcontrole.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doutor_view(request):
    return render(request,'hospital/admin_doutor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doutor_view(request):
    doutores=models.Doutor.objects.all().filter(status=True)
    return render(request,'hospital/admin_ver_doutor.html',{'doutores':doutores})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deletar_doutor_from_hospital_view(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)
    user.delete()
    doutor.delete()
    return redirect('admin-ver-doutor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def atualizar_doutor_view(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)

    userForm=forms.DoutorUserForm(instance=user)
    doutorForm=forms.DoutorForm(request.FILES,instance=doutor)
    mydict={'userForm':userForm,'doutorForm':doutorForm}
    if request.method=='POST':
        userForm=forms.DoutorUserForm(request.POST,instance=user)
        doutorForm=forms.DoutorForm(request.POST,request.FILES,instance=doutor)
        if userForm.is_valid() and doutorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doutorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-ver-doutor')
    return render(request,'hospital/admin_atualizar_doutor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doutor_view(request):
    userForm=forms.DoutorUserForm()
    doutorForm=forms.DoutorForm()
    mydict={'userForm':userForm,'doutorForm':doutorForm}
    if request.method=='POST':
        userForm=forms.DoutorUserForm(request.POST)
        doutorForm=forms.DoutorForm(request.POST, request.FILES)
        if userForm.is_valid() and doutorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doutor=doutorForm.save(commit=False)
            doutor.user=user
            doutor.status=True
            doutor.save()

            my_doutor_group = Group.objects.get_or_create(name='DOUTOR')
            my_doutor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-ver-doutor')
    return render(request,'hospital/admin_add_doutor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_doutor_view(request):
    
    doutores=models.Doutor.objects.all().filter(status=False)
    return render(request,'hospital/admin_aprovar_doutor.html',{'doutores':doutores})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprovar_doutor_view(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    doutor.status=True
    doutor.save()
    return redirect(reverse('admin-aprovar-doutor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rejeitar_doutor_view(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)
    user.delete()
    doutor.delete()
    return redirect('admin-aprovar-doutor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doutor_especializacao_view(request):
    doutores=models.Doutor.objects.all().filter(status=True)
    return render(request,'hospital/admin_ver_doutor_especializacao.html',{'doutores':doutores})

#----recepcionsita admin----

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_recepcionista_view(request):
    return render(request,'hospital/admin_recepcionista.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_recepcionista_view(request):
    recepcionistas=models.Recepcionista.objects.all().filter(status=True)
    return render(request,'hospital/admin_ver_recepcionista.html',{'recepcionistas':recepcionistas})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deletar_recepcionista_from_hospital_view(request,pk):
    recepcionista=models.Recepcionista.objects.get(id=pk)
    user=models.User.objects.get(id=recepcionista.user_id)
    user.delete()
    recepcionista.delete()
    return redirect('admin-ver-recepcionista')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def atualizar_recepcionista_view(request,pk):
    recepcionista=models.Recepcionista.objects.get(id=pk)
    user=models.User.objects.get(id=recepcionista.user_id)

    userForm=forms.RecepcionistaUserForm(instance=user)
    recepcionistaForm=forms.RecepcionistaForm(request.FILES,instance=recepcionista)
    mydict={'userForm':userForm,'recepcionistaForm':recepcionistaForm}
    if request.method=='POST':
        userForm=forms.RecepcionistaUserForm(request.POST,instance=user)
        recepcionistaForm=forms.RecepcionistaForm(request.POST,request.FILES,instance=recepcionista)
        if userForm.is_valid() and recepcionistaForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            recepcionista=recepcionistaForm.save(commit=False)
            recepcionista.status=True
            recepcionista.save()
            return redirect('admin-ver-recepcionista')
    return render(request,'hospital/admin_atualizar_recepcionista.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_recepcionista_view(request):
    userForm=forms.RecepcionistaUserForm()
    recepcionistaForm=forms.RecepcionistaForm()
    mydict={'userForm':userForm,'recepcionistaForm':recepcionistaForm}
    if request.method=='POST':
        userForm=forms.RecepcionistaUserForm(request.POST)
        recepcionistaForm=forms.RecepcionistaForm(request.POST, request.FILES)
        if userForm.is_valid() and recepcionistaForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            recepcionista=recepcionistaForm.save(commit=False)
            recepcionista.user=user
            recepcionista.status=True
            recepcionista.save()

            my_recepcionista_group = Group.objects.get_or_create(name='RECEPCIONISTA')
            my_recepcionista_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-ver-recepcionista')
    return render(request,'hospital/admin_add_recepcionista.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_recepcionista_view(request):
    
    recepcionistas=models.Recepcionista.objects.all().filter(status=False)
    return render(request,'hospital/admin_aprovar_recepcionista.html',{'recepcionistas':recepcionistas})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprovar_recepcionista_view(request,pk):
    recepcionista=models.Recepcionista.objects.get(id=pk)
    recepcionista.status=True
    recepcionista.save()
    return redirect(reverse('admin-aprovar-recepcionista'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rejeitar_recepcionista_view(request,pk):
    recepcionista=models.Recepcionista.objects.get(id=pk)
    user=models.User.objects.get(id=recepcionista.user_id)
    user.delete()
    recepcionista.delete()
    return redirect('admin-aprovar-recepcionista')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_paciente_view(request):
    return render(request,'hospital/admin_paciente.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_paciente_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'hospital/admin_ver_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def deletar_paciente_from_hospital_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('admin-ver-paciente')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def atualizar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)

    userForm=forms.PacienteUserForm(instance=user)
    pacienteForm=forms.PacienteForm(request.FILES,instance=paciente)
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST,instance=user)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES,instance=paciente)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.status=True
            paciente.assinadoDoutorId=request.POST.get('assinadoDoutorId')
            paciente.save()
            return redirect('admin-ver-paciente')
    return render(request,'hospital/admin_atualizar_paciente.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_paciente_view(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.status=True
            paciente.assinadoDoutorId=request.POST.get('assinadoDoutorId')
            paciente.save()

            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-ver-paciente')
    return render(request,'hospital/admin_add_paciente.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_paciente_view(request):
    
    pacientes=models.Paciente.objects.all().filter(status=False)
    return render(request,'hospital/admin_aprovar_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprovar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    paciente.status=True
    paciente.save()
    return redirect(reverse('admin-aprovar-paciente'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rejeitar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('admin-aprovar-paciente')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_alta_paciente_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'hospital/admin_alta_paciente.html',{'pacientes':pacientes})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def alta_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    days=(date.today()-paciente.admitirData) 
    assinadoDoutor=models.User.objects.all().filter(id=paciente.assinadoDoutorId)
    d=days.days 
    pacienteDict={
        'pacienteId':pk,
        'nome':paciente.get_name,
        'telefone':paciente.telefone,
        'endereco':paciente.endereco,
        'sintomas':paciente.sintomas,
        'admitirData':paciente.admitirData,
        'todayDate':date.today(),
        'day':d,
        'assinadoDoutorNome':assinadoDoutor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'custoQuarto':int(request.POST['custoQuarto'])*int(d),
            'taxaDoutor':request.POST['taxaDoutor'],
            'medicamentos' : request.POST['medicamentos'],
            'Outros' : request.POST['Outros'],
            'total':(int(request.POST['custoQuarto'])*int(d))+int(request.POST['taxaDoutor'])+int(request.POST['medicamentos'])+int(request.POST['Outros'])
        }
        pacienteDict.update(feeDict)
        
        pDD=models.PacienteAltaDetalhes()
        pDD.pacienteId=pk
        pDD.pacienteNome=paciente.get_name
        pDD.assinadoDoutorNome=assinadoDoutor[0].first_name
        pDD.endereco=paciente.endereco
        pDD.telefone=paciente.telefone
        pDD.sintomas=paciente.sintomas
        pDD.admitirData=paciente.admitirData
        pDD.saidaData=date.today()
        pDD.diaPassado=int(d)
        pDD.medicamentos=int(request.POST['medicamentos'])
        pDD.custoQuarto=int(request.POST['custoQuarto'])*int(d)
        pDD.taxaDoutor=int(request.POST['taxaDoutor'])
        pDD.Outros=int(request.POST['Outros'])
        pDD.total=(int(request.POST['custoQuarto'])*int(d))+int(request.POST['taxaDoutor'])+int(request.POST['medicamentos'])+int(request.POST['Outros'])
        pDD.save()
        return render(request,'hospital/paciente_final_conta.html',context=pacienteDict)
    return render(request,'hospital/paciente_gerar_conta.html',context=pacienteDict)



#--------------para alta do paciente (pdf) download e print
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    altaDetalhes=models.PacienteAltaDetalhes.objects.all().filter(pacienteId=pk).order_by('-id')[:1]
    dict={
        'pacienteNome':altaDetalhes[0].pacienteNome,
        'assinadoDoutorNome':altaDetalhes[0].assinadoDoutorNome,
        'endereco':altaDetalhes[0].endereco,
        'telefone':altaDetalhes[0].telefone,
        'sintomas':altaDetalhes[0].sintomas,
        'admitirData':altaDetalhes[0].admitirData,
        'saidaData':altaDetalhes[0].saidaData,
        'diaPassado':altaDetalhes[0].diaPassado,
        'medicamentos':altaDetalhes[0].medicamentos,
        'custoQuarto':altaDetalhes[0].custoQuarto,
        'taxaDoutor':altaDetalhes[0].taxaDoutor,
        'Outros':altaDetalhes[0].Outros,
        'total':altaDetalhes[0].total,
    }
    return render_to_pdf('hospital/download_conta.html',dict)



#-----------------COMPROMISSO--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_compromisso_view(request):
    return render(request,'hospital/admin_compromisso.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_compromisso_view(request):
    compromissos=models.Compromisso.objects.all().filter(status=True)
    return render(request,'hospital/admin_ver_compromisso.html',{'compromissos':compromissos})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_compromisso_view(request):
    compromissoForm=forms.CompromissoForm()
    mydict={'compromissoForm':compromissoForm,}
    if request.method=='POST':
        compromissoForm=forms.CompromissoForm(request.POST)
        if compromissoForm.is_valid():
            compromisso=compromissoForm.save(commit=False)
            compromisso.doutorId=request.POST.get('doutorId')
            compromisso.pacienteId=request.POST.get('pacienteId')
            compromisso.doutorNome=models.User.objects.get(id=request.POST.get('doutorId')).first_name
            compromisso.pacienteNome=models.User.objects.get(id=request.POST.get('pacienteId')).first_name
            compromisso.status=True
            compromisso.save()
        return HttpResponseRedirect('admin-ver-compromisso')
    return render(request,'hospital/admin_add_compromisso.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_aprovar_compromisso_view(request):
    
    compromissos=models.Compromisso.objects.all().filter(status=False)
    return render(request,'hospital/admin_aprovar_compromisso.html',{'compromissos':compromissos})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def aprovar_compromisso_view(request,pk):
    compromisso=models.Compromisso.objects.get(id=pk)
    compromisso.status=True
    compromisso.save()
    return redirect(reverse('admin-aprovar-compromisso'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def rejeitar_compromisso_view(request,pk):
    compromisso=models.Compromisso.objects.get(id=pk)
    compromisso.delete()
    return redirect('admin-aprovar-compromisso')
#---------------------------------------------------------------------------------
#------------------------ ADMIN final de visualizar ------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------------------RECEPCIONISTA começa visualizar------------------------------
#---------------------------------------------------------------------------------


@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_painelcontrole_view(request):
    
    doutores=models.Doutor.objects.all().order_by('-id')
    pacientes=models.Paciente.objects.all().order_by('-id')
    
    doutorcount=models.Doutor.objects.all().filter(status=True).count()
    pendentedoutorcount=models.Doutor.objects.all().filter(status=False).count()

    pacientecount=models.Paciente.objects.all().filter(status=True).count()
    pendentepacientecount=models.Paciente.objects.all().filter(status=False).count()

    compromissocount=models.Compromisso.objects.all().filter(status=True).count()
    pendentecompromissocount=models.Compromisso.objects.all().filter(status=False).count()
    mydict={
    'doutores':doutores,
    'pacientes':pacientes,
    'doutorcount':doutorcount,
    'pendentedoutorcount':pendentedoutorcount,
    'pacientecount':pacientecount,
    'pendentepacientecount':pendentepacientecount,
    'compromissocount':compromissocount,
    'pendentecompromissocount':pendentecompromissocount,
    }
    return render(request,'hospital/recepcionista_painelcontrole.html',context=mydict)



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_doutor_view(request):
    return render(request,'hospital/recepcionista_doutor.html')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_view_doutor_view(request):
    doutores=models.Doutor.objects.all().filter(status=True)
    return render(request,'hospital/recepcionista_ver_doutor.html',{'doutores':doutores})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def deletar_doutor_from_hospital(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)
    user.delete()
    doutor.delete()
    return redirect('recepcionista-ver-doutor')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def atualizar_doutor(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)

    userForm=forms.DoutorUserForm(instance=user)
    doutorForm=forms.DoutorForm(request.FILES,instance=doutor)
    mydict={'userForm':userForm,'doutorForm':doutorForm}
    if request.method=='POST':
        userForm=forms.DoutorUserForm(request.POST,instance=user)
        doutorForm=forms.DoutorForm(request.POST,request.FILES,instance=doutor)
        if userForm.is_valid() and doutorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doutorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('recepcionista-ver-doutor')
    return render(request,'hospital/recepcionista_atualizar_doutor.html',context=mydict)




@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_add_doutor_view(request):
    userForm=forms.DoutorUserForm()
    doutorForm=forms.DoutorForm()
    mydict={'userForm':userForm,'doutorForm':doutorForm}
    if request.method=='POST':
        userForm=forms.DoutorUserForm(request.POST)
        doutorForm=forms.DoutorForm(request.POST, request.FILES)
        if userForm.is_valid() and doutorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doutor=doutorForm.save(commit=False)
            doutor.user=user
            doutor.status=True
            doutor.save()

            my_doutor_group = Group.objects.get_or_create(name='DOUTOR')
            my_doutor_group[0].user_set.add(user)

        return HttpResponseRedirect('recepcionista-ver-doutor')
    return render(request,'hospital/recepcionista_add_doutor.html',context=mydict)




@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_aprovar_doutor_view(request):
    
    doutores=models.Doutor.objects.all().filter(status=False)
    return render(request,'hospital/recepcionista_aprovar_doutor.html',{'doutores':doutores})


@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def aprovar_doutor(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    doutor.status=True
    doutor.save()
    return redirect(reverse('recepcionista-aprovar-doutor'))


@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def rejeitar_doutor(request,pk):
    doutor=models.Doutor.objects.get(id=pk)
    user=models.User.objects.get(id=doutor.user_id)
    user.delete()
    doutor.delete()
    return redirect('recepcionista-aprovar-doutor')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_view_doutor_especializacao_view(request):
    doutores=models.Doutor.objects.all().filter(status=True)
    return render(request,'hospital/recepcionista_ver_doutor_especializacao.html',{'doutores':doutores})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_paciente_view(request):
    return render(request,'hospital/recepcionista_paciente.html')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_view_paciente_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'hospital/recepcionista_ver_paciente.html',{'pacientes':pacientes})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def deletar_paciente_from_hospital(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('recepcionista-ver-paciente')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def atualizar_paciente(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)

    userForm=forms.PacienteUserForm(instance=user)
    pacienteForm=forms.PacienteForm(request.FILES,instance=paciente)
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST,instance=user)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES,instance=paciente)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.status=True
            paciente.assinadoDoutorId=request.POST.get('assinadoDoutorId')
            paciente.save()
            return redirect('recepcionista-ver-paciente')
    return render(request,'hospital/recepcionista_atualizar_paciente.html',context=mydict)





@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_add_paciente_view(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.status=True
            paciente.assinadoDoutorId=request.POST.get('assinadoDoutorId')
            paciente.save()

            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)

        return HttpResponseRedirect('recepcionista-ver-paciente')
    return render(request,'hospital/recepcionista_add_paciente.html',context=mydict)




@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_aprovar_paciente_view(request):
    
    pacientes=models.Paciente.objects.all().filter(status=False)
    return render(request,'hospital/recepcionista_aprovar_paciente.html',{'pacientes':pacientes})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def aprovar_paciente(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    paciente.status=True
    paciente.save()
    return redirect(reverse('recepcionista-aprovar-paciente'))



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def rejeitar_paciente(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('recepcionista-aprovar-paciente')




@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_alta_paciente_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'hospital/recepcionista_alta_paciente.html',{'pacientes':pacientes})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def alta_paciente(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    days=(date.today()-paciente.admitirData) 
    assinadoDoutor=models.User.objects.all().filter(id=paciente.assinadoDoutorId)
    d=days.days 
    pacienteDict={
        'pacienteId':pk,
        'nome':paciente.get_name,
        'telefone':paciente.telefone,
        'endereco':paciente.endereco,
        'sintomas':paciente.sintomas,
        'admitirData':paciente.admitirData,
        'todayDate':date.today(),
        'day':d,
        'assinadoDoutorNome':assinadoDoutor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'custoQuarto':int(request.POST['custoQuarto'])*int(d),
            'taxaDoutor':request.POST['taxaDoutor'],
            'medicamentos' : request.POST['medicamentos'],
            'Outros' : request.POST['Outros'],
            'total':(int(request.POST['custoQuarto'])*int(d))+int(request.POST['taxaDoutor'])+int(request.POST['medicamentos'])+int(request.POST['Outros'])
        }
        pacienteDict.update(feeDict)
        
        pDD=models.PacienteAltaDetalhes()
        pDD.pacienteId=pk
        pDD.pacienteNome=paciente.get_name
        pDD.assinadoDoutorNome=assinadoDoutor[0].first_name
        pDD.endereco=paciente.endereco
        pDD.telefone=paciente.telefone
        pDD.sintomas=paciente.sintomas
        pDD.admitirData=paciente.admitirData
        pDD.saidaData=date.today()
        pDD.diaPassado=int(d)
        pDD.medicamentos=int(request.POST['medicamentos'])
        pDD.custoQuarto=int(request.POST['custoQuarto'])*int(d)
        pDD.taxaDoutor=int(request.POST['taxaDoutor'])
        pDD.Outros=int(request.POST['Outros'])
        pDD.total=(int(request.POST['custoQuarto'])*int(d))+int(request.POST['taxaDoutor'])+int(request.POST['medicamentos'])+int(request.POST['Outros'])
        pDD.save()
        return render(request,'hospital/paciente_conta.html',context=pacienteDict)
    return render(request,'hospital/paciente_gerar.html',context=pacienteDict)



##COMPROMISSO RECEPCIONISTA

@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_compromisso_view(request):
    return render(request,'hospital/recepcionista_compromisso.html')



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_view_compromisso_view(request):
    compromissos=models.Compromisso.objects.all().filter(status=True)
    return render(request,'hospital/recepcionista_ver_compromisso.html',{'compromissos':compromissos})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_add_compromisso_view(request):
    compromissoForm=forms.CompromissoForm()
    mydict={'compromissoForm':compromissoForm,}
    if request.method=='POST':
        compromissoForm=forms.CompromissoForm(request.POST)
        if compromissoForm.is_valid():
            compromisso=compromissoForm.save(commit=False)
            compromisso.doutorId=request.POST.get('doutorId')
            compromisso.pacienteId=request.POST.get('pacienteId')
            compromisso.doutorNome=models.User.objects.get(id=request.POST.get('doutorId')).first_name
            compromisso.pacienteNome=models.User.objects.get(id=request.POST.get('pacienteId')).first_name
            compromisso.status=True
            compromisso.save()
        return HttpResponseRedirect('recepcionista-ver-compromisso')
    return render(request,'hospital/recepcionista_add_compromisso.html',context=mydict)



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def recepcionista_aprovar_compromisso_view(request):
    
    compromissos=models.Compromisso.objects.all().filter(status=False)
    return render(request,'hospital/recepcionista_aprovar_compromisso.html',{'compromissos':compromissos})



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def aprovar_compromisso(request,pk):
    compromisso=models.Compromisso.objects.get(id=pk)
    compromisso.status=True
    compromisso.save()
    return redirect(reverse('recepcionista-aprovar-compromisso'))



@login_required(login_url='recepcionistalogin')
@user_passes_test(is_recepcionista)
def rejeitar_compromisso(request,pk):
    compromisso=models.Compromisso.objects.get(id=pk)
    compromisso.delete()
    return redirect('recepcionista-aprovar-compromisso')


#---------------------------------------------------------------------------------
#------------------------ RECEPCIONISTA fim visualizar ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ DOCTOR comeca visualizarr ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_painelcontrole_view(request):
    
    pacientecount=models.Paciente.objects.all().filter(status=True,assinadoDoutorId=request.user.id).count()
    compromissocount=models.Compromisso.objects.all().filter(status=True,doutorId=request.user.id).count()
    pacienteliberado=models.PacienteAltaDetalhes.objects.all().distinct().filter(assinadoDoutorNome=request.user.first_name).count()

    
    compromissos=models.Compromisso.objects.all().filter(status=True,doutorId=request.user.id).order_by('-id')
    pacienteid=[]
    for a in compromissos:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid).order_by('-id')
    compromissos=zip(compromissos,pacientes)
    mydict={
    'pacientecount':pacientecount,
    'compromissocount':compromissocount,
    'pacienteliberado':pacienteliberado,
    'compromissos':compromissos,
    'doutor':models.Doutor.objects.get(user_id=request.user.id), 
    }
    return render(request,'hospital/doutor_painelcontrole.html',context=mydict)



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_paciente_view(request):
    mydict={
    'doutor':models.Doutor.objects.get(user_id=request.user.id), 
    }
    return render(request,'hospital/doutor_paciente.html',context=mydict)





@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_view_paciente_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True,assinadoDoutorId=request.user.id)
    doutor=models.Doutor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/doutor_ver_paciente.html',{'pacientes':pacientes,'doutor':doutor})


@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def search_view(request):
    doutor=models.Doutor.objects.get(user_id=request.user.id) 
    
    query = request.GET['query']
    pacientes=models.Paciente.objects.all().filter(status=True,assinadoDoutorId=request.user.id).filter(Q(sintomas__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doutor_ver_paciente.html',{'pacientes':pacientes,'doutor':doutor})



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_view_liberado_paciente_view(request):
    liberadopacientes=models.PacienteAltaDetalhes.objects.all().distinct().filter(assinadoDoutorNome=request.user.first_name)
    doutor=models.Doutor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/doutor_ver_alta_paciente.html',{'liberadopacientes':liberadopacientes,'doutor':doutor})



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_compromisso_view(request):
    doutor=models.Doutor.objects.get(user_id=request.user.id)
    return render(request,'hospital/doutor_compromisso.html',{'doutor':doutor})



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_view_compromisso_view(request):
    doutor=models.Doutor.objects.get(user_id=request.user.id) 
    compromissos=models.Compromisso.objects.all().filter(status=True,doutorId=request.user.id)
    pacienteid=[]
    for a in compromissos:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    compromissos=zip(compromissos,pacientes)
    return render(request,'hospital/doutor_ver_compromisso.html',{'compromissos':compromissos,'doutor':doutor})



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def doutor_deletar_compromisso_view(request):
    doutor=models.Doutor.objects.get(user_id=request.user.id)
    compromissos=models.Compromisso.objects.all().filter(status=True,doutorId=request.user.id)
    pacienteid=[]
    for a in compromissos:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    compromissos=zip(compromissos,pacientes)
    return render(request,'hospital/doutor_delete_compromisso.html',{'compromissos':compromissos,'doutor':doutor})



@login_required(login_url='doutorlogin')
@user_passes_test(is_doutor)
def deletar_compromisso_view(request,pk):
    compromisso=models.Compromisso.objects.get(id=pk)
    compromisso.delete()
    doutor=models.Doutor.objects.get(user_id=request.user.id)
    compromissos=models.Compromisso.objects.all().filter(status=True,doutorId=request.user.id)
    pacienteid=[]
    for a in compromissos:
        pacienteid.append(a.pacienteId)
    pacientes=models.Paciente.objects.all().filter(status=True,user_id__in=pacienteid)
    compromissos=zip(compromissos,pacientes)
    return render(request,'hospital/doutor_delete_compromisso.html',{'compromissos':compromissos,'doutor':doutor})



#---------------------------------------------------------------------------------
#------------------------ DOUTOR FIM DE VISUALIZARR ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PACIENTE COMECO VISUALIZA ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_painelcontrole_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    doutor=models.Doutor.objects.get(user_id=paciente.assinadoDoutorId)
    mydict={
    'paciente':paciente,
    'doutorNome':doutor.get_name,
    'doutorTelefone':doutor.telefone,
    'doutorendereco':doutor.endereco,
    'sintomas':paciente.sintomas,
    'doutorDepartamento':doutor.departamento,
    'admitirData':paciente.admitirData,
    }
    return render(request,'hospital/paciente_painelcontrole.html',context=mydict)



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_compromisso_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    return render(request,'hospital/paciente_compromisso.html',{'paciente':paciente})



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_agendar_compromisso_view(request):
    compromissoForm=forms.PacienteCompromissoForm()
    paciente=models.Paciente.objects.get(user_id=request.user.id) 
    message=None
    mydict={'compromissoForm':compromissoForm,'paciente':paciente,'message':message}
    if request.method=='POST':
        compromissoForm=forms.PacienteCompromissoForm(request.POST)
        if compromissoForm.is_valid():
            print(request.POST.get('doutorId'))
            desc=request.POST.get('descricao')

            doutor=models.Doutor.objects.get(user_id=request.POST.get('doutorId'))
            
            compromisso=compromissoForm.save(commit=False)
            compromisso.doutorId=request.POST.get('doutorId')
            compromisso.pacienteId=request.user.id
            compromisso.doutorNome=models.User.objects.get(id=request.POST.get('doutorId')).first_name
            compromisso.pacienteNome=request.user.first_name
            compromisso.status=False
            compromisso.save()
        return HttpResponseRedirect('paciente-ver-compromisso')
    return render(request,'hospital/paciente_agendar_compromisso.html',context=mydict)



def paciente_view_doutor_view(request):
    doutores=models.Doutor.objects.all().filter(status=True)
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    return render(request,'hospital/paciente_ver_doutor.html',{'paciente':paciente,'doutores':doutores})



def pesquisar_doutor_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id) 
    
    
    query = request.GET['query']
    doutores=models.Doutor.objects.all().filter(status=True).filter(Q(departamento__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/paciente_ver_doutor.html',{'paciente':paciente,'doutores':doutores})




@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_view_compromisso_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    compromissos=models.Compromisso.objects.all().filter(pacienteId=request.user.id)
    return render(request,'hospital/paciente_ver_compromisso.html',{'compromissos':compromissos,'paciente':paciente})



@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_liberado_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    altaDetalhes=models.PacienteAltaDetalhes.objects.all().filter(pacienteId=paciente.id).order_by('-id')[:1]
    pacienteDict=None
    if altaDetalhes:
        pacienteDict ={
        'esta_liberado':True,
        'paciente':paciente,
        'pacienteId':paciente.id,
        'pacienteNome':paciente.get_name,
        'assinadoDoutorNome':altaDetalhes[0].assinadoDoutorNome,
        'endereco':paciente.endereco,
        'telefone':paciente.telefone,
        'sintomas':paciente.sintomas,
        'admitirData':paciente.admitirData,
        'saidaData':altaDetalhes[0].saidaData,
        'diaPassado':altaDetalhes[0].diaPassado,
        'medicamentos':altaDetalhes[0].medicamentos,
        'custoQuarto':altaDetalhes[0].custoQuarto,
        'taxaDoutor':altaDetalhes[0].taxaDoutor,
        'Outros':altaDetalhes[0].Outros,
        'total':altaDetalhes[0].total,
        }
        print(pacienteDict)
    else:
        pacienteDict={
            'esta_liberado':False,
            'paciente':paciente,
            'pacienteId':request.user.id,
        }
    return render(request,'hospital/paciente_alta.html',context=pacienteDict)


#------------------------ PACIENTE FIM VISUALIZARR  ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ SOBRE NOS E CONTATE NOS ------------------------------
#---------------------------------------------------------------------------------
def sobrenos_view(request):
    return render(request,'hospital/sobrenos.html')

def contatenos_view(request):
    sub = forms.ContatoForm()
    if request.method == 'POST':
        sub = forms.ContatoForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            nome=sub.cleaned_data['Nome']
            mensagem = sub.cleaned_data['Mensagem']
            send_mail(str(nome)+' || '+str(email),mensagem,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contatenossucesso.html')
    return render(request, 'hospital/contatenos.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN FIM DE VISUALIZACAO ------------------------------
#---------------------------------------------------------------------------------



