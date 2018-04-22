#!/usr/bin/env python

import socket
import os, sys, getopt
import traceback
import hmac
import hashlib
import logging
import mensagem_pb2
import names
from communication import (
    send_message, recv_message
)
from random import ( 
    choice, randint
)
from string import (
    ascii_uppercase, ascii_letters, digits
)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5001))

    mensagem = mensagem_pb2.Mensagem()
    mensagem.tipo_operacao = 0
    for i in range(100):
        try:
            
            aluno = mensagem.aluno.add()
            aluno.nome = names.get_full_name()
            aluno.matriculado = randint(0,1)
            aluno.idade = randint(15,100)
            aluno.matricula = int(''.join([choice(digits) for n in xrange(9)]))
            aluno.curso = ''.join([choice(ascii_letters + digits) for n in xrange(5)])
            aluno.semestre = randint(1,20)
            aluno.campus = randint(1,4)

            logging.info("[Sended] Operation type: %s, Values: matriculado: %s, nome: %s, idade: %s, matricula: %s, curso: %s, semestre: %s, campus: %s", mensagem.tipo_operacao, aluno.matriculado, aluno.nome, aluno.idade, aluno.matricula, aluno.curso, aluno.semestre, mensagem_pb2.Mensagem.Aluno.Campus.Name(aluno.campus))
            
        except:
            traceback.print_exc()
        
    send_message(sock, mensagem)  
    sock.close()

