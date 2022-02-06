from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------ADMIN URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('sobrenos', views.sobrenos_view),
    path('contatenos', views.contatenos_view),


    path('adminclick', views.adminclick_view),
    path('recepcionistaclick', views.recepcionistaclick_view),
    path('doutorclick', views.doutorclick_view),
    path('pacienteclick', views.pacienteclick_view),

    path('admincadastro', views.admin_cadastro_view),
    path('recepcionistacadastro', views.recepcionista_cadastro_view,name='recepcionistacadastro'),
    path('doutorcadastro', views.doutor_cadastro_view,name='doutorcadastro'),
    path('pacientecadastro', views.paciente_cadastro_view),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('recepcionistalogin', LoginView.as_view(template_name='hospital/recepcionistalogin.html')),
    path('doutorlogin', LoginView.as_view(template_name='hospital/doutorlogin.html')),
    path('pacientelogin', LoginView.as_view(template_name='hospital/pacientelogin.html')),


    path('aposlogin', views.aposlogin_view,name='aposlogin'),
    path('sair', LogoutView.as_view(template_name='hospital/index.html'),name='sair'),


    path('admin-painelcontrole', views.admin_painelcontrole_view,name='admin-painelcontrole'),

    path('admin-doutor', views.admin_doutor_view,name='admin-doutor'),
    path('admin-ver-doutor', views.admin_view_doutor_view,name='admin-ver-doutor'),
    path('deletar-doutor-from-hospital/<int:pk>', views.deletar_doutor_from_hospital_view,name='deletar-doutor-from-hospital'),
    path('atualizar-doutor/<int:pk>', views.atualizar_doutor_view,name='atualizar-doutor'),
    path('admin-add-doutor', views.admin_add_doutor_view,name='admin-add-doutor'),
    path('admin-aprovar-doutor', views.admin_aprovar_doutor_view,name='admin-aprovar-doutor'),
    path('aprovar-doutor/<int:pk>', views.aprovar_doutor_view,name='aprovar-doutor'),
    path('rejeitar-doutor/<int:pk>', views.rejeitar_doutor_view,name='rejeitar-doutor'),
    path('admin-ver-doutor-especializacao',views.admin_view_doutor_especializacao_view,name='admin-ver-doutor-especializacao'),

    path('admin-recepcionista', views.admin_recepcionista_view,name='admin-recepcionista'),
    path('admin-ver-recepcionista', views.admin_view_recepcionista_view,name='admin-ver-recepcionista'),
    path('deletar-recepcionista-from-hospital/<int:pk>', views.deletar_recepcionista_from_hospital_view,name='deletar-recepcionista-from-hospital'),
    path('atualizar-recepcionista/<int:pk>', views.atualizar_recepcionista_view,name='atualizar-recepcionista'),
    path('admin-add-recepcionista', views.admin_add_recepcionista_view,name='admin-add-recepcionista'),
    path('admin-aprovar-recepcionista', views.admin_aprovar_recepcionista_view,name='admin-aprovar-recepcionista'),
    path('aprovar-recepcionista/<int:pk>', views.aprovar_recepcionista_view,name='aprovar-recepcionista'),
    path('rejeitar-recepcionista/<int:pk>', views.rejeitar_recepcionista_view,name='rejeitar-recepcionista'),

    path('admin-paciente', views.admin_paciente_view,name='admin-paciente'),
    path('admin-ver-paciente', views.admin_view_paciente_view,name='admin-ver-paciente'),
    path('deletar-paciente-from-hospital/<int:pk>', views.deletar_paciente_from_hospital_view,name='deletar-paciente-from-hospital'),
    path('atualizar-paciente/<int:pk>', views.atualizar_paciente_view,name='atualizar-paciente'),
    path('admin-add-paciente', views.admin_add_paciente_view,name='admin-add-paciente'),
    path('admin-aprovar-paciente', views.admin_aprovar_paciente_view,name='admin-aprovar-paciente'),
    path('aprovar-paciente/<int:pk>', views.aprovar_paciente_view,name='aprovar-paciente'),
    path('rejeitar-paciente/<int:pk>', views.rejeitar_paciente_view,name='rejeitar-paciente'),
    path('admin-alta-paciente', views.admin_alta_paciente_view,name='admin-alta-paciente'),
    path('alta-paciente/<int:pk>', views.alta_paciente_view,name='alta-paciente'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-compromisso', views.admin_compromisso_view,name='admin-compromisso'),
    path('admin-ver-compromisso', views.admin_view_compromisso_view,name='admin-ver-compromisso'),
    path('admin-add-compromisso', views.admin_add_compromisso_view,name='admin-add-compromisso'),
    path('admin-aprovar-compromisso', views.admin_aprovar_compromisso_view,name='admin-aprovar-compromisso'),
    path('aprovar-compromisso/<int:pk>', views.aprovar_compromisso_view,name='aprovar-compromisso'),
    path('rejeitar-compromisso/<int:pk>', views.rejeitar_compromisso_view,name='rejeitar-compromisso'),
]

