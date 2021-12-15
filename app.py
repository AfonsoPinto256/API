# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:23:41 2021

@author: Afonso
"""

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from alunos import Alunos, AlunosLista
from professores import Professores, ProfessoresLista
from turmas import Turmas, TurmaLista
# instalar Flask-JWT
# JWT - JSON web token

app = Flask(__name__) # nada de novo
app.secret_key = 'gelatina'
api = Api(app) # transformando o app em api

jwt = JWT(app, authenticate, identity) # cria o endpoint auth



api.add_resource(Alunos, '/alunos/<string:name>') # definimos o endpoint
api.add_resource(AlunosLista, '/alunos')
api.add_resource(Professores, '/professores/<string:name>') # definimos o endpoint
api.add_resource(ProfessoresLista, '/professores')
api.add_resource(Turmas, '/turmas/<string:name>') # definimos o endpoint
api.add_resource(TurmaLista, '/turmas')
app.run(port=5000, debug=True)

# Vamos imaginar queremos items