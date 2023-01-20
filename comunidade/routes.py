from flask import render_template, request, redirect, url_for, flash
from comunidade import app, database, bcrypt
from comunidade.forms import FormLogin, FormCriarConta
from comunidade.models import Usuario
from flask_login import login_user


lista_usuarios = ["Rayanne", "Cacau", "Neide", "Raimundo"]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).firtst()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_criar_conta.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f"Login feito com sucesso!Bem vindo(a) {form_login.email.data}", ' alert-success')
            return redirect(url_for('home'))
        else:
            flash(f"Falha no login. Email ou senha incorretos.", 'alert-danger')
    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data,
                          senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Conta criada com sucesso, bem vindo(a) {form_criar_conta.email.data}", 'alert-success')
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)
