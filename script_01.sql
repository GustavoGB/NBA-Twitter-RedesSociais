DROP DATABASE IF EXISTS redes;
CREATE DATABASE redes;
USE redes;

CREATE TABLE jogador (
		id_jogador INT NOT NULL auto_increment,
        nome VARCHAR(80) UNIQUE,
        PRIMARY KEY (id_jogador)
);	

CREATE TABLE times (
	id_time INT NOT NULL auto_increment,
    nome VARCHAR(80),
    PRIMARY KEY (id_time)
);

CREATE TABLE transferencia (
	id_transferencia INT NOT NULL auto_increment,
    id_jogador INT NOT NULL,
    id_time INT NOT NULL,
	ano INT NOT NULL,
	FOREIGN KEY (id_jogador)
		REFERENCES jogador (id_jogador),
	FOREIGN KEY (id_time)
		REFERENCES times (id_time),
	PRIMARY KEY (id_transferencia, id_jogador, id_time, ano)
);


CREATE TABLE waived (
	id_waived INT NOT NULL auto_increment,
    id_jogador INT NOT NULL,
    id_time INT NOT NULL,
	ano INT NOT NULL,
	FOREIGN KEY (id_jogador)
		REFERENCES jogador (id_jogador),
	FOREIGN KEY (id_time)
		REFERENCES times (id_time),
	PRIMARY KEY (id_waived, id_jogador, id_time)
);

CREATE TABLE jogador_tag (
		id_jogador INT NOT NULL auto_increment,
        tag VARCHAR(80),
		FOREIGN KEY (id_jogador)
			REFERENCES jogador (id_jogador),
        PRIMARY KEY (id_jogador, tag)
);