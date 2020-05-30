"""
PDB
SQLITE3
MONGODB
VIRTUALENV (instalar pacotes com o pip do venv)
	pip freeze > requirements.txt (exportar)
	pip install -r requirements.txt (importar)

"""
from flask import Flask
"""
Criação da instância do aplicativo.
1°) __name__ -> obrigatório. Define as dependências de localização de arquivos no projeto.
2°) static_folder="nome" -> opcional. Define um novo nome para a pasta de arquivos estáticos (possui nome padrão).
3°) template_folder="nome" -> opcional. Define um novo nome para a pasta de templates (nome padrão é "templates").
"""
app = Flask(__name__, static_folder='static', template_folder='')
#__________________________________________________________________________________________________________________

"""
Rotas -> pontos de acesso para operações da API. São acessadas pelas urls e executam as funções de endpoint.
Rotas retornam tipos de dados específicos (string, json, etc).
"""

"""
Rota Estática -> não recebe argumentos, dados, formulários, etc.
"""
@app.route('/')
def index():
	return '<h1>Hello World!</h1>'



#OBS: Declaração de rota pode ser feita de outra maneira, sem decorators!
def indexteste():
	return '<h1>Uma rota definida sem decorators!</h1>'
"""
1°) nome da rota
2°) endpoint (nome da função)
3°) função a ser executada
"""
app.add_url_rule('/rotateste', 'indexteste', indexteste)
#__________________________________________________________________________________________________________________






"""
Rota Dinâmica -> recebe argumentos tabelados na url.
Esses argumentos podem ser tipados como: <float:var>, <int:var>, <string:var> (padrão).
Atenção: valores passados por URL precisam respeitar a sintaxe da mesma, logo não aceita números negativos nem vírgula (separação de decimal é ponto).

Exemplo: http://127.0.0.1:5000/user/rodrigo/leao/22/1.86
"""
@app.route('/user/<name>/<string:surname>/<int:idade>/<float:altura>')
def user(name, surname, idade, altura):
	return f'<h1>Hello, {name} {surname}, você tem {idade} anos e possui {altura}m de altura!<h1>'
#__________________________________________________________________________________________________________________



"""
Redirecionamento -> redireciona o serviço web para outro endereço especificado.
url_for('endpoint', argumento1, argumento2, etc.) -> redireciona o serviço web para uma rota definida na aplicação, através de seu endpoint.
"""
from flask import redirect, url_for
@app.route('/google')
def google():
	return redirect('http://google.com.br', code=302)		#code é opcinal. 302 padrão.

@app.route('/redirecionamentointerno')
def redirecionamentointerno():
	return redirect(url_for('user', name='rodrigo', surname='leao', idade=22, altura=1.86))

#Exemplo: http://127.0.0.1:5000/redirecionamentointerno
#tem o mesmo efeito de
#http://127.0.0.1:5000/user/rodrigo/leao/22/1.86
#__________________________________________________________________________________________________________________





"""
Request -> objeto principal da web, se refere a requisição web feita e possui diversas informações acessíveis e úteis para o projeto.

request.method -> retorna o método da requisição que foi efetuada. 
	get -> busca dados
	head -> get sem retorno de dados
	post -> enviar dados
	put -> atualizar dados
	patch -> semelhante ao put
	delete -> retirar dados
	obs: link tabelado no browser é sempre 'get'

request.args -> acessa as variáveis passadas como argumento na url. sintaxe: url?variavel1=valor1&variavel2=valor2&etc.
request.form -> acessa os valores submetidos por um formulário.
request.files -> acessa arquivos passados.
"""
from flask import request
import json

#Definir quais métodos de requisição a rota irá aceitar ("GET" é o padrão)
@app.route('/requisicao', methods=["POST", "GET", "PUT"])
def requisicao():
	obj = {}
	obj['navegador'] = request.headers.get('User-Agent')
	obj['metodo'] = request.method
	obj['argumentos'] = request.args
	obj['formulario'] = request.form
	obj['arquivos'] = request.files
	obj['cookies'] = request.cookies.get('nomecookie')
	return json.dumps(obj)
#Exemplo: http://127.0.0.1:5000/requisicao?var1=rodrigo&var2=leao
#________________________________________________________






"""
Cookies -> armazenamento temporários e local de dados. É definido na Response.
"""
from flask import make_response

@app.route('/definircookie')
def definircookie():
	resp = make_response(redirect('/pegarcookie'))
	resp.set_cookie('teste', value='ola, mundo!')	#[value=] é opcional
	return resp


@app.route('/pegarcookie')
def pegarcookie():
	return request.cookies.get('teste')
#Exemplo: http://127.0.0.1:5000/pegarcookie
#________________________________________________________








"""
Session -> armazenamento local e temporário por instância de aba/navegador. É necessário uma chave.
"""

from flask import session
app.secret_key = '123456'

@app.route('/iniciarsessao')
def iniciarsessao():
	session['usuario'] = 'rodrigo'
	session['senha'] = 'xamazinho'

	return "Sessão iniciada com usuário e senha!"

@app.route('/verificarsessao')
def verificarsessao():
	obj = {}
	obj['usuario'] = session['usuario']
	obj['senha'] = session['senha']

	return json.dumps(obj)

@app.route('/encerrarsessao')
def encerrarsessao():
	session.pop('usuario')		#pop ou setar p None
	session.pop('senha')	

	return 'Sessão finalizada!'
#________________________________________________________







"""
Abortar -> tipos de erros e códigos de requisições web. abort só funciona para 4xx ou 5xx
1xx -> 
2xx -> 200(ok)
3xx -> 302(redirecionado)
4xx -> 400(requisição errada), 401 (não autenticado), 403 (proibido acesso), 404 (não encontrado)
5xx -> 500 (erro interno do servidor)
"""

from flask import abort

@app.route('/abortar')
def abortar():
	abort(403)
#________________________________________________________







"""
Renderizar templates -> jinja2 (sintaxe front-end) é uma forma de apresentar páginas renderizadas com dados da aplicação.
passa argumentos como dados para o front-end.
Ver arquivo app.html para tutorial jinja2.
"""

from flask import render_template

@app.route('/exibirapp')
def exibirapp():
	return render_template('app.html', nome='Rodrigo', sobrenome='Cezar Leão')
#________________________________________________________







#________________________________________________________
#Falta Upload de Arquivos
#Falta Jinja2 no app.html
#________________________________________________________

if __name__ == '__main__':
	#app.run()
	app.run(debug=True, host='127.0.0.1', port='5000')