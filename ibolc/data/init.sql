create schema ibolc;
-- TODO: Naming convention for types, tables and fields

create extension citext;

create table country (
       id serial primary key,
       iso text unique not null,
       name text unique not null,
       nice_name text not null,
       iso3 text,
       num_code smallint,
       phone_code numeric(5)

       constraint country_ck_iso_2_char
                  check (char_length(iso) = 2),
       constraint country_ck_iso3_length
                  check(char_length(iso3) = 3)
);

create table state (
       id serial primary key,
       code char(2) not null,
       name text not null
);

create domain phone_number as text
       constraint phone_number_ck_length
                  check (char_length(value) between 7 and 25)
;

create domain zipcode as text
       constraint zipcode_ck_length_limit
                  check (char_length(value) < 13)
       constraint zipcode_ck_only_numeric_hyphens
                  check(value ~ '\d{5}(-\d{4}(-\d{2})?)?')
;

create domain email as citext
       -- constraint email_ck_format
       --            check (value ~ '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
       constraint email_ck_length check (char_length(value) between 3 and 255)
;

create table branch (
       id serial primary key,
       name text not null,
       full_name text not null,
       code text
);

create table address (
       id serial primary key,
       address1 text not null,
       address2 text,
       address3 text,
       city text not null,
       state_id serial references state (id),
       zipcode zipcode not null

       constraint address_ck_address1_limit check (char_length(address1) < 120),
       constraint address_ck_address2_limit check (char_length(address2) < 120),
       constraint address_ck_address3_limit check (char_length(address3) < 120),
       constraint address_ck_city_limit check (char_length(city) < 120)
);

create type mil_component as enum (
'Active',
'National Guard',
'Reserve'
);

create table soldier (
       id serial primary key,
       first_name text not null,
       middle_name text,
       last_name text not null,
       ssn ssn,
       dob date,
       country_id serial references country (id),
       address_id serial references address (id),
       cell_phone phone_number,
       email email unique not null,
       branch_id serial references branch (id),
       component mil_component

       constraint soldier_ck_first_name_limit
                  check (char_length(first_name) < 80),
       constraint soldier_ck_middle_name_limit
                  check (char_length(middle_name) < 80),
       constraint soldier_ck_last_name_limit
                  check (char_length(last_name) < 80),
       constraint soldier_ck_age_older_17
                  check (age(dob) > '17 years')
);


create table student (
) inherits (soldier);


create table cadre (

) inherits (soldier);


create index soldier_ix_last_name on soldier (last_name);
