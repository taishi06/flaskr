drop table if exists entries;
create table entries (
	id INT(11) NOT NULL AUTO_INCREMENT,
	title TEXT NOT NULL,
	text TEXT NOT NULL,
	PRIMARY KEY (id)
);
