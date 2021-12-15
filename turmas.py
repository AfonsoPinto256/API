# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:24:45 2021

@author: Afonso
"""

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Turmas(Resource): # definimos resource

    parser = reqparse.RequestParser()
    parser.add_argument('nome',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('nralunos',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('media',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('alunos',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    @jwt_required()
    def get(self, name): # definimos o get request
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM turmas WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'Turmas': {'nome': row[0], 'nralunos': row[1], 'media': row[2], 'alunos': row[3]}}
        return {'message': 'turma not found'}, 404

        turma = next(filter(lambda x: x['nome'] == name, turmas), None)
        return {'turma': turma}, 200 if turma else 404

    def post(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()

        query = "SELECT * FROM turmas WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {'message': "Já existe uma turma com o nome '{}' cadastrado.".format(name)}, 400

        data = Turmas.parser.parse_args()
        item = (name, data['nralunos'], data['media'], data['alunos'])
        query = "INSERT INTO turmas VALUES (?, ?, ?, ?)"
        cursor.execute(query, item)
        connection.commit()
        connection.close()
        return {'turma': name, 'nralunos': data['nralunos'], 'media': data['media'], 'alunos': data['alunos']}, 201 # 202 accepted - vou criar quando puder, verifique em alguns instantes


    def put(self, name):
        data = Turmas.parser.parse_args()

        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM turmas WHERE nome = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row is None:
            item = (name, data['nralunos'], data['media'], data['alunos'])
            query = "INSERT INTO turmas VALUES (?, ?, ?, ?)"
            cursor.execute(query, item)
            connection.commit()
        else:
            item = (data['nralunos'], data['media'], data['alunos'], name)
            query = "UPDATE turmas SET nralunos=?, media=?, alunos=? WHERE nome=?"
            cursor.execute(query, item)
            connection.commit()
        connection.close()
        return {'turma': name, 'nralunos': data['nralunos'], 'media': data['media'], 'alunos': data['alunos']}

    def delete(self, name):
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "DELETE FROM turmas WHERE nome = ?"
        result = cursor.execute(query, (name,))
        result.fetchone()

        connection.commit()
        connection.close()

        return {'message': 'turma deleted'}




class TurmaLista(Resource): # definimos resource
    #ItemList é uma lista de items
    def get(self): # retorna a lista de itens
        turmas = []
        connection = sqlite3.connect('uni.db')
        cursor = connection.cursor()
        query = "SELECT * FROM turmas"
        for row in cursor.execute(query):
            turmas.append({'nome': row[0], 'nralunos': row[1], 'media': row[2], 'alunos': row[3]})
        return turmas