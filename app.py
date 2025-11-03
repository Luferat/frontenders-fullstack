from flask import Flask, render_template

app = Flask(__name__)

# Rota da página inicial
@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/newpad")
def newpad_page():
    return render_template("newpad.html")

@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")

@app.route("/search")
def search_page():
    return render_template("search.html")

if __name__ == '__main__':
    app.run(debug=True)
