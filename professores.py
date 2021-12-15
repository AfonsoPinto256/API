# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 22:35:39 2021

@author: Afonso
"""


import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Professores(Resource): # definimos resource

    parser = reqparse.RequestParser()
    parser.add_argument('nome',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('idade',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('grau_academico',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('turmas',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    @jwt_required()
    def get(self, name): # definimos o get request
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM professores WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'Professores': {'nome': row[0], 'idade': row[1], 'grau_academico': row[2], 'turmas': row[3]}}
        return {'message': 'professor not found'}, 404

        professor = next(filter(lambda x: x['nome'] == name, professores), None)
        return {'nome': professor}, 200 if professor else 404

    def post(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM professores WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {'message': "Já existe um professor com o nome '{}' cadastrado.".format(name)}, 400

        data = Professores.parser.parse_args()
        professor = (name, data['idade'], data['grau_academico'], data['turmas'])
        query = "INSERT INTO professores VALUES (?, ?, ?, ?)"
        cursor.execute(query, professor)
        connection.commit()
        connection.close()
        return {'nome': name, 'idade': data['idade'], 'grau_academico': data['grau_academico'], 'turmas': data['turmas']}, 201 # 202 accepted - vou criar quando puder, verifique em alguns instantes


    def put(self, name):
        data = Professores.parser.parse_args()

        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM professores WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row is None:
            professor = (name, data['idade'], data['grau_academico'], data['turmas'])
            query = "INSERT INTO professores VALUES (?, ?, ?, ?)"
            cursor.execute(query, professor)
            connection.commit()
        else:
            professor = (data['idade'], data['grau_academico'], data['turmas'], name)
            query = "UPDATE professores SET idade=?, grau_academico=?, turmas=? WHERE nome=?"
            cursor.execute(query, professor)
            connection.commit()
        connection.close()
        return {'nome': name, 'idade': data['idade'], 'grau_academico': data['grau_academico'], 'turmas': data['turmas']}

    def delete(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "DELETE FROM professores WHERE nome = ?"
        result = cursor.execute(query, (name,))
        result.fetchone()

        connection.commit()
        connection.close()

        return {'message': 'professor deleted'}




class ProfessoresLista(Resource): # definimos resource
    #ItemList é uma lista de items
    def get(self): # retorna a lista de itens
        Professores = []
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM professores"
        for row in cursor.execute(query):
            Professores.append({'nome': row[0], 'idade': row[1], 'grau_academico': row[2], 'turmas': row[3]})
        return Professores