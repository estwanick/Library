PRAGMA foreign_keys = ON;
.headers on
.mode column


-- insert into library values (101, "Bloom", "YC");

-- insert into library values (102, "New Jack", "City");

-- insert into document values (1, "Harry potter", "Book", "Wizard");

-- insert into inventory values (101, 1, 0, 101, 0);

-- insert into document_keyword values (1, "Bye");

-- insert into Author values (1, "Mike");

-- insert into Authoring values (1, 1);


-- insert into inventory values ('admin', 1, 1, 'admin', 0);
-- insert into inventory values ('admin', 1, 2, 'admin', 0);
-- insert into inventory values ('admin', 1, 3, 'admin', 0);
-- insert into inventory values ('admin', 1, 4, 'admin', 0);
-- insert into inventory values ('admin', 1, 5, 'admin', 0);
-- insert into inventory values ('admin', 1, 6, 'admin', 0);

-- insert into library values ('bloomfield', "Bloomfield library", "NJ", 'Belleville', 07003, 'pass');
-- insert into library values ('newark', "NJIT library", "NJ", 'Newark', 07105, 'pass');

-- insert into inventory values ('newark', 1, 7, 'admin', 0);
-- insert into inventory values ('newark', 1, 8, 'admin', 0);


-- insert into document values (1, "Divergent", "Book", "Action");
-- insert into document values (2, "Harry Potter ", "Book", "Something");

-- -- insert into inventory values ('admin', 1, 5, 'admin', 0);
-- insert into inventory values ('newark', 2, 4, 'newark', 0);
-- insert into inventory values ('newark', 2, 5, 'newark', 0);
-- insert into inventory values ('newark', 1, 9, 'newark', 0);
-- insert into inventory values ('newark', 1, 10, 'newark', 0);

-- -- select * from library; 
-- -- select * from document;
-- select * from inventory;

-- drop table if exists Library;
-- drop table if exists Inventory;
-- drop table if exists Document;
-- drop table if exists Document_Keyword;
-- drop table if exists Author;
-- drop table if exists Authoring;
-- drop table if exists Reader;
-- drop table if exists Borrow;
-- drop table if exists Return;
-- drop table if exists Waiting;
-- drop table if exists Lend;
-- drop table if exists Member_of;

select b.lib_id, b.doc_id, b.doc_copy, b.borrow_date, b.exp_return
    from borrow as b
        where b.reader_id = 'reader1'
            and not exists( select * 
                            from return as r
                                where r.return_id = b.borrow_id );