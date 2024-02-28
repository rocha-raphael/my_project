from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
#importar google autenticador
from django.contrib.auth.models import User, Group
from my_project.settings import YOUR_GOOGLE_CLIENT_ID
#importar decor para ver se esta logado
from django.contrib.auth.decorators import login_required
#Autenticar
from django.contrib.auth import logout, authenticate
from django.views.generic import TemplateView, View
from django.contrib.auth import login as djandoLogin
import re
from django.contrib.auth.mixins import LoginRequiredMixin
#teste Streaming
import cv2
import base64
import threading
import numpy as np
from django.core.mail import EmailMessage
from django.views.decorators import gzip

# Create your views here.
class index(TemplateView):
    #Nome do template na pasta /templates/
    #Paginas de autenticação, home, login e pagina de recuperação de senha
    pages = {"home":"home.html", "login":"login.html", "r_senha":"rec_senha.html"}

    def get(self, request, *args, **kwargs):
        """
        Método GET para a visualização da página, determinando a página atual com base no status de login do usuário.

        Args:
            request: Objeto de requisição HTTP.

            *args: Argumentos adicionais.
            **kwargs: Argumentos adicionais com palavras-chave.
            user_dict: Dicionario para preencher variaveis das paginas
            current_page: Qual pagina será carregada

        Returns:
            HttpResponse: Renderiza a página inicial, a página de login, dependendo do status de login.
        """
        user_dict = {}
        user_dict['YOUR_GOOGLE_CLIENT_ID'] = YOUR_GOOGLE_CLIENT_ID
        if request.user.is_authenticated:

            try:
                # Se o usuário estiver logado, define o grupo do usuário e a página inicial.
                user_dict["grupo"] = request.user.groups.first().name
                current_page = self.pages["home"]

            except AttributeError:
                # Tratar caso o usuário não tenha grupos ou request.user seja None.
                current_page = self.pages["login"]
                user_dict["erro_msg"] = (
                    "Ocorreu um problema ao determinar seu grupo de usuário. "
                    "Por favor, entre em contato com o suporte técnico."
                )
        else:
            # Se o usuário não estiver logado, define a página de login.
            current_page = self.pages["login"]
            
        return render(request, current_page, user_dict)

    def post(self, request, *args, **kwargs):

        current_page = self.pages["login"]
        #busca todos os process  do post
        current_dict = self.process_post(request)

        # verifica se senha e login foram preenchidos
        if current_dict['usuario'] and current_dict['senha']:
            current_page, erro_msg = self.authenticate_user(current_dict['usuario'], current_dict['senha']) #tenta autendicar
            current_dict = self.process_post(request) #busca as caracteristicvaas do methodo post novamente do usuário atual
            current_dict['erro_msg'] = erro_msg #inclui a mensagem de erro no dicionario atual, se houver ao tentar autenticar


        #Verificar se está autenticado
        if request.user.is_authenticated:
            """
            Verifica os botões da side-bar e direciona para a classe
            """
            if request.POST.get('container'):

                if request.POST.get('container') == 'usuarios':
                    return redirect("/index/usuarios/")

                if request.POST.get('container') == 'ponto':
                    return redirect("/index/captura/")

                current_dict["container"] = request.POST.get('container')
                current_page = self.pages["home"]

            #Clicando no botao logou deslogar
            if request.POST.get('logout'):
                logout(request)

            #Clicando no recuperar senha direciona para pagina de alteração de senha
            if request.POST.get('c_senha'):
                current_page = self.pages["r_senha"]
            # Ao clicar no botão para alterar a senha, este bloco de código verifica se todos os argumentos
            # necessários estão presentes e valida se as senhas atendem aos padrões estabelecidos.
            # Em caso de sucesso e sem erros, redireciona para a página home.
            if request.POST.get('new_pass'): 
                # Obtenção dos dados necessários do formulário
                usuario = request.POST.get('usuario')
                nova_senha = request.POST.get('nova_senha')
                confirma_nova_senha = request.POST.get('confirma_nova_senha')
                # Validar formato da senha e obter mensagem de erro, se houver
                mensagem_erro = self.validar_formato_senha(request, nova_senha, confirma_nova_senha, usuario)
                # Verificar se não há mensagem de erro
                if mensagem_erro is None:
                    try:
                        # Alterar a senha do usuário e realizar o login
                        request.user.set_password(str(nova_senha))# Define a nova senha para o usuário
                        request.user.save()# Salva as alterações no objeto do usuário
                        autenticacao = authenticate(username=usuario, password=confirma_nova_senha)# Autentica o usuário com a nova senha
                        djandoLogin(request, autenticacao)  # Realiza o login do usuário com a nova senha
                        # Redirecionar para a página home em caso de sucesso
                        current_page = self.pages["home"]
                    except Exception as e:
                        # Tratar erros durante a alteração da senha e redireciona para a página de senha
                        current_dict['erro_msg'] = f"Erro {e}."
                        current_page = self.pages["r_senha"]
                else:
                    # Caso haja mensagem de erro na validação da senha e redireciona para pagina de senha
                    current_dict['erro_msg'] = mensagem_erro
                    current_page = self.pages["r_senha"]


        return render(request, current_page, current_dict)

    def process_post(self, request):
        context = {}
        if request.method == 'POST':
            context['usuario'] = request.POST.get('usuario')
            context['senha'] = request.POST.get('senha')
            context['container'] = request.POST.get('container')
            context['usuario_logado'] = request.user
            context['nova_senha'] = request.POST.get('nova_senha')
            context['confirma_nova_senha'] = request.POST.get('confirma_nova_senha')
            context["todos_grupos"] = ['supervisor','usuario','admin']
            context["grupo"] = self.verificar_grupo(request.user)

        return context
    def authenticate_user(self, usuario, senha):
        """
        Função para autenticar um usuário.
    
        Args:
            request: Objeto de requisição HTTP.
            usuario: Nome de usuário fornecido pelo usuário.
            senha: Senha fornecida pelo usuário.
    
        Returns:
            page: pagina a ser direcionada.
            erro_msg: se houver erro 
        """
        autenticacao = authenticate(username=usuario, password=senha)
        if autenticacao:
            djandoLogin(self.request, autenticacao)
            page = self.pages["home"]
            erro_msg = ""
        else:
            # Tratar caso o usuário não tenha grupos ou request.user seja None.
            page = self.pages["login"]
            erro_msg = (
                "Ocorreu um problema ao tentar logar. "
                "Por favor, entre em contato com o suporte técnico."
            )
        return page, erro_msg


    def validar_formato_senha(self, request, senha, n_senha, usuario):
            """
            Verifica a compatibilidade e critérios de formato da senha.
            Retorna uma mensagem de erro se houver algum problema, caso contrário, retorna None.
            """
            # Verificar se as senhas são iguais
            if senha != n_senha:
                return "As senhas não são iguais. Verifique e tente novamente."

            # Verificar se a senha atende aos critérios de formato
            if len(n_senha) < 8:
                return "A senha muito curta, ao menos 8."

            # Verificar se a senha atende aos critérios de formato
            if not re.search(r'[A-Z]', n_senha):
                return "A senha precisa de ao menos 1 caracter maiúsculo."

            # Verificar se o usuário é compatível
            if str(usuario) != str(request.user):
                return "Usuário não compatível"

            # A senha atende aos critérios e é compatível
            return None

    def verificar_grupo(self, user):
        if user.groups.exists():
            # Se sim, obtém o nome do primeiro grupo
            grupo = user.groups.first().name
        else:
            # Se não pertencer a nenhum grupo, define uma mensagem apropriada
            grupo = "Sem grupo"
        return  grupo

