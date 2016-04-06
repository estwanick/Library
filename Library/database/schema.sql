--Library Schema
create table if not exists Library(
    lib_id int(11),
    lib_name varchar(40),
    zip_code int(7),
    city varchar(20),
    state varchar(20),
    primary key(lib_id)
);

create table if not exists Author(
    author_id int(11),
    author_name varchar(40),
    primary key(author_id)
);

create table if not exists Authoring(
    author_id int(11),
    doc_id int(11),
    primary key(author_id, doc_id)
);

create table if not exists Document(
    doc_id int(11),
    doc_type varchar(20),
    doc_keyword varchar(20),
    doc_title varchar(40),
    total_copies int(11),
    primary key(doc_id)
);

create table if not exists Inventory(
    doc_id int(11),
    doc_copy int(11),
    lib_id int(11),
    doc_status varchar(11),
    doc_location varchar(11),
    primary key(doc_id, doc_copy, lib_id)
);

create table if not exists Reader(
    reader_id int(11),
    reader_name varchar(40),
    reader_type varchar(20),
    lib_id  int(11)
);

create table if not exists Borrow(
    doc_id int(11),
    doc_copy int(11),
    from_lib int(11),
    return_lib int(11),
    reader_id int(11),
    borrow_date datetime default current_timestamp,
    return_date datetime,
    doc_status varchar(20)
);

create table if not exists Waiting(
    doc_id int(11),
    wait_date datetime default current_timestamp,
    reader_id int(11)
);

create table if not exists Orders(
    from_lib int(11),
    to_lib int(11),
    doc_id int(11),
    doc_copy int(11),
    delivery_date datetime,
    order_date datetime default current_timestamp
);