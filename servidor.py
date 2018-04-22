import MySQLdb

import datetime
import os, sys
import traceback
import socket
import hmac
import hashlib
import mensagem_pb2
import threading
from random import randint
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

from random import (
    choice, randint
)
from string import (
   ascii_uppercase, ascii_letters, digits
)
from communication import (
    send_message, recv_message, SocketReadError
)

# Seleciona todos os alunos com as informacoes enviadas na sequinte ordem
# Matriculado > Nome > Idade > Matricula > Curso > Semestre > Campus
# ou seja, a primeira informacao encontrada nessa ordem sera utilizada na busca
def select(cursor, aluno):
    sql = 'SELECT * FROM Aluno WHERE '
    
    if aluno.HasField('matriculado'):
        sql += 'matriculado = '+str(aluno.matriculado)+';'
    
    elif aluno.HasField('nome'):
        sql += 'nome = "'+str(aluno.nome)+'";'
        
    elif aluno.HasField('idade'):
        sql += 'idade = '+str(aluno.idade)+';'
        
    elif aluno.HasField('matricula'):
        sql += 'matricula = '+str(aluno.matricula)+';'
        
    elif aluno.HasField('curso'):
        sql += 'curso = "'+str(aluno.curso)+'";'
        
    elif aluno.HasField('semestre'):
        sql += 'semestre = '+str(aluno.semestre)+';'
        
    elif aluno.HasField('campus'):
        sql += 'campus = '+str(aluno.campus)+';'
        
    else:
        sql = 'SELECT * FROM Aluno;'
    
    cursor.execute(sql)
    print 'Executed: '+sql
    print ''
    result = cursor.fetchall()
    for row in result:
        print row
        
def delete(db, cursor, aluno):
    sql = 'DELETE FROM Aluno WHERE '
    
    if aluno.HasField('matriculado'):
        sql += 'matriculado = '+str(aluno.matriculado)+';'
    
    elif aluno.HasField('nome'):
        sql += 'nome = "'+str(aluno.nome)+'";'
        
    elif aluno.HasField('idade'):
        sql += 'idade = '+str(aluno.idade)+';'
        
    elif aluno.HasField('matricula'):
        sql += 'matricula = '+str(aluno.matricula)+';'
        
    elif aluno.HasField('curso'):
        sql += 'curso = "'+str(aluno.curso)+'";'
        
    elif aluno.HasField('semestre'):
        sql += 'semestre = '+str(aluno.semestre)+';'
        
    elif aluno.HasField('campus'):
        sql += 'campus = '+str(aluno.campus)+';'
    
    try:
        cursor.execute(sql)
        db.commit()
        print 'Executed: '+sql
    except:
        db.rollback()

def recebe_mensagem_do_cliente(cliente, endereco):

    while True:
        try:
            db = MySQLdb.connect("localhost","victor","","alunos" )

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            mensagem = mensagem_pb2.Mensagem()
            recebe_mensagem = recv_message(cliente)
            mensagem.ParseFromString(recebe_mensagem)
            
            sql = ''
            
            if not mensagem:
                raise error('Erro de comunicacao')
            
            start_time = datetime.datetime.now()
            if mensagem.tipo_operacao == 0:
                
                for aluno in mensagem.aluno:
                    sql = 'INSERT INTO Aluno (matriculado, nome, idade, matricula, curso, semestre, campus) VALUES ('+ str(aluno.matriculado) + ', "' + str(aluno.nome) + '", ' + str(aluno.idade) + ', ' + str(aluno.matricula) + ', "' + str(aluno.curso) + '", ' + str(aluno.semestre) + ', ' + str(aluno.campus) +');'
                    
                    
                    result = cursor.execute(sql)
                    db.commit()
                    print 'Executed: '+sql
                    
            elif mensagem.tipo_operacao == 1:
                
                for aluno in mensagem.aluno:
                    select(cursor, aluno)
                    
            elif mensagem.tipo_operacao == 2:
                for aluno in mensagem.aluno:
                    delete(db, cursor, aluno)
            
            end_time = datetime.datetime.now()
            time_delta = end_time - start_time
            print 'Start time: ' + str(start_time)
            print 'End time: ' + str(end_time)
            print 'Time delta: ' + str(time_delta)
            
            db.close()
        except (SocketReadError):
            db.close()
            cliente.close()
            return False
        except:
            db.close()
            traceback.print_exc()

if __name__ == "__main__":
    
    PORTA = 5001
    
    try:
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_socket.bind(("0.0.0.0", PORTA))
        s_socket.listen(10)
    
        logging.info ("Servidor iniciado na porta %s", str(PORTA))
    
        while True:
            (cliente, endereco) = s_socket.accept()
            logging.info ("Cliente (%s, %s) conectado" % endereco)
            threading.Thread(target = recebe_mensagem_do_cliente,args = (cliente,endereco)).start()

        s_socket.close()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Finalizando a execucacao ...")
        pass
    except:
        traceback.print_exc()
