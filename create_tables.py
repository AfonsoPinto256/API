# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:24:13 2021

@author: Afonso
"""

import sqlite3

connection = sqlite3.connect('uni.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS professores (id INTEGER PRIMARY KEY, nome text, idade text, grau_academico text, turmas text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY, nome text, nralunos char, media char, alunos text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, nome text, idade char, curso text, notas char, media char)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()