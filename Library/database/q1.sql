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


-- insert into document values (2, "Divergent", "Book", "Action");

-- insert into inventory values ('admin', 1, 5, 'admin', 0);
insert into inventory values ('admin', 2, 0, 'admin', 0);
insert into inventory values ('admin', 2, 1, 'admin', 0);
insert into inventory values ('admin', 2, 2, 'admin', 0);
insert into inventory values ('admin', 2, 3, 'admin', 0);

-- select * from library; 
-- select * from document;
select * from inventory;

