create table Library(
	lib_id int,
	lib_name varchar,
	lib_location varchar,
	primary key(lib_id)
);

create table Waitlist(
	reader_id int,
	doc_id int,
	primary key(reader_id, doc_id)	
);

create table BorrrowHistory(
	lib_id int,
	reader_id int,
	doc_id int,
	borrow_date date,
	return_date date,
	primary key(lib_id, reader_id, doc_id)
);

create table Inventory(
	lib_id int,
	doc_id int,a
	doc_copy int,
	status int,
	primary key(lib_id, doc_id)
);

create table Author{
	author_id int,
	author_name varchar,
	primary key author_id
}

create table Authoring{
	author_id int,
	doc_id int,
	primary key(author_id, doc_id)
}

create table Document(
	doc_id int,
	doc_title varchar,
	doc_type varchar,
	doc_desc varchar,
	primary key(doc_id)
);

create table Reader(
	reader_id int,
	reader_name varchar,
	reader_type varchar,
	primary key(reader_id)
);

create table Borrow(
	lib_id int,
	reader_id int,
	doc_id int,
	borrow_date date,
	return_date date,
	primary key(reader_id, doc_id)
);

