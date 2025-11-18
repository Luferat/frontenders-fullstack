# app.py
# Aplicativo principal

from flask import Flask, render_template
from database import init_db
from blueprints.owner import owner_bp
from blueprints.home import home_bp
from blueprints.contacts import contacts_bp
from blueprints.newpad import newpad_bp
from blueprints.search import search_bp
from blueprints.viewpad import viewpad_bp
from blueprints.deletepad import delete_bp

app = Flask(__name__)

# Chave secreta da sessão
app.secret_key = '39888r09e748y5872y487ht43987thdj843th2ej3298t3490twh49ktgb9487tb974b74128bt97tb'

# Inicializa o banco de dados ao iniciar o aplicativo
init_db()

# Registra o blueprint para as rotas de owner
app.register_blueprint(owner_bp, url_prefix='/owner')

# Registra o blueprint da página inicial
app.register_blueprint(home_bp)

# Outros blueprints
app.register_blueprint(viewpad_bp)
app.register_blueprint(newpad_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(search_bp)
app.register_blueprint(delete_bp)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")


if __name__ == '__main__':
    app.run(debug=True)

