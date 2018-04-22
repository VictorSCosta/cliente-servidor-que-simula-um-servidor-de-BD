CREATE TABLE Aluno (
    id int PRIMARY KEY AUTO_INCREMENT,
    
	matriculado BOOLEAN,
    nome varchar(255),
    idade int,
    matricula int,
    curso varchar(255),
    semestre int DEFAULT 0,
    campus ENUM('BAGE', 'ALEGRETE', 'SAO_GABRIEL','URUGUAIANA', 'LIVRAMENTO') DEFAULT 'BAGE'
);
