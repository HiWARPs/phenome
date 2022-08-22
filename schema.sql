pragma foreign_keys = ON;
drop table if exists datacolumns;
drop table if exists submissions;
drop table if exists users;

create table users (
	id integer primary key autoincrement,
	username text not null,
	fullname text,
	email text
);

insert into users (id, username) values (1, 'admin');

create table submissions (
	id integer primary key autoincrement,
	author_id integer not null,
	date_submitted integer not null,
	title text not null,
	description text,
	datafile text not null,
	confirmed boolean not null,
	foreign key (author_id) references users(id)
);

create table datacolumns (
	subm_id integer not null,
	n integer not null,
	title text not null,
	units text not null,
	role integer not null,
	foreign key (subm_id) references submissions(id)
);
