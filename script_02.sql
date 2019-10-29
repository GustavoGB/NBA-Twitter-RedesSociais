USE redes;

CREATE TABLE rivalidade (
	id_time1 INT NOT NULL,
    id_time2 INT NOT NULL,
	ano INT,
	FOREIGN KEY (id_time1)
		REFERENCES times (id_time),
	FOREIGN KEY (id_time2)
		REFERENCES times (id_time),
	PRIMARY KEY (id_time1, id_time2)
);