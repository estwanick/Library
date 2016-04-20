PRAGMA foreign_keys = ON;
.headers on
.mode column


-- Add Location
insert into location values ('New Jersey', 'Bloomfield', 07003);
insert into location values ('New York', 'Dale', 09009);
insert into location values ('New York', 'Newark', 02039);
insert into location values ('Delaware', 'Denton', 97093);
-- Add Libraries
insert into library values ('library1', 'Bloomfield Library', 07003, 'admin');
insert into library values ('library2', 'New York Library', 09009, 'admin');
insert into library values ('library3', 'New York-Newark Library', 02039, 'admin');
insert into library values ('library4', 'Denton Library', 97093, 'admin');
-- Add Documents
insert into document values (1, 'Divergent', 'Action', 15);
insert into document values (2, 'Harry Potter ', 'Wizardry', 5);
insert into document values (3, 'Bourne', 'Action', 5);
insert into document values (4, 'Cactus', 'Story', 8);
insert into document values (5, 'Holes', 'Action', 6);
insert into document values (6, 'Illustrator', 'Document', 7);
insert into document values (7, 'MACOSX', 'Document', 7);
insert into document values (8, 'Mad Science', 'Document', 8);
-- Add Document Keyword
insert into document_keyword values (1, 'hello');
insert into document_keyword values (1, 'go');
insert into document_keyword values (1, 'bye');
insert into document_keyword values (1, 'yes');
insert into document_keyword values (1, 'no');
insert into document_keyword values (2, 'hello');
insert into document_keyword values (2, 'go');
insert into document_keyword values (2, 'bye');
insert into document_keyword values (2, 'yes');
insert into document_keyword values (2, 'no');
insert into document_keyword values (3, 'bye');
insert into document_keyword values (3, 'yes');
insert into document_keyword values (3, 'no');
insert into document_keyword values (3, 'fast');
insert into document_keyword values (3, 'quick');
insert into document_keyword values (4, 'story');
insert into document_keyword values (4, 'hello');
insert into document_keyword values (4, 'fast');
insert into document_keyword values (4, 'quick');
insert into document_keyword values (5, 'slow');
insert into document_keyword values (5, 'hello');
insert into document_keyword values (5, 'languid');
insert into document_keyword values (5, 'bye');
insert into document_keyword values (6, 'hello');
insert into document_keyword values (6, 'languid');
insert into document_keyword values (6, 'bye');
insert into document_keyword values (6, 'fast');
insert into document_keyword values (6, 'quick');
insert into document_keyword values (7, 'good');
insert into document_keyword values (7, 'really');
insert into document_keyword values (7, 'great');
insert into document_keyword values (7, 'goodness');
insert into document_keyword values (7, 'hello');
insert into document_keyword values (8, 'good');
insert into document_keyword values (8, 'really');
insert into document_keyword values (8, 'great');
insert into document_keyword values (8, 'go');
insert into document_keyword values (8, 'bye');
insert into document_keyword values (8, 'yes');
-- Add Readers
insert into reader values ('reader1','Michael','researcher','admin');
insert into reader values ('reader2','Richard','researcher','admin');
insert into reader values ('reader3','James','student','admin');
insert into reader values ('reader4','Paul','Hobby','admin');
insert into reader values ('reader5','Jazmine','student','admin');
insert into reader values ('reader6','Amanda','Hobby','admin');
-- Add Member_of
insert into member_of values ('reader1','library1');
insert into member_of values ('reader2','library1');
insert into member_of values ('reader3','library2');
insert into member_of values ('reader4','library2');
insert into member_of values ('reader5','library3');
insert into member_of values ('reader6','library4');
-- Add Inventory
insert into inventory values ('library1', 1, 1, 'library1', 0);
insert into inventory values ('library1', 1, 2, 'library1', 0);
insert into inventory values ('library1', 1, 3, 'library1', 0);
insert into inventory values ('library1', 1, 4, 'library1', 0);
insert into inventory values ('library4', 1, 5, 'library4', 0);
insert into inventory values ('library4', 1, 6, 'library4', 0);
insert into inventory values ('library4', 1, 7, 'library4', 0);
insert into inventory values ('library2', 2, 1, 'library2', 0);
insert into inventory values ('library2', 2, 2, 'library2', 0);
insert into inventory values ('library3', 2, 3, 'library3', 0);
insert into inventory values ('library3', 2, 4, 'library3', 0);
insert into inventory values ('library1', 3, 1, 'library1', 0);
insert into inventory values ('library2', 3, 2, 'library2', 0);
insert into inventory values ('library4', 3, 3, 'library4', 0);
insert into inventory values ('library4', 3, 4, 'library4', 0);
insert into inventory values ('library4', 3, 5, 'library4', 0);
insert into inventory values ('library2', 4, 1, 'library2', 0);
insert into inventory values ('library2', 4, 2, 'library2', 0);
insert into inventory values ('library3', 4, 3, 'library3', 0);
insert into inventory values ('library1', 5, 1, 'library1', 0);
insert into inventory values ('library2', 5, 2, 'library2', 0);
insert into inventory values ('library2', 5, 3, 'library2', 0);
insert into inventory values ('library4', 5, 4, 'library4', 0);
insert into inventory values ('library4', 5, 5, 'library4', 0);
insert into inventory values ('library2', 6, 1, 'library2', 0);
insert into inventory values ('library3', 6, 2, 'library3', 0);
insert into inventory values ('library3', 6, 3, 'library3', 0);
insert into inventory values ('library4', 6, 4, 'library4', 0);
insert into inventory values ('library4', 6, 5, 'library4', 0);
insert into inventory values ('library2', 7, 1, 'library2', 0);
insert into inventory values ('library3', 7, 2, 'library3', 0);
insert into inventory values ('library3', 7, 3, 'library3', 0);
insert into inventory values ('library4', 8, 1, 'library4', 0);
insert into inventory values ('library4', 8, 2, 'library4', 0);
insert into inventory values ('library4', 8, 3, 'library4', 0);
-- Add Authors
insert into author values (1,'author1');
insert into author values (2,'author2');
insert into author values (3,'author3');
insert into author values (4,'author4');
-- Add Authoring
insert into authoring values (1, 1);
insert into authoring values (1, 2);
insert into authoring values (2, 3);
insert into authoring values (2, 4);
insert into authoring values (3, 5);
insert into authoring values (3, 6);
insert into authoring values (4, 7);
insert into authoring values (4, 8);
-- Add Waiting 
-- insert into waiting values ('reader1', 1, '2016-04-16');
-- insert into waiting values ('reader2', 1, '2016-04-16');
-- insert into waiting values ('reader3', 1, '2016-04-16');
-- insert into waiting values ('reader1', 2, '2016-04-16');
-- insert into waiting values ('reader2', 2, '2016-04-16');
-- insert into waiting values ('reader3', 2, '2016-04-16');
-- Add Borrow

-- Add Return

-- Add Lend


--Print Data to console
--  select * from library;
--  select * from location;
--  select * from document;
--  select * from document_keyword;