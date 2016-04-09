PRAGMA foreign_keys = ON;
.headers on
.mode column

drop table if exists Library;
drop table if exists Inventory;
drop table if exists Document;
drop table if exists Document_Keyword;
drop table if exists Author;
drop table if exists Authoring;
drop table if exists Reader;
drop table if exists Borrow;
drop table if exists Return;
drop table if exists Waiting;
drop table if exists Lend;

create table Library(
	lib_id varchar,
	lib_name varchar,
	state varchar,
    city varchar,
    zip_code int,
    password varchar,
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
    foreign key(author_id) references Author(author_id),
    foreign key(doc_id) references Document(doc_id)
);

create table Reader(
    reader_id varchar,
    lib_id int,
    reader_name varchar,
    reader_type varchar,
    password varchar,
    primary key(reader_id)
    foreign key(lib_id) references Library(lib_id)
);

create table Borrow(
    reader_id int,
    lib_id int,
    doc_id int,
    doc_copy int,
    borrow_date date,
    exp_return date,
    primary key(reader_id, lib_id, doc_id, doc_copy, borrow_date),
    foreign key(reader_id) references Reader(reader_id),
    foreign key(lib_id) references Inventory(lib_id),
    foreign key(doc_id) references Inventory(doc_id)
);

create table Return(
    reader_id int,
    lib_id int,
    doc_id int,
    doc_copy int,
    actual_return date,
    primary key(reader_id, lib_id, doc_id, actual_return),
    foreign key(reader_id) references Reader(reader_id),
    foreign key(lib_id) references Inventory,
    foreign key(doc_id) references Inventory
);

create table Waiting(
    reader_id int,
    doc_id int,
    wait_date date,
    primary key(reader_id, doc_id, wait_date)
);

create table Lend(
    to_lib int,
    from_lib int,
    order_date date,
    delivery_date date,
    doc_id int,
    doc_copy int,
    primary key(to_lib, from_lib)
);