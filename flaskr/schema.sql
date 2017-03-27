drop table if exists entires;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);