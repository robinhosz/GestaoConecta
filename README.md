<h1 align="center">
<img src="https://user-images.githubusercontent.com/82779533/152694763-81546442-8f00-4144-a12c-f6bd92bfea2b.png" width="300px" />
</h1>
<br><br>
<p align="center">Uma aplicação web para aperfeiçoar a gestão dos hospitais e clínicas.</p>

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-funcionalidades">Funcionalidades</a> •
 <a href="#-Pré-Requesitos">Pré Requesitos</a> • 
 <a href="#-tecnologias">Tecnologias</a> • 
</p>

## 💻 Sobre o projeto

:hospital: Conecta Gestão - é uma forma de conectar a gestão com o usuário, a principal meta é revolucionar o padrão de gestão dos consultórios.

Projeto desenvolvido durante a **Cadeira de Engenharia de Software** 

<h1 align="center">
<img src="https://user-images.githubusercontent.com/82779533/152699571-387dc0a8-c456-4620-99c7-993fe47cbaee.png" width="800px" />
</h1>
<br><br>

## ⚙️ Funcionalidades

**ADMINISTRADOR**
  - [x] Pode registrar/ver/aprovar/rejeitar/excluir médico (aprovar os médicos que se candidataram a emprego em seu hospital).
  - [x] Pode admitir/ver/aprovar/rejeitar/liberar o paciente (alar o paciente quando o tratamento estiver concluído).
  - [x] Pode gerar/baixar fatura em pdf (gerar fatura de acordo com o custo do medicamento, taxa de quarto, taxa de médico e outras taxas).
  - [x] Pode visualizar/marcar/aprovar consulta (aprovar as consultas solicitadas pelo paciente).
  
  **RECEPCIONISTA**
  - [x] Pode registrar/ver/excluir médico.
  - [x] Pode ver/liberar o paciente (Dar alta ao paciente quando o tratamento estiver concluído).
  - [x] Pode gerar/baixar fatura em pdf (gerar fatura de acordo com o custo do medicamento, taxa de quarto, taxa de médico e outras taxas).
  - [x] Pode visualizar/marcar/aprovar consulta (aprovar as consultas solicitadas pelo paciente).
  
  **DOUTOR**
  - [x] Só pode visualizar os detalhes do paciente (sintomas, nome, celular) atribuídos a esse médico pelo administrador.
  - [x] Pode visualizar sua lista de pacientes dispensados (por admin).
  - [x] Pode visualizar seus compromissos, reservados pelo administrador.
  - [x] Pode excluir sua consulta, quando o médico compareceu à consulta.
  
  **PACIENTE** 
  - [x] Pode visualizar os detalhes do médico atribuído, como (especialização, celular, endereço).
  - [x] Pode visualizar o status do compromisso reservado (pendente/confirmado pelo administrador).
  - [x] Pode agendar compromissos. (aprovação exigida pelo administrador)
  - [x] Pode visualizar/baixar o pdf da fatura (somente quando esse paciente tiver alta pelo administrador).
  
  
  ## 🚀 Pré Requesitos
1. Baixe uma IDE de sua preferência, recomendo o [Visual Code](https://code.visualstudio.com/download).
2. Baixe o [Python](https://www.python.org/) (não se esqueça de marcar Adicionar ao Path ao instalar o Python)!

### Como executar o projeto
- Abra o Terminal e execute os seguintes comandos:
```
pip install django==3.0.5
pip install django-widget-tweaks
pip install xhtml2pdf
```
- Baixe esta pasta Zip do projeto e extraia-a
- Mover para a pasta do projeto no Terminal. Em seguida, execute os seguintes comandos:
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Agora digite o seguinte URL no seu navegador instalado no seu PC
```
http://127.0.0.1:8000/
```

## 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
