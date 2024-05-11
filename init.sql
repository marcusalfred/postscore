--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.1 (Debian 16.1-1.pgdg120+1)

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

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tee_boxes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.tee_boxes (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    course_id uuid NOT NULL,
    rating real NOT NULL,
    slope integer NOT NULL,
    yardage integer NOT NULL,
    name character varying NOT NULL,
    hex character varying(50),
    created_on timestamp without time zone NOT NULL
);


ALTER TABLE public.tee_boxes OWNER TO golf_api;


--
-- Name: courses; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.courses (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(50),
    city character varying(50),
    state character varying(50),
    zip character varying(50),
    website character varying(255),
    created_on timestamp without time zone NOT NULL,
    par integer
);


ALTER TABLE public.courses OWNER TO golf_api;


--
-- Name: players; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.players (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(50) NOT NULL,
    zip character varying(50),
    handicap character varying(255),
    ghin_number integer,
    email character varying(50),
    hashed_password character varying(50),
    is_active boolean,
    is_super boolean
    );


ALTER TABLE public.players OWNER TO golf_api;

--
-- Name: round_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.round_holes (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    round_id uuid,
    tee_box_hole_id uuid NOT NULL,
    score integer NOT NULL,
    gir boolean,
    fairway character varying(8),
    putts integer,
    penalties integer,
    sand boolean,
    water boolean,
    created_on timestamp without time zone NOT NULL
);


ALTER TABLE public.round_holes OWNER TO golf_api;


--
-- Name: rounds; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.rounds (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    player_id uuid NOT NULL,
    course_id uuid NOT NULL,
    tee_box_id uuid NOT NULL,
    total_score integer,
    holes integer,
    created_on timestamp without time zone NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    status character varying(16)
);


ALTER TABLE public.rounds OWNER TO golf_api;

--
-- Name: tee_boxes course_tees_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_boxes
    ADD CONSTRAINT course_tees_pkey PRIMARY KEY (id);


--
-- Name: courses courses_name_key; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_name_key UNIQUE (name);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: players golfers_name_key; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT golfers_name_key UNIQUE (name);


--
-- Name: players golfers_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT golfers_pkey PRIMARY KEY (id);


--
-- Name: round_holes round_holes_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes
    ADD CONSTRAINT round_holes_pkey PRIMARY KEY (id);


--
-- Name: rounds rounds_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT rounds_pkey PRIMARY KEY (id);


--
-- Name: tee_boxes course_tees_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_boxes
    ADD CONSTRAINT course_tees_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: rounds fk_round_tees; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT fk_round_tees FOREIGN KEY (tee_box_id) REFERENCES public.tee_boxes(id);


--
-- Name: round_holes round_holes_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes
    ADD CONSTRAINT round_holes_round_id_fkey FOREIGN KEY (round_id) REFERENCES public.rounds(id);


--
-- Name: rounds rounds_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT rounds_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: rounds rounds_golfer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT rounds_golfer_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(id);


--
-- PostgreSQL database dump complete
--