class usuarios(LoginRequiredMixin, TemplateView):
    '''
    Essa é a classe é para incluir, editar ou excluir usuários
    '''
    #Nome do template na pasta /templates/
    pages = {"home":"home.html", "login":"login.html", "r_senha":"rec_senha.html"}
    current_page = pages['home'] # Pagina home é definida como padrão
    login_url = '/index/' # Pagina para ser direcionado cas não esteja logado

    #current_dict["grupos"] = [grupo.name for grupo in self.request.user.groups.all()]
    def get_context_data(self, **kwargs):
        # Obtém os dados de contexto padrão
        context = super().get_context_data(**kwargs)

        # Mantém o container no "usuários" após o post
        context["container"] = 'usuarios'

        # Define os grupos que podem ser escolhidos
        context["todos_grupos"] = ['usuario', 'supervisor', 'admin']

        # Sidebar da direita com nomes de usuários (excluindo 'admin' e o usuário atual)
        context["nomes"] = [nome.username for nome in User.objects.all() if nome.username not in ['admin', str(self.request.user)]]

        # Busca o nome do usuário atual
        context['nome_usuario'] = self.request.user

        # Define o usuário alvo como 'editar' por padrão (edita o usuário atual)
        context['usuario_alvo'] = 'editar'

        # Busca mais informações do usuário atual
        user = get_object_or_404(User, username=self.request.user)

        # Obter dados mais completos do usuário atual
        context['nome_completo'] = f"{user.first_name} {user.last_name}"
        context['email'] = user.email
        context['grupo'] = user.groups.first().name  # Grupo do usuário atual que indica ações de preenchimento da página
        context['grupo_primario'] = context['grupo']

        return context


    def get(self, request, *args, **kwargs):
        current_dict = self.get_context_data()
        return render(request, self.current_page, current_dict)

    def post(self, request, *args, **kwargs):
        current_dict = self.get_context_data()
        if 'adicionar' in request.POST:
        #if request.POST.get('adicionar'):
                current_dict.update({
                    'usuario_alvo': 'adicionar',
                    'nome_usuario': "",
                    'nome_completo': "",
                    'email': "",
                    'grupo_new': "",
                    'grupo_primario': "usuario"
                })
        if 'acao_botao_usuarios' in request.POST:
        #if request.POST.get('acao_botao_usuarios'):
            if request.POST.get('acao_botao_usuarios') == 'adicionar':
                current_dict['erro_msg'] = self.validar_formato_senha(request.POST.get('senha'))
                if current_dict['erro_msg'] is None:
                    erro_msg = self.add_user(request.POST.dict(), atualizar=False)
                    current_dict = self.get_context_data()
                    current_dict['erro_msg'] = erro_msg

            if request.POST.get('acao_botao_usuarios') == 'editar_atual':
                erro_msg = self.add_user(request.POST.dict(), atualizar=True)
                current_dict = self.get_context_data()
                current_dict['erro_msg'] = erro_msg

            if request.POST.get('acao_botao_usuarios') == 'editar_outro':
                erro_msg = self.add_user(request.POST.dict(), atualizar=True)
                current_dict = self.get_context_data()
                current_dict['erro_msg'] = erro_msg

        #Aqui é a side bar de nomes do lado direito para editar outros usuários
        if request.POST.get('nome_editar'):
            usuario = request.POST.get('nome_editar')
            infos = self.obter_informacoes_usuario_por_login(usuario)
            current_dict.update({
                'usuario_alvo': 'editar_outro',
                'nome_usuario': usuario,
                'nome_completo': f"{infos['primeiro_nome']} {infos['ultimo_nome']}",
                'email': infos['email'],
                'grupo_primario': infos['grupo_primario'],
                'usuarios_editar': usuario
            })
            

        if request.POST.get('excluir_usuario'):
            login = request.POST.get('login')
            try:
                # Tente encontrar o usuário pelo login
                usuario = User.objects.get(username=login)

                # Exclua o usuário
                usuario.delete()
                erro_msg = ""

            #except User.DoesNotExist:  
            except Exception as e:  
                erro_msg = "Usuário não existe"
            finally:
                current_dict = self.get_context_data()
                current_dict['erro_msg'] = erro_msg
                
        return render(request, self.current_page, current_dict)

    def add_user(self, request_data, atualizar=False):
        """
        Adiciona um novo usuário ou atualiza um existente com base nos dados fornecidos.

        Args:
            request_data (dict): Dados do usuário a serem processados.
            atualizar (bool): Indica se é uma atualização de usuário existente.

        Returns:
            str: Mensagem de erro ou string vazia em caso de sucesso.
        """
        # Extraindo informações do dicionário
        login = request_data.get('login')
        nome = request_data.get('nome')
        grupo = request_data.get('grupo')
        email = request_data.get('email')
        senha = request_data.get('senha')

        try:
            # Verificar se o usuário já existe
            if User.objects.filter(username=login).exists():
                if atualizar:
                    # Tente obter o usuário pelo login
                    usuario = User.objects.get(username=login)

                    # Atualize os dados do usuário
                    usuario.username = login
                    if len(nome.split(' ')) > 1:
                        usuario.first_name = str(nome.split(' ')[0]).strip()
                        usuario.last_name = str(" ".join(nome.split(' ')[1:])).strip()
                    else:
                        usuario.first_name = str(nome).strip()
                        usuario.last_name = ''.strip()
                    usuario.email = email

                    if senha != "0000000000":
                        usuario.set_password(senha)  # Certifique-se de usar set_password para armazenar a senha criptografada

                    # Atualize o grupo do usuário
                    usuario.groups.clear()  # Remove o usuário de todos os grupos anteriores
                    novo_grupo, criado = Group.objects.get_or_create(name=grupo)
                    usuario.groups.add(novo_grupo)

                    # Salve as alterações
                    usuario.save()

                    # Faça login novamente com as novas credenciais
                    user_atual = get_object_or_404(User, username=self.request.user)
                    if usuario == user_atual:
                        djandoLogin(self.request, usuario)

                else:
                    return "Usuário já existe"

            elif not atualizar:
                # Criar o usuário
                user = User.objects.create_user(username=login, password=senha, email=email, first_name=nome)

                # Adicionar o usuário ao grupo (se o grupo existir)
                novo_grupo, criado = Group.objects.get_or_create(name=grupo)
                user.groups.add(novo_grupo)

            return ''
        except Exception as e:
            return f"Erro ao adicionar ou atualizar usuário: {e}"

    def obter_informacoes_usuario_por_login(self ,login):
        try:
            # Tente obter o usuário pelo login
            usuario = User.objects.get(username=login)
    
            # Se o usuário for encontrado, você pode acessar as informações
            primeiro_nome = usuario.first_name
            ultimo_nome = usuario.last_name
            email = usuario.email
    
            # Obtenha o primeiro grupo do usuário, se existir
            primeiro_grupo = usuario.groups.first().name if usuario.groups.exists() else None
    
            # Agora você pode usar as informações como necessário
            return {
                'primeiro_nome': primeiro_nome,
                'ultimo_nome': ultimo_nome,
                'email': email,
                'grupo_primario': primeiro_grupo,
            }

        except User.DoesNotExist:
            # Lidere com o caso em que o usuário não existe
            return None



    def validar_formato_senha(self, senha):
            """
            Verifica a compatibilidade e critérios de formato da senha.
            Retorna uma mensagem de erro se houver algum problema, caso contrário, retorna None.
            """

            # Verificar se a senha atende aos critérios de formato
            if len(senha) < 8:
                return "A senha muito curta, ao menos 8."

            # Verificar se a senha atende aos critérios de formato
            if not re.search(r'[A-Z]', senha):
                return "A senha precisa de ao menos 1 caracter maiúsculo."

            # A senha atende aos critérios e é compatível
            return None


class CapturaView(View):
    @gzip.gzip_page
    def get(self, request, *args, **kwargs):
        try:
            cam = self.VideoCamera()
            return StreamingHttpResponse(self.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except Exception as e:
            print(f"Erro na captura de vídeo: {e}")
            return self.handle_error(request)

    # To capture video class
    class VideoCamera(object):
        def __init__(self):
            self.video = None
            threading.Thread(target=self.initialize_video, args=()).start()

        def initialize_video(self):
            try:
                self.video = cv2.VideoCapture(0)
                (self.grabbed, self.frame) = self.video.read()
            except Exception as e:
                print(f"Erro ao inicializar a câmera: {e}")

        def __del__(self):
            if self.video:
                self.video.release()

        def get_frame(self):
            if self.video:
                _, jpeg = cv2.imencode('.jpg', self.frame)
                return jpeg.tobytes()

        def update(self):
            while True:
                if self.video:
                    (self.grabbed, self.frame) = self.video.read()

    def gen(self, camera):
        while True:
            frame = camera.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def handle_error(self, request):
        return HttpResponse("Erro na captura de vídeo. Consulte os logs para obter mais informações.")