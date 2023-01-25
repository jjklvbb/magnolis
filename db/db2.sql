

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = heap;


CREATE DATABASE work_db;

\connect work_db


CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;



CREATE TABLE public.attributes (
    attr_id integer NOT NULL,
    attr_name character varying NOT NULL,
    attr_ont integer NOT NULL
);


ALTER TABLE public.attributes OWNER TO postgres;



CREATE SEQUENCE public.attributes_attr_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attributes_attr_id_seq OWNER TO postgres;



ALTER SEQUENCE public.attributes_attr_id_seq OWNED BY public.attributes.attr_id;




CREATE TABLE public.maintable (
    main_id integer NOT NULL,
    main_doc integer NOT NULL,
    main_attr integer NOT NULL,
    main_value integer NOT NULL
);


ALTER TABLE public.maintable OWNER TO postgres;



CREATE SEQUENCE public.maintable_main_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.maintable_main_id_seq OWNER TO postgres;



ALTER SEQUENCE public.maintable_main_id_seq OWNED BY public.maintable.main_id;




CREATE TABLE public.ontologies (
    ont_id integer NOT NULL,
    ont_name character varying NOT NULL,
    ont_owner integer NOT NULL,
    attr_entity_name character varying NOT NULL,
    attr_date character varying NOT NULL
);


ALTER TABLE public.ontologies OWNER TO postgres;



CREATE SEQUENCE public.ontologies_ont_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ontologies_ont_id_seq OWNER TO postgres;



ALTER SEQUENCE public.ontologies_ont_id_seq OWNED BY public.ontologies.ont_id;




CREATE TABLE public.textdocs (
    doc_id integer NOT NULL,
    doc_name character varying NOT NULL,
    doc_ont integer NOT NULL,
    doc_text character varying
);


ALTER TABLE public.textdocs OWNER TO postgres;



CREATE SEQUENCE public.textdocs_doc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.textdocs_doc_id_seq OWNER TO postgres;


ALTER SEQUENCE public.textdocs_doc_id_seq OWNED BY public.textdocs.doc_id;


CREATE TABLE public.users (
    user_id integer NOT NULL,
    login character varying NOT NULL,
    password character varying NOT NULL
);

ALTER TABLE public.users OWNER TO postgres;


CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.users_user_id_seq OWNER TO postgres;

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


CREATE TABLE public."values" (
    value_id integer NOT NULL,
    value character varying NOT NULL
);

ALTER TABLE public."values" OWNER TO postgres;


CREATE SEQUENCE public.values_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.values_value_id_seq OWNER TO postgres;


ALTER SEQUENCE public.values_value_id_seq OWNED BY public."values".value_id;


ALTER TABLE ONLY public.attributes ALTER COLUMN attr_id SET DEFAULT nextval('public.attributes_attr_id_seq'::regclass);


ALTER TABLE ONLY public.maintable ALTER COLUMN main_id SET DEFAULT nextval('public.maintable_main_id_seq'::regclass);


ALTER TABLE ONLY public.ontologies ALTER COLUMN ont_id SET DEFAULT nextval('public.ontologies_ont_id_seq'::regclass);


ALTER TABLE ONLY public.textdocs ALTER COLUMN doc_id SET DEFAULT nextval('public.textdocs_doc_id_seq'::regclass);


ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


ALTER TABLE ONLY public."values" ALTER COLUMN value_id SET DEFAULT nextval('public.values_value_id_seq'::regclass);


INSERT INTO public.alembic_version VALUES ('63b2667118f3');


INSERT INTO public.users VALUES (1, 'kate', 'ldjlkajsdflkjdsa');


SELECT pg_catalog.setval('public.attributes_attr_id_seq', 657, true);


SELECT pg_catalog.setval('public.maintable_main_id_seq', 814, true);


SELECT pg_catalog.setval('public.ontologies_ont_id_seq', 23, true);


SELECT pg_catalog.setval('public.textdocs_doc_id_seq', 44, true);


SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


SELECT pg_catalog.setval('public.values_value_id_seq', 251, true);


ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT attributes_pkey PRIMARY KEY (attr_id);


ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT duo2_constr UNIQUE (attr_name, attr_ont);


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT duo3_constr UNIQUE (main_doc, main_attr);


ALTER TABLE ONLY public.textdocs
    ADD CONSTRAINT duo_constr UNIQUE (doc_name, doc_ont);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT login_constr UNIQUE (login);


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT maintable_pkey PRIMARY KEY (main_id);


ALTER TABLE ONLY public.ontologies
    ADD CONSTRAINT name_constr UNIQUE (ont_name, ont_owner);


ALTER TABLE ONLY public.ontologies
    ADD CONSTRAINT ontologies_pkey PRIMARY KEY (ont_id);


ALTER TABLE ONLY public.textdocs
    ADD CONSTRAINT textdocs_pkey PRIMARY KEY (doc_id);


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT trio_constr UNIQUE (main_doc, main_attr, main_value);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


ALTER TABLE ONLY public."values"
    ADD CONSTRAINT value_constr UNIQUE (value);


ALTER TABLE ONLY public."values"
    ADD CONSTRAINT values_pkey PRIMARY KEY (value_id);


ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT attributes_attr_ont_fkey FOREIGN KEY (attr_ont) REFERENCES public.ontologies(ont_id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT maintable_main_attr_fkey FOREIGN KEY (main_attr) REFERENCES public.attributes(attr_id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT maintable_main_doc_fkey FOREIGN KEY (main_doc) REFERENCES public.textdocs(doc_id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.maintable
    ADD CONSTRAINT maintable_main_value_fkey FOREIGN KEY (main_value) REFERENCES public."values"(value_id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.ontologies
    ADD CONSTRAINT ontologies_ont_owner_fkey FOREIGN KEY (ont_owner) REFERENCES public.users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.textdocs
    ADD CONSTRAINT textdocs_doc_ont_fkey FOREIGN KEY (doc_ont) REFERENCES public.ontologies(ont_id) ON UPDATE CASCADE ON DELETE CASCADE;

