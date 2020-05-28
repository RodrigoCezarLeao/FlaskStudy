#SORT DICT POR DATA
#EDIT ROUTE AND PAGE -> FINISH CRUD
from flask import Flask, render_template, request, redirect, url_for
import json

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
	


@app.route('/savedatabase')
def savedatabase():
	fp = open('database/database.txt', 'w')
	for estudo in lista:		
		fp.write(json.dumps(estudo) + '\n')

	fp.close()	
	return redirect(url_for('index'))


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
	pid = proxPid(lista)
	app.run(debug=True, host="127.0.0.1", port="5000")