--
-- PostgreSQL database dump from andrea Muñoz
-- conn = psycopg2.connect(database="postgres",
--                     host="localhost",
--                     user="andreais_745",
--                     password="localhost",
--                     port=5432)
-- --

-- Dumped from database version 17.4 (Postgres.app)
-- Dumped by pg_dump version 17.4 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: taxi_management; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA taxi_management;


ALTER SCHEMA taxi_management OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: address; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.address (
    road text NOT NULL,
    number text NOT NULL,
    city text NOT NULL
);


ALTER TABLE taxi_management.address OWNER TO postgres;

--
-- Name: can_drive; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.can_drive (
    driver_name text NOT NULL,
    model_id integer NOT NULL,
    car_id integer NOT NULL
);


ALTER TABLE taxi_management.can_drive OWNER TO postgres;

--
-- Name: car; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.car (
    car_id integer NOT NULL,
    brand text
);


ALTER TABLE taxi_management.car OWNER TO postgres;

--
-- Name: client; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.client (
    name text,
    email text NOT NULL
);


ALTER TABLE taxi_management.client OWNER TO postgres;

--
-- Name: credit_card; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.credit_card (
    number character(16) NOT NULL,
    email text,
    road text NOT NULL,
    number_addr text NOT NULL,
    city text NOT NULL
);


ALTER TABLE taxi_management.credit_card OWNER TO postgres;

--
-- Name: driver; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.driver (
    name text NOT NULL,
    road text NOT NULL,
    number text NOT NULL,
    city text NOT NULL
);


ALTER TABLE taxi_management.driver OWNER TO postgres;

--
-- Name: hasaddress; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.hasaddress (
    email text NOT NULL,
    road text NOT NULL,
    number text NOT NULL,
    city text NOT NULL
);


ALTER TABLE taxi_management.hasaddress OWNER TO postgres;

--
-- Name: manager; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.manager (
    name text,
    ssn character(9) NOT NULL,
    email text
);


ALTER TABLE taxi_management.manager OWNER TO postgres;

--
-- Name: model; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.model (
    model_id integer NOT NULL,
    transmission text,
    year integer,
    color text,
    car_id integer NOT NULL
);


ALTER TABLE taxi_management.model OWNER TO postgres;

--
-- Name: rent; Type: TABLE; Schema: taxi_management; Owner: andreais_745
--

CREATE TABLE taxi_management.rent (
    rent_id integer NOT NULL,
    rent_date date,
    email text NOT NULL,
    name text NOT NULL,
    model_id integer NOT NULL,
    car_id integer NOT NULL
);


ALTER TABLE taxi_management.rent OWNER TO andreais_745;

--
-- Name: rent_rent_id_seq; Type: SEQUENCE; Schema: taxi_management; Owner: andreais_745
--

CREATE SEQUENCE taxi_management.rent_rent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE taxi_management.rent_rent_id_seq OWNER TO andreais_745;

--
-- Name: rent_rent_id_seq; Type: SEQUENCE OWNED BY; Schema: taxi_management; Owner: andreais_745
--

ALTER SEQUENCE taxi_management.rent_rent_id_seq OWNED BY taxi_management.rent.rent_id;


--
-- Name: review_id_seq; Type: SEQUENCE; Schema: taxi_management; Owner: andreais_745
--

CREATE SEQUENCE taxi_management.review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE taxi_management.review_id_seq OWNER TO andreais_745;

--
-- Name: review; Type: TABLE; Schema: taxi_management; Owner: postgres
--

CREATE TABLE taxi_management.review (
    review_id integer DEFAULT nextval('taxi_management.review_id_seq'::regclass) NOT NULL,
    rating integer,
    message text,
    name text NOT NULL,
    email text NOT NULL
);


ALTER TABLE taxi_management.review OWNER TO postgres;

--
-- Name: rent rent_id; Type: DEFAULT; Schema: taxi_management; Owner: andreais_745
--

ALTER TABLE ONLY taxi_management.rent ALTER COLUMN rent_id SET DEFAULT nextval('taxi_management.rent_rent_id_seq'::regclass);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (road, number, city);


