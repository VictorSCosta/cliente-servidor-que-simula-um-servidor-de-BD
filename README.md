# SETUP
> Install necessary packages:
	
	python MySQLdb
	$ pip install MySQL-python
	
	python random name generator
	$ pip install names

	protobuf
	$ pip install protobuf

> Create a database on your mysql server and execute the sql file "mysql-create-table.sql" to create the table;

> Open file "servidor.py" and edit line 94

	db = MySQLdb.connect("localhost","victor","","alunos" )
	to
	db = MySQLdb.connect("localhost", " USERNAME ", " PASSWORD ", " DATABASE NAME ")


# INSTRUCTIONS

## INSERT
By default the client.py is setup to send a message to the server with instructions to insert 100 random generated "Alunos";
You can change this number to whatever you wish at "cliente.py" in line 29
	
	"for i in range(100):"

## SELECT
If you wish to select "alunos" from the database change the number on line 29 to 1 and change line 28 from

	"mensagem.tipo_operacao = 0"
	to
	"mensagem.tipo_operacao = 1"

## DELETE
If you wish to delete "alunos" from the database change the number on line 29 to 1 and change line 28 from

	"mensagem.tipo_operacao = 0"
	to
	"mensagem.tipo_operacao = 2"

The way the delete and select operations works is:

> client sends a message with the information of the "Aluno" it wishes to retrieve or delete
> the server searches the information on the message in the following order: 

	Matriculado > Nome > Idade > Matricula > Curso > Semestre > Campus
	
> the server uses the first info it finds in that order to delete or retrieve the "Alunos"


For this to work you need to change lines 33 to 39 in "cliente.py"

	aluno.nome = names.get_full_name()
	aluno.matriculado = randint(0,1)
	aluno.idade = randint(15,100)
	aluno.matricula = int(''.join([choice(digits) for n in xrange(9)]))
	aluno.curso = ''.join([choice(ascii_letters + digits) for n in xrange(5)])
	aluno.semestre = randint(1,20)
	aluno.campus = randint(1,4)

and leave only the field you want to search for, setting its value,
if no information is sent, the server will retrieve all the "alunos".

Example:
if you leave only the field "idade" and set value 20
	
	"aluno.idade = 20"
the server will retrieve or delete(depending on what you set in line 29) all the "alunos" that are 20 years old.

