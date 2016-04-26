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

-- update lend set delivery_date = '2016-04-20' where doc_id = 4;
--  update lend set delivery_date = '2016-04-20' where doc_id = '7';
-- --, max( i.doc_copy )
-- select i.lib_id, i.doc_id, max( i.doc_copy )
--             from inventory as i
--             where i.lib_id <> 'library1'
--             and i.doc_id = 2
--             and not exists
--             (
--                 select *
--                 from borrow as b
--                 where b.doc_id = i.doc_id
--                   and b.doc_copy = i.doc_copy 
--             )
--             and not exists
--             (
--                 select *
--                 from lend as l
--                 where l.doc_id = i.doc_id
--                   and l.doc_copy = i.doc_copy
--                   and l.status = 'processing'
--             );

-- select i.lib_id, i.doc_id, i.doc_copy, i.curr_location, i.doc_status, d.doc_title
--                 from inventory as i
--                 inner join document as d 
--                     on d.doc_id = i.doc_id
--                 where lib_id = 'library1' 
--                   and curr_location = 'library1'
--                   and not exists(
--                       select *
--                       from borrow as b
--                       where b.doc_id   = i.doc_id
--                         and b.doc_copy = i.doc_copy  
--                   );

-- select ar.author_name, d.doc_title, d.doc_id, k.keyword
-- from document as d
-- left join document_keyword as k
--     on d.doc_id = k.doc_id
-- left join authoring as au 
--     on au.doc_id = d.doc_id
-- left join author as ar 
--   on ar.author_id = au.author_id
-- where k.keyword  like '%james%'
--   or d.doc_title like '%james%'
--   or ar.author_name like '%james%'
--   group by doc_title;
  
  
  -- select d.doc_title, i.doc_copy, d.doc_type, i.curr_location, i.doc_id, i.lib_id
  --           from inventory as i
  --           inner join document as d 
  --           on i.doc_id = d.doc_id 
  --           where i.doc_id   = (?)

-- insert into borrow values (10, 'reader1', 'library1', 1, 4, '2016-1-1', '2016-1-10');

-- select d.doc_title, max( i.doc_copy ), i.curr_location, i.doc_id
--             from inventory as i
--             inner join document as d 
--             on i.doc_id = d.doc_id
--             where i.lib_id = 'library1'
--               and i.curr_location = 'library1'
--               and i.doc_id = 5
--             and not exists
--             (
--                 select *
--                 from borrow as b
--                 where b.doc_id   = i.doc_id
--                   and b.doc_copy = i.doc_copy
--             )
--             and not exists
--             (
--                 select *
--                 from lend as l
--                 where l.doc_id = i.doc_id
--                   and l.doc_copy = i.doc_copy
--                   and l.status = 'processing'
--             );


-- insert into borrow values (9, 'reader1', 'library1', 1, 8, '2016-1-1', '2016-1-10');

-- select * from borrow;


-- select d.doc_title, i.doc_copy, i.curr_location, i.doc_id
--             from inventory as i
--             inner join document as d 
--             on i.doc_id = d.doc_id
--             where i.lib_id = 'library1'
--               and i.curr_location = 'library1'
--             and not exists
--             (
--                 select *
--                 from borrow as b
--                 where b.doc_id   = i.doc_id
--                   and b.doc_copy = i.doc_copy
--             )
--             and not exists
--             (
--                 select *
--                 from lend as l
--                 where l.doc_id = i.doc_id
--                   and l.doc_copy = i.doc_copy
--                   and l.status = 'processing'
--             );

-- select d.doc_title, max( i.doc_copy ), d.doc_type, i.curr_location, i.doc_id, i.lib_id
--             from inventory as i
--             inner join document as d 
--                 on i.doc_id = d.doc_id
--             where i.lib_id = 'library1'
--               and i.curr_location = 'library1'
--               and i.doc_id = 5
--             and not exists
--             (
--                 select *
--                 from borrow as b
--                 where b.doc_id   = i.doc_id
--                   and b.doc_copy = i.doc_copy
--             )
--             and not exists
--             (
--                 select *
--                 from lend as l
--                 where l.doc_id = i.doc_id
--                   and l.doc_copy = i.doc_copy
--                   and l.status = 'processing'
--             );

-- select ar.author_name, d.doc_title, i.doc_id, i.doc_copy, i.lib_id
--             from inventory as i
--             inner join document as d
--                 on i.doc_id = d.doc_id
--             inner join authoring as au 
--                 on i.doc_id = au.doc_id
--             inner join author as ar 
--                 on au.author_id = ar.author_id
--             left join document_keyword as k
--                 on i.doc_id = k.doc_id  
--             where i.lib_id = 'library1'
--               and i.curr_location = 'library1'
--               and ( d.doc_title like (?) or k.keyword like (?) or ar.author_id like (?))
--             group by i.doc_id;

-- select d.doc_title, d.doc_type, i.curr_location, i.doc_id, max( i.doc_copy ),i.lib_id
--             from inventory as i
--             inner join document as d 
--                 on i.doc_id = d.doc_id
--             where i.lib_id = 'library1'
--               and i.curr_location = 'library1'
--               and i.doc_id = 8
--             and not exists
--             (
--                 select *
--                 from borrow as b
--                 where b.doc_id   = i.doc_id
--                   and b.doc_copy = i.doc_copy
--             )
--             and not exists
--             (
--                 select *
--                 from lend as l
--                 where l.doc_id = i.doc_id
--                   and l.doc_copy = i.doc_copy
--                   and l.status = 'processing'
--             )and not exists(
--                 select *
--                 from waiting as w
--                 where w.doc_id = i.doc_id
--                   and w.reader_id = 'reader1' 
--             );

select d.doc_title, i.doc_copy, i.curr_location, i.doc_id
            from inventory as i
            inner join document as d 
            on i.doc_id = d.doc_id
            where i.lib_id = 'library1'
              and i.curr_location = 'library1'
            and not exists
            (
                select *
                from borrow as b
                where b.doc_id    = i.doc_id
                  and b.reader_id = 'reader1'
            )
            and not exists
            (
                select *
                from lend as l
                where l.doc_id = i.doc_id
                  and l.doc_copy = i.doc_copy
                  and l.status = 'processing'
            )
            group by i.doc_id;