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
-- Removed UUID extension
--


--
-- Removed UUID extension comments
--


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: courses; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.courses (
id TEXT PRIMARY KEY,
name character varying(50) NOT NULL,
address character varying(50),
city character varying(50),
state character varying(50),
zip character varying(50),
website character varying(50),
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.courses OWNER TO golf_api;

--
-- Name: players; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.players (
id TEXT PRIMARY KEY,
name character varying,
email character varying,
zip integer,
ghin_number integer,
handicap double precision,
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.players OWNER TO golf_api;

--
-- Name: round_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.round_holes (
id TEXT PRIMARY KEY,
round_id TEXT,
tee_box_hole_id TEXT NOT NULL,
score integer,
gir boolean,
fairway character varying,
putts integer,
penalties integer,
sand boolean,
water boolean,
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.round_holes OWNER TO golf_api;

--
-- Name: rounds; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.rounds (
id TEXT PRIMARY KEY,
player_id TEXT NOT NULL,
course_id TEXT NOT NULL,
tee_box_id TEXT NOT NULL,
total_score integer,
holes integer,
start_time timestamp without time zone,
end_time timestamp without time zone,
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.rounds OWNER TO golf_api;

--
-- Name: tee_box_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.tee_box_holes (
id TEXT PRIMARY KEY,
tee_box_id TEXT NOT NULL,
hole_number integer,
par integer,
yardage integer,
handicap integer,
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.tee_box_holes OWNER TO golf_api;

--
-- Name: tee_boxes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.tee_boxes (
id TEXT PRIMARY KEY,
name character varying(50) NOT NULL,
course_id TEXT NOT NULL,
rating double precision,
slope integer,
yardage integer,
hex character varying(50),
created_at timestamp without time zone NOT NULL,
updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.tee_boxes OWNER TO golf_api;

--
-- Name: round_holes unique_round_hole_per_round; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes
ADD CONSTRAINT unique_round_hole_per_round UNIQUE (round_id, tee_box_hole_id);


--
-- Name: round_holes round_holes_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes
ADD CONSTRAINT round_holes_round_id_fkey FOREIGN KEY (round_id) REFERENCES public.rounds(id);


--
-- Name: round_holes round_holes_tee_box_hole_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes
ADD CONSTRAINT round_holes_tee_box_hole_id_fkey FOREIGN KEY (tee_box_hole_id) REFERENCES public.tee_box_holes(id);


--
-- Name: rounds rounds_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
ADD CONSTRAINT rounds_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: rounds rounds_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
ADD CONSTRAINT rounds_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(id);


--
-- Name: rounds rounds_tee_box_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
ADD CONSTRAINT rounds_tee_box_id_fkey FOREIGN KEY (tee_box_id) REFERENCES public.tee_boxes(id);


--
-- Name: tee_box_holes tee_box_holes_tee_box_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_box_holes
ADD CONSTRAINT tee_box_holes_tee_box_id_fkey FOREIGN KEY (tee_box_id) REFERENCES public.tee_boxes(id);


--
-- Name: tee_boxes tee_boxes_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_boxes
ADD CONSTRAINT tee_boxes_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- PostgreSQL database dump complete
--

