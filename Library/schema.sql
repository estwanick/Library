drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	title text not null,
	text text not null
);

drop table if exists User;
create table User(
    username varchar(50),
    password varchar(20),
    email    varchar(50),
    registered_on date
);
