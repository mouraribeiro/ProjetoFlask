from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome do usuário:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha:', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Faça login ou crie outra conta.')


class FormLogin(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField('Login')
    lembrar_dados = BooleanField("Lembrar-me")


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do usuário:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto', validators=[FileAllowed(['jpg', 'png'])])
    curso_sql = BooleanField('SQL')
    curso_python = BooleanField('Python')
    curso_adobe = BooleanField('Adobe')
    curso_powerBi = BooleanField('Power BI')
    botao_submit_editarperfil = SubmitField('Salvar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse email.Cadastre um email diferente.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
