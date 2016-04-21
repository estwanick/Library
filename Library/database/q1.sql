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


-- select d.doc_id, d.doc_title, d.doc_type, d.number_copies, u.author_name, max(i.doc_copy)
--                 from document as d
--                 inner join authoring as a
--                     on d.doc_id = a.doc_id
--                 inner join author as u
--                     on a.author_id = u.author_id
--                 inner join inventory as i
--                     on d.doc_id = i.doc_id
--                 group by i.doc_id;

-- select *
-- from document as d
-- where not exists
-- (
--     select i.doc_id
--     from inventory as i 
--     where i.lib_id = "library1"
--     and i.doc_id = d.doc_id 
-- )
-- and exists
-- (
--     select i.doc_id
--     from inventory as i 
--     where i.lib_id <> "library1"
--     and i.doc_id = d.doc_id 
-- );

-- select i.lib_id, i.doc_id, max( i.doc_copy )
-- from inventory as i
-- where i.lib_id <> 1
--   and i.doc_id = 1
--   and not exists(
--     select *
--     from borrow as b
--     where b.doc_id = i.doc_id
--         and b.doc_copy = i.doc_copy );

-- select *
-- from waiting as w
-- where w.reader_id = 'reader1'
--   and exists(
--     select *
--     from lend as l
--     where l.for_reader = w.reader_id
--       and l.status <> 'complete'
-- );

--  select d.doc_title, d.doc_id
--             from document as d
--             where not exists(
--                 select i.doc_id
--                 from inventory as i 
--                 where i.lib_id = (?)
--                 and i.doc_id = d.doc_id 
--             )
--             and exists
--             (
--                 select i.doc_id
--                 from inventory as i 
--                 where i.lib_id <> "library1"
--                 and i.doc_id = d.doc_id 
--             )and not exists
--             (
--                 select *
--                 from waiting as w
--                 where w.reader_id = 'reader1'
--                   and w.doc_id = d.doc_id
--             ); 

-- select d.doc_title, l.doc_id, l.doc_copy, l.order_date, l.delivery_date, l.status
--                     from lend as l 
--                     inner join document as d
--                         on l.doc_id = d.doc_id
--                     where l.for_reader = 'reader1';

update lend set delivery_date = '2016-04-20' where doc_id = 4;
update lend set status = 'complete' where doc_id = 4;