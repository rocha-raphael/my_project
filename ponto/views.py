from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
import json

# Create your views here.

class ponto(LoginRequiredMixin, TemplateView):
    '''

    '''
    pages = {"home":"home.html", "login":"login.html", "r_senha":"rec_senha.html"}
    current_page = pages['home'] # Pagina home é definida como padrão
    login_url = '/index/' # Pagina para ser direcionado cas não esteja logado
    current_dict = {"nome_completo":"raphael", "container": "ponto"}



    def get(self, request, *args, **kwargs):
        print(request.GET.dict())
        user = get_object_or_404(User, username=request.user)
        self.current_dict['nome_completo'] = f"{user.first_name} {user.last_name}"
        self.current_dict['grupo'] = user.groups.first().name
        self.current_dict['login_ponto'] = None
        print(self.current_dict)

        return render(request, self.current_page, self.current_dict)
    def post(self, request, *args, **kwargs):
        print(args, kwargs)
        user = get_object_or_404(User, username=request.user)
        self.current_dict['nome_completo'] = f"{user.first_name} {user.last_name}"
        self.current_dict['grupo'] = user.groups.first().name
        self.current_dict['login_ponto'] = request.POST.get('login_ponto')

        # Obter dados mais completos do usuário atual
        nome_completo = f"{user.first_name} {user.last_name}"
        print(request.POST.dict())
        print(request.POST.get('horarioAtualizado'))
        if self.current_dict['login_ponto']:
            try:
                pass
                print(request.POST)
            except Exception as e:
                print(e)

        try:
            data = json.loads(request.body)
            print(data)

            nome_usuario = data.get('nome_usuario')
            valor_relogio = data.get('valor_relogio')
            print(nome_usuario, valor_relogio)
        except json.JSONDecodeError as e:
            print(f"Erro: {e}")
        # Faça algo com os dados recebidos
        print(self.current_dict)

        return render(request, self.current_page, self.current_dict)
