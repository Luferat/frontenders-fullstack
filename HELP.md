# Pequenos Ajustes e Correções

> **_DICA!_**
> - _Crie um novo branch para as alterações à seguir._

 - [ ] Edite `blueprints\view.py`

Localize a linha:
```python
def search_page(pad_id):
```

Troque o nome da função:
```python
def view_page(pad_id):
```
---

# Corrigindo a Formatação das Datas

 - [ ] Edite `app.py`

Importe `datetime`:

```python
from datetime import datetime
```
 
Adicione o `template_filter` `fmtdate` abaixo logo após a linha `app = Flask(__name__)`:

```python
@app.template_filter("fmtdate")
def fmtdate(value):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%d/%m/%Y às %H:%M")
```

 - [ ] Edite `templates\home.html` e `templates\view.html`

Em ambos os arquivos, localize:
```html
Em <em>{{ pad.pad_created_at }}</em>
```

E aplique o filtro:
```html
Em <em>{{ pad.pad_created_at | fmtdate }}</em>
```

Sempre que precisar da data formatada em um template, use o filtro `fmtdate`.

---

# Cadastro de Novo Pad

 - [ ] Edite `blueprints\newpad.py`
 - [ ] Edite `templates\newpad.html`
 
Obtenha ambos os códigos, atualizados, do repositório.

 - [ ] Edite `templates\_base.html`

Localize:
```html
<li class="nav-item mt-2 mt-md-0"><a class="nav-link is-logged d-none" href="/newpad">Novo</a></li>
```

Ajuste o link da rota para `/new`:
```html
<li class="nav-item mt-2 mt-md-0"><a class="nav-link is-logged d-none" href="/new">Novo</a></li>
```

- [ ] Edite `static\js\script.js`

Adicione o trecho abaixo no final do arquivo:

```javascript
// Fecha caixas de alerta após 5 segundos
const delayInMilliseconds = 5000;
document.addEventListener('DOMContentLoaded', function () {
    const alertElement = document.getElementById('baseMainAlert');
    if (alertElement) {
        const bsAlert = new bootstrap.Alert(alertElement);
        setTimeout(function () { bsAlert.close(); }, delayInMilliseconds);
    }
});
```

Ele tem função estética e fecha os alertas do "Bootstrap 5" após 5 segundos (5000 milissegundos).
Você pode alterar esse tempo na constante `delayInMilliseconds`, lembrando que o valor é em milissegundos (1000 milissegundos = 1 segundo).

---

# Editando um Pad

Isso dá funcionalidade para o botão `[Editar]` em `/view/{id}`.

 - [ ] Crie `blueprints\edit.py`
 - [ ] Crie `templates\edit.html`

Obtenha ambos os códigos, do repositório.

 - [ ] Edite `app.py`

Importe o `blueprint` `edit_bp`:

```python
from blueprints.edit import edit_bp 
```

Registre o blueprint logo após os outros registros:
```python
app.register_blueprint(edit_bp)
```

---

# Pesquisa

 - [ ] Edite [`templates\_base.html`](https://github.com/Luferat/frontenders-fullstack/blob/06-Pesquisa/templates/_base.html)
 
Altere a seção do formulário de pesquisa que deve ficar:

```html
<form class="order-2 order-md-1 w-100" name="searchform" method="get" action="/search">
    <div class="input-group">
        <input class="form-control" type="search" placeholder="Procurar Pad..." name="q" required minlength="2" value="{{ query }}">
        <button class="btn btn-secondary" type="submit"><i class="bi bi-search"></i></button>
    </div>
</form>
```

 - [ ] Edite [`templates\search.html`](https://github.com/Luferat/frontenders-fullstack/blob/06-Pesquisa/templates/search.html)

Vamos inserir um formulário auxiliar já que `/search` pode ser acessada diretamente e exibir os resultados da pesquisa.

 - [ ] Edite [`blueprints\search.py`](https://github.com/Luferat/frontenders-fullstack/blob/06-Pesquisa/blueprints/search.py)

Recebe a "query" da pesquisa, sanitiza e envia a pesquisa ao banco de dados.
Os resultados são exibidos pelo template `templates\search.html`.