from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
	return render_template('index.html', database=lista)

@app.route('/add')
def add():
	return render_template('add.html')

@app.route('/excluir')
def excluir():
	id_e = int(request.args['pid'])
	for estudo in lista:
		if estudo['id'] == id_e:
			lista.remove(estudo)
			break
			
	return redirect(url_for('index'))


@app.route('/editar')
def editar():
	id_e = int(request.args['pid'])
	aux = {}
	for estudo in lista:
		if estudo['id'] == id_e:
			aux = estudo
			break

	temp = aux['data'][-4:] + '-' + aux['data'][-7:-5] + '-' + aux['data'][:2]
	aux['data'] = temp
	return render_template('edit.html', estudo=aux)


@app.route('/addestudo', methods=["POST"])
def addestudo():
	global pid
	estudo = {
		"data": request.form['i_data'][-2:] + '-' + request.form['i_data'][-5:-3] + '-' + request.form['i_data'][:4],
		"livro": request.form['i_livro'],
		"porção": request.form['i_porção'],
		"título": request.form['i_título'],
		"id": pid
	}
	pid += 1
	lista.append(estudo)	
	#return render_template('index.html', database=lista)
	return redirect(url_for('index'))


@app.route('/editestudo', methods=["POST"])
def editestudo():
	for estudo in lista:
		if estudo['id'] == int(request.form['i_pid']):
			estudo['data'] = request.form['i_data'][-2:] + '-' + request.form['i_data'][-5:-3] + '-' + request.form['i_data'][:4]
			estudo['livro'] = request.form['i_livro']
			estudo['porção'] = request.form['i_porção']
			estudo['título'] = request.form['i_título']

	return redirect(url_for('index'))


@app.route('/savedatabase')
def savedatabase():
	fp = open('database/database.txt', 'w')
	for estudo in lista:		
		fp.write(json.dumps(estudo) + '\n')

	fp.close()	
	return redirect(url_for('index'))




def sortDatabase(lista):
	for j in range(len(lista)):
		for i in range(len(lista) - 1):
			dateI = datetime.date(int(lista[i]['data'][-4:]), int(lista[i]['data'][-7:-5]), int(lista[i]['data'][:2]) )
			dateIN = datetime.date(int(lista[i+1]['data'][-4:]), int(lista[i+1]['data'][-7:-5]), int(lista[i+1]['data'][:2]) )

			if dateI > dateIN:
				lista[i], lista[i+1] = lista[i+1], lista[i]

	return lista		
		

def loaddatabase():
	fp = open('database/database.txt', 'r')
	lista = []
	for lin in fp:
		lista.append(json.loads(lin[:-1]))

	fp.close()
	return lista

def proxPid(lista):
	pid = 0
	for elem in lista:
		if elem['id'] > pid:
			pid = elem['id']

	return pid + 1

if __name__ == "__main__":
	lista = loaddatabase()
	sortDatabase(lista)
	pid = proxPid(lista)
	app.run(debug=True, host="127.0.0.1", port="5000")