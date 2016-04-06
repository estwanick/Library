PRAGMA foreign_keys = ON;
.headers on
.mode column

drop table if exists Library;
drop table if exists Inventory;
drop table if exists Document;
drop table if exists Document_Keyword;
drop table if exists Author;
drop table if exists Authoring;

create table Library(
	lib_id int check( lib_id > 100 ),
	lib_name varchar,
	lib_location varchar,
	primary key(lib_id)
);

create table Inventory(
	lib_id int,
	doc_id int,
	doc_copy int,
    curr_location int,
	doc_status int,
	primary key(lib_id, doc_id, doc_copy),
    foreign key(lib_id) references Library(lib_id),
    foreign key(doc_id) references Document(doc_id)
);

create table Document(
	doc_id int,
	doc_title varchar,
	doc_type varchar,
	doc_desc varchar,
	primary key(doc_id)
);

create table Document_Keyword(
    doc_id int,
    keyword varchar,
    primary key(doc_id, keyword),
    foreign key(doc_id) references Document(doc_id)
);

create table Author(
    author_id int,
    author_name varchar,
    primary key(author_id)
);

create table Authoring(
    author_id int,
    doc_id int,
    primary key(author_id, doc_id),
    foreign key(author_id) references Author,
    foreign key(doc_id) references Document
);


