# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 23:03:50 2021

@author: Afonso
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 22:35:39 2021

@author: Afonso
"""


import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Alunos(Resource): # definimos resource

    parser = reqparse.RequestParser()
    parser.add_argument('nome',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('idade',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('curso',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('notas',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('media',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")

    @jwt_required()
    def get(self, name): # definimos o get request
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM alunos WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'alunos': {'nome': row[0], 'idade': row[1], 'curso': row[2], 'notas': row[3], 'media': row[4]}}
        return {'message': 'Aluno not found'}, 404

        aluno = next(filter(lambda x: x['nome'] == name, alunos), None)
        return {'nome': aluno}, 200 if aluno else 404

    def post(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM alunos WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {'message': "Já existe um aluno com o nome '{}' cadastrado.".format(name)}, 400

        data = Alunos.parser.parse_args()
        professor = (name, data['idade'], data['curso'], data['notas'], data['media'])
        query = "INSERT INTO alunos VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, professor)
        connection.commit()
        connection.close()
        return {'nome': name, 'idade': data['idade'], 'curso': data['curso'], 'notas': data['notas'], 'media': data['media']}, 201 # 202 accepted - vou criar quando puder, verifique em alguns instantes


    def put(self, name):
        data = Alunos.parser.parse_args()

        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM alunos WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row is None:
            professor = (name, data['idade'], data['curso'], data['notas'], data['media'])
            query = "INSERT INTO alunos VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, professor)
            connection.commit()
        else:
            professor = (data['idade'], data['curso'], data['notas'], name)
            query = "UPDATE alunos SET idade=?, curso=?, notas=?, media=? WHERE nome=?"
            cursor.execute(query, professor)
            connection.commit()
        connection.close()
        return {'nome': name, 'idade': data['idade'], 'curso': data['curso'], 'notas': data['notas'], 'media': data['media']}

    def delete(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "DELETE FROM alunos WHERE nome = ?"
        result = cursor.execute(query, (name,))
        result.fetchone()

        connection.commit()
        connection.close()

        return {'message': 'aluno deleted'}




class AlunosLista(Resource): # definimos resource
    #ItemList é uma lista de items
    def get(self): # retorna a lista de itens
        Alunos = []
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM alunos"
        for row in cursor.execute(query):
            Alunos.append({'nome': row[0], 'idade': row[1], 'curso': row[2], 'notas': row[3], 'media': row[4]})
        return Alunos