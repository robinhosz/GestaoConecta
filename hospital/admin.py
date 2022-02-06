from django.contrib import admin
from .models import Doutor,Recepcionista,Paciente,Compromisso,PacienteAltaDetalhes

class DoutorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doutor, DoutorAdmin)

class RecepcionistaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Recepcionista, RecepcionistaAdmin)

class PacienteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paciente, PacienteAdmin)

class CompromissoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Compromisso, CompromissoAdmin)

class PacienteAltaDetalhesAdmin(admin.ModelAdmin):
    pass
admin.site.register(PacienteAltaDetalhes, PacienteAltaDetalhesAdmin)
