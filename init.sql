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
    id integer NOT NULL,
    course_id integer NOT NULL,
    rating real NOT NULL,
    slope integer NOT NULL,
    yardage integer NOT NULL,
    name character varying NOT NULL,
    hex character varying(50),
    created_on timestamp without time zone NOT NULL,
    hole1_yards integer,
    hole2_yards integer,
    hole3_yards integer,
    hole4_yards integer,
    hole5_yards integer,
    hole6_yards integer,
    hole7_yards integer,
    hole8_yards integer,
    hole9_yards integer,
    hole10_yards integer,
    hole11_yards integer,
    hole12_yards integer,
    hole13_yards integer,
    hole14_yards integer,
    hole15_yards integer,
    hole16_yards integer,
    hole17_yards integer,
    hole18_yards integer
);


ALTER TABLE public.tee_boxes OWNER TO golf_api;

--
-- Name: course_tees_id_seq; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.course_tees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_tees_id_seq OWNER TO golf_api;

--
-- Name: course_tees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: golf_api
--

ALTER SEQUENCE public.course_tees_id_seq OWNED BY public.tee_boxes.id;


--
-- Name: courses; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.courses (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(50),
    city character varying(50),
    state character varying(50),
    zip character varying(50),
    website character varying(255),
    created_on timestamp without time zone NOT NULL,
    par integer,
    hole1_par integer,
    hole2_par integer,
    hole3_par integer,
    hole4_par integer,
    hole5_par integer,
    hole6_par integer,
    hole7_par integer,
    hole8_par integer,
    hole9_par integer,
    hole10_par integer,
    hole11_par integer,
    hole12_par integer,
    hole13_par integer,
    hole14_par integer,
    hole15_par integer,
    hole16_par integer,
    hole17_par integer,
    hole18_par integer,
    hole1_handicap integer,
    hole2_handicap integer,
    hole3_handicap integer,
    hole4_handicap integer,
    hole5_handicap integer,
    hole6_handicap integer,
    hole7_handicap integer,
    hole8_handicap integer,
    hole9_handicap integer,
    hole10_handicap integer,
    hole11_handicap integer,
    hole12_handicap integer,
    hole13_handicap integer,
    hole14_handicap integer,
    hole15_handicap integer,
    hole16_handicap integer,
    hole17_handicap integer,
    hole18_handicap integer
);


ALTER TABLE public.courses OWNER TO golf_api;

--
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.courses_id_seq OWNER TO golf_api;

--
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: golf_api
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- Name: golfer_sequence; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.golfer_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.golfer_sequence OWNER TO golf_api;

--
-- Name: players; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.players (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    zip character varying(50),
    handicap character varying(255),
    ghin_number integer,
    email character varying(50),
    pid uuid DEFAULT public.uuid_generate_v4() NOT NULL
);


ALTER TABLE public.players OWNER TO golf_api;

--
-- Name: golfers_id_seq; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.golfers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.golfers_id_seq OWNER TO golf_api;

--
-- Name: golfers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: golf_api
--

ALTER SEQUENCE public.golfers_id_seq OWNED BY public.players.id;