--
-- Name: can_drive candrive_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.can_drive
    ADD CONSTRAINT candrive_pkey PRIMARY KEY (driver_name, model_id, car_id);


--
-- Name: car car_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.car
    ADD CONSTRAINT car_pkey PRIMARY KEY (car_id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (email);


--
-- Name: credit_card creditcard_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.credit_card
    ADD CONSTRAINT creditcard_pkey PRIMARY KEY (number);


--
-- Name: driver driver_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.driver
    ADD CONSTRAINT driver_pkey PRIMARY KEY (name);


--
-- Name: hasaddress hasaddress_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.hasaddress
    ADD CONSTRAINT hasaddress_pkey PRIMARY KEY (email, road, number, city);


--
-- Name: manager manager_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.manager
    ADD CONSTRAINT manager_pkey PRIMARY KEY (ssn);


--
-- Name: model model_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.model
    ADD CONSTRAINT model_pkey PRIMARY KEY (model_id, car_id);


--
-- Name: rent rent_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: andreais_745
--

ALTER TABLE ONLY taxi_management.rent
    ADD CONSTRAINT rent_pkey PRIMARY KEY (rent_id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (review_id, name);


--
-- Name: can_drive candrive_driver_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.can_drive
    ADD CONSTRAINT candrive_driver_fkey FOREIGN KEY (driver_name) REFERENCES taxi_management.driver(name);


--
-- Name: can_drive candrive_model_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.can_drive
    ADD CONSTRAINT candrive_model_fkey FOREIGN KEY (model_id, car_id) REFERENCES taxi_management.model(model_id, car_id);


--
-- Name: credit_card creditcard_address_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.credit_card
    ADD CONSTRAINT creditcard_address_fkey FOREIGN KEY (road, number_addr, city) REFERENCES taxi_management.address(road, number, city);


--
-- Name: credit_card creditcard_client_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.credit_card
    ADD CONSTRAINT creditcard_client_fkey FOREIGN KEY (email) REFERENCES taxi_management.client(email);


--
-- Name: driver driver_address_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.driver
    ADD CONSTRAINT driver_address_fkey FOREIGN KEY (road, number, city) REFERENCES taxi_management.address(road, number, city);


--
-- Name: hasaddress hasaddress_address_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.hasaddress
    ADD CONSTRAINT hasaddress_address_fkey FOREIGN KEY (road, number, city) REFERENCES taxi_management.address(road, number, city);


--
-- Name: hasaddress hasaddress_client_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.hasaddress
    ADD CONSTRAINT hasaddress_client_fkey FOREIGN KEY (email) REFERENCES taxi_management.client(email);


--
-- Name: model model_car_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.model
    ADD CONSTRAINT model_car_fkey FOREIGN KEY (car_id) REFERENCES taxi_management.car(car_id);


--
-- Name: rent rent_client_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: andreais_745
--

ALTER TABLE ONLY taxi_management.rent
    ADD CONSTRAINT rent_client_fkey FOREIGN KEY (email) REFERENCES taxi_management.client(email);


--
-- Name: rent rent_driver_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: andreais_745
--

ALTER TABLE ONLY taxi_management.rent
    ADD CONSTRAINT rent_driver_fkey FOREIGN KEY (name) REFERENCES taxi_management.driver(name);


--
-- Name: rent rent_model_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: andreais_745
--

ALTER TABLE ONLY taxi_management.rent
    ADD CONSTRAINT rent_model_fkey FOREIGN KEY (model_id, car_id) REFERENCES taxi_management.model(model_id, car_id);


--
-- Name: review review_client_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.review
    ADD CONSTRAINT review_client_fkey FOREIGN KEY (email) REFERENCES taxi_management.client(email);


--
-- Name: review review_driver_fkey; Type: FK CONSTRAINT; Schema: taxi_management; Owner: postgres
--

ALTER TABLE ONLY taxi_management.review
    ADD CONSTRAINT review_driver_fkey FOREIGN KEY (name) REFERENCES taxi_management.driver(name);


--
-- PostgreSQL database dump complete
--