#---------RECEPCIONISTA URLS-------------------------------------
urlpatterns += [

    path('',views.home_view,name=''),

    path('recepcionista-painelcontrole', views.recepcionista_painelcontrole_view,name='recepcionista-painelcontrole'),

    path('recepcionista-doutor', views.recepcionista_doutor_view,name='recepcionista-doutor'),
    path('recepcionista-ver-doutor', views.recepcionista_view_doutor_view,name='recepcionista-ver-doutor'),
    path('deletar-doutor-from/<int:pk>', views.deletar_doutor_from_hospital,name='deletar-doutor-from'),
    path('atualizar-doutor-from/<int:pk>', views.atualizar_doutor,name='atualizar-doutor-from'),
    path('recepcionista-add-doutor', views.recepcionista_add_doutor_view,name='recepcionista-add-doutor'),
    path('recepcionista-aprovar-doutor', views.recepcionista_aprovar_doutor_view,name='recepcionista-aprovar-doutor'),
    path('recepcionista-ver-doutor-especializacao',views.recepcionista_view_doutor_especializacao_view,name='recepcionista-ver-doutor-especializacao'),


    path('recepcionista-paciente', views.recepcionista_paciente_view,name='recepcionista-paciente'),
    path('recepcionista-ver-paciente', views.recepcionista_view_paciente_view,name='recepcionista-ver-paciente'),
    path('deletar-paciente-from/<int:pk>', views.deletar_paciente_from_hospital,name='deletar-paciente-from'),
    path('atualizar-paciente-from/<int:pk>', views.atualizar_paciente,name='atualizar-paciente-from'),
    path('recepcionista-add-paciente', views.recepcionista_add_paciente_view,name='recepcionista-add-paciente'),
    path('recepcionista-aprovar-paciente', views.recepcionista_aprovar_paciente_view,name='recepcionista-aprovar-paciente'),
    path('recepcionista-alta-paciente', views.recepcionista_alta_paciente_view,name='recepcionista-alta-paciente'),
    path('recep-alta-paciente/<int:pk>', views.alta_paciente,name='recep-alta-paciente'),

    path('recepcionista-compromisso', views.recepcionista_compromisso_view,name='recepcionista-compromisso'),
    path('recepcionista-ver-compromisso', views.recepcionista_view_compromisso_view,name='recepcionista-ver-compromisso'),
    path('recepcionista-add-compromisso', views.recepcionista_add_compromisso_view,name='recepcionista-add-compromisso'),
    path('recepcionista-aprovar-compromisso', views.recepcionista_aprovar_compromisso_view,name='recepcionista-aprovar-compromisso'),
    path('aprovar-compromisso-recep/<int:pk>', views.aprovar_compromisso,name='aprovar-compromisso-recep'),
    path('rejeitar-compromisso-recep/<int:pk>', views.rejeitar_compromisso,name='rejeitar-compromisso-recep'),
]

#---------DOUTOR URLS-------------------------------------
urlpatterns +=[
    path('doutor-painelcontrole', views.doutor_painelcontrole_view,name='doutor-painelcontrole'),
    path('search', views.search_view,name='search'),

    path('doutor-paciente', views.doutor_paciente_view,name='doutor-paciente'),
    path('doutor-ver-paciente', views.doutor_view_paciente_view,name='doutor-ver-paciente'),
    path('doutor-ver-alta-paciente',views.doutor_view_liberado_paciente_view,name='doutor-ver-alta-paciente'),

    path('doutor-compromisso', views.doutor_compromisso_view,name='doutor-compromisso'),
    path('doutor-ver-compromisso', views.doutor_view_compromisso_view,name='doutor-ver-compromisso'),
    path('doutor-delete-compromisso',views.doutor_deletar_compromisso_view,name='doutor-delete-compromisso'),
    path('deletar-compromisso/<int:pk>', views.deletar_compromisso_view,name='deletar-compromisso'),
]




#---------PACIENTE URLS-------------------------------------
urlpatterns +=[

    path('paciente-painelcontrole', views.paciente_painelcontrole_view,name='paciente-painelcontrole'),
    path('paciente-compromisso', views.paciente_compromisso_view,name='paciente-compromisso'),
    path('paciente-agendar-compromisso', views.paciente_agendar_compromisso_view,name='paciente-agendar-compromisso'),
    path('paciente-ver-compromisso', views.paciente_view_compromisso_view,name='paciente-ver-compromisso'),
    path('paciente-ver-doutor', views.paciente_view_doutor_view,name='paciente-ver-doutor'),
    path('pesquisar-doutor', views.pesquisar_doutor_view,name='pesquisar-doutor'),
    path('paciente-alta', views.paciente_liberado_view,name='paciente-alta'),

]