--
-- Name: round_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.round_holes (
    id integer NOT NULL,
    round_id integer,
    hole_number integer NOT NULL,
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
-- Name: round_holes_id_seq; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.round_holes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.round_holes_id_seq OWNER TO golf_api;

--
-- Name: round_holes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: golf_api
--

ALTER SEQUENCE public.round_holes_id_seq OWNED BY public.round_holes.id;


--
-- Name: rounds; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.rounds (
    id integer NOT NULL,
    player_id integer NOT NULL,
    course_id integer NOT NULL,
    tee_box_id integer NOT NULL,
    total_score integer,
    holes integer,
    created_on timestamp without time zone NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    status character varying(16)
);


ALTER TABLE public.rounds OWNER TO golf_api;

--
-- Name: rounds_round_id_seq; Type: SEQUENCE; Schema: public; Owner: golf_api
--

CREATE SEQUENCE public.rounds_round_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rounds_round_id_seq OWNER TO golf_api;

--
-- Name: rounds_round_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: golf_api
--

ALTER SEQUENCE public.rounds_round_id_seq OWNED BY public.rounds.id;


--
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- Name: players id; Type: DEFAULT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.players ALTER COLUMN id SET DEFAULT nextval('public.golfers_id_seq'::regclass);


--
-- Name: round_holes id; Type: DEFAULT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.round_holes ALTER COLUMN id SET DEFAULT nextval('public.round_holes_id_seq'::regclass);


--
-- Name: rounds id; Type: DEFAULT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds ALTER COLUMN id SET DEFAULT nextval('public.rounds_round_id_seq'::regclass);


--
-- Name: tee_boxes id; Type: DEFAULT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_boxes ALTER COLUMN id SET DEFAULT nextval('public.course_tees_id_seq'::regclass);


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.courses (id, name, address, city, state, zip, website, created_on, par, hole1_par, hole2_par, hole3_par, hole4_par, hole5_par, hole6_par, hole7_par, hole8_par, hole9_par, hole10_par, hole11_par, hole12_par, hole13_par, hole14_par, hole15_par, hole16_par, hole17_par, hole18_par, hole1_handicap, hole2_handicap, hole3_handicap, hole4_handicap, hole5_handicap, hole6_handicap, hole7_handicap, hole8_handicap, hole9_handicap, hole10_handicap, hole11_handicap, hole12_handicap, hole13_handicap, hole14_handicap, hole15_handicap, hole16_handicap, hole17_handicap, hole18_handicap) FROM stdin;
5	TPC Louisiana	\N	\N	\N	\N	\N	2023-11-14 22:26:17.922456	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
1	Bayou Oaks - South	\N	New Orleans	Louisiana	70124	\N	2023-06-27 18:16:13.690545	72	4	3	5	4	4	4	3	4	5	4	5	4	4	3	4	4	3	5	11	7	3	13	5	15	17	9	1	14	10	18	2	8	4	12	16	6
3	Bayou Oaks - North	\N	New Orleans	Louisiana	70124	\N	2023-11-14 22:04:27.559552	69	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.players (id, name, zip, handicap, ghin_number, email, pid) FROM stdin;
1	Tiger Woods	70122	0.0	\N	tiger@postscore.dev	1d4336c9-0d30-4df8-aaeb-041d0da0ed9c
\.

--
-- Data for Name: tee_boxes; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.tee_boxes (id, course_id, rating, slope, yardage, name, hex, created_on, hole1_yards, hole2_yards, hole3_yards, hole4_yards, hole5_yards, hole6_yards, hole7_yards, hole8_yards, hole9_yards, hole10_yards, hole11_yards, hole12_yards, hole13_yards, hole14_yards, hole15_yards, hole16_yards, hole17_yards, hole18_yards) FROM stdin;
9	1	75	134	7297	Gold	#D4AF37	2023-11-24 04:37:04.844756	420	223	577	404	452	374	178	350	613	412	589	387	484	242	450	365	197	580
11	1	72	128	6640	Blue	#0047AB	2023-11-24 04:37:04.850055	385	181	546	390	413	349	145	320	571	374	547	337	451	207	395	314	177	538
12	1	71	124	6400	Blue/White	#ADD8E6	2023-11-24 04:37:04.850724	365	174	546	390	383	349	145	320	556	374	512	337	411	179	365	314	160	520
13	1	69	117	6103	White	#FFFFFF	2023-11-24 04:37:04.85137	365	174	463	281	383	333	131	299	556	357	512	318	411	179	365	296	160	520
14	1	66	109	5507	Green	#008000	2023-11-24 04:37:04.852005	308	159	437	270	359	293	113	271	463	323	479	295	329	171	341	257	138	501
15	1	64	107	5039	Red	#FF0000	2023-11-24 04:37:04.852651	289	142	421	253	334	270	101	243	390	306	413	279	323	163	334	214	120	444
10	1	73.3	131	7010	Black	#000000	2023-11-24 04:37:04.849321	406	204	556	400	433	367	164	339	589	394	562	370	466	221	434	348	192	565
\.


--
-- Name: course_tees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.course_tees_id_seq', 35, true);


--
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.courses_id_seq', 18, true);


--
-- Name: golfer_sequence; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.golfer_sequence', 1, true);


--
-- Name: golfers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.golfers_id_seq', 10, true);


--
-- Name: round_holes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.round_holes_id_seq', 14, true);


--
-- Name: rounds_round_id_seq; Type: SEQUENCE SET; Schema: public; Owner: golf_api
--

SELECT pg_catalog.setval('public.rounds_round_id_seq', 7, true);


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

