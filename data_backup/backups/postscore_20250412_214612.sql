--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: golf_api
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO golf_api;

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
-- Name: courses; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.courses (
    id text NOT NULL,
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
    id text NOT NULL,
    name character varying(50) NOT NULL,
    zip character varying(50),
    handicap double precision,
    ghin_number character varying,
    email character varying(50),
    hashed_password character varying(128),
    is_active boolean DEFAULT true,
    is_super boolean DEFAULT false,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.players OWNER TO golf_api;

--
-- Name: round_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.round_holes (
    id text NOT NULL,
    round_id text,
    tee_box_hole_id text NOT NULL,
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
    id text NOT NULL,
    player_id text NOT NULL,
    course_id text NOT NULL,
    tee_box_id text NOT NULL,
    total_score integer,
    holes integer,
    created_on timestamp without time zone NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    status character varying(16)
);


ALTER TABLE public.rounds OWNER TO golf_api;

--
-- Name: tee_box_holes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.tee_box_holes (
    id text NOT NULL,
    tee_box_id text NOT NULL,
    hole_number integer,
    par integer,
    yardage integer,
    handicap integer,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tee_box_holes OWNER TO golf_api;

--
-- Name: tee_boxes; Type: TABLE; Schema: public; Owner: golf_api
--

CREATE TABLE public.tee_boxes (
    id text NOT NULL,
    course_id text NOT NULL,
    rating real NOT NULL,
    slope integer NOT NULL,
    yardage integer NOT NULL,
    name character varying NOT NULL,
    hex character varying(50),
    created_on timestamp without time zone NOT NULL
);


ALTER TABLE public.tee_boxes OWNER TO golf_api;

--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.courses (id, name, address, city, state, zip, website, created_on, par) FROM stdin;
01JRK6SAZY9MAQ5V6CH8761FSJ	Pine Valley Golf Club	1234 Pine Valley Road	Pine Valley	NJ	08021	https://pinevalleygolfclub.com	2025-04-11 19:56:18.302216	\N
01JRKPA0XK8024YBB1Y3Y1Y4VA	Test Golf Club	123 Fairway Drive	Golf City	CA	12345	https://testgolfclub.com	2025-04-12 00:27:33.683307	\N
01JRNBZ4QJT57A2C92RXQPBJS8	Admin Course	123 Admin St	Admin City	CA	12345	https://admin-example.com	2025-04-12 16:05:20.24277	\N
013930306362343539363166633734373466646236613536333362643066623736	Test Course Via SQL	123 Golf Lane	Golfville	CA	12345	https://testcourse.com	2025-04-13 00:02:18.321611	\N
\.


--
-- Data for Name: players; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.players (id, name, zip, handicap, ghin_number, email, hashed_password, is_active, is_super, created_on) FROM stdin;
01JRK6RDYV2QVXECVJYDJVSFPQ	John Smith	90210	12.4	12345678	john.smith@example.com	\N	\N	\N	2025-04-12 21:04:22.188578
01JRK6RPKHE6GEF54FZV1K5ADR	Sarah Johnson	60611	18.2	23456789	sarah.j@example.com	\N	\N	\N	2025-04-12 21:04:22.188578
01JRK6S290S1Y01HPW9FMSH5AM	Miguel Rodriguez	33139	7.5	34567890	miguel.r@example.com	\N	\N	\N	2025-04-12 21:04:22.188578
01JRKMW89HDN1A6X6185W5NZGH	Test User	12345	10.5	1234567	test@example.com	$2b$12$CCWJBye6YzNm4sI31qGVJObQ0NZ.ubaMqz2VW/VZcRO2kUCHQtCuG	t	\N	2025-04-12 21:04:22.188578
01JRKNHN5WG95EZ62GNRDD5FQV	Regular User	12345	15	5432109	regular@example.com	$2b$12$1NBLm8DbBXjqmMdAgQUyy.6zTHI5A6C4gKMmtblmnF7WOeafB1x72	t	t	2025-04-12 21:04:22.188578
01JRKP0F8R6R1Y9Z7CHCKR7Y4F	New User	12345	20.5	1122334	newuser@example.com	$2b$12$HNDuPF/jU.6fmMXoBZU8xeIoSfL2H1jCjunRT/bGSBk80SORa9YAu	t	f	2025-04-12 21:04:22.188578
01JRKPQHWA5DBWQ9TGGRSW9P3P	Auth Test	12345	15	1234567	testauth@example.com	$2b$12$wpI0JCXKRP2J5JtzK0YEOejhOwEXGsLJhMKG5vLa0nYAWsEslOAH.	t	f	2025-04-12 21:04:22.188578
01JRKPR5E9HD96R3P652BNCJWD	Super User	12345	15	9876543	superuser@example.com	$2b$12$pKpClGzMamftZm1bPON2TuXP8LOyK.8FT185wg..jDUn0PukcHUl6	t	f	2025-04-12 21:04:22.188578
01JRKPSD4RP6R6Y3RTBJAJNN9M	Super Admin	12345	10	9876543	superadmin@example.com	$2b$12$kQClo1ndm.VesrZRwGy8ve28zzhsoRmf4lG7aBffBp0LEmKfieK.2	t	t	2025-04-12 21:04:22.188578
01JRKQTJ0XGZE9R4D1BCJG4CM6	Mac	12345	10	7654321	mac987@gmail.com	$2b$12$PbJIqJ0fMrSq5nwh2PKmM.VOfzLNZzp2zYpHXCmwVYZ9bMpZFJqlG	t	t	2025-04-12 21:04:22.188578
01JRNBWAH1DXWR53FGHHVMDQA9	Test Regular User	12345	15	5432178	testuser@example.com	$2b$12$k.1i0fLdIbjMF7DwcbSSIeHy5Qv2aXVXTjQgSLy2fRlxgPVxzWEM2	t	f	2025-04-12 21:04:22.188578
01JRNK5NEY5P9CX7E3A5S9MKPZ	New Test User	12345	10	9876543	newtest@example.com	$2b$12$Kvy2theXQCec50fM5lxxseCCMOR6XJ7l1ynP3mV7rFLoZQEmPOdGO	t	f	2025-04-12 21:04:22.188578
01JRNK8B1S1R5MHW1QQ55D3DYB	Final Test User	12345	10	7654321	final@example.com	$2b$12$jr8b61zzeXIfElg1KklHoOvbNLnHIu/33vCbrERWm86Kmg3cH8MRu	t	f	2025-04-12 21:04:22.188578
01JRNX5C1FQK3XVEXCK5WWEGH2	Test Player	12345	10	1234567	test@example.com	\N	t	f	2025-04-12 21:05:50.127097
01JRNXPC8PXTX46Y3QMZEMKV65	Test Player 2	12345	10	1234567	test2@example.com	\N	t	f	2025-04-12 21:15:07.415259
01JRKNGMKM022862FRA8F1HHA1	Admin User	12345	10	1234567	admin@example.com	a$12$1X.GQIzB5Vz1N0ReR92kJ.Ky5/pfR.zK6Bqy91F2zfYUPvAATQsmW	t	t	2025-04-12 21:04:22.188578
\.


--
-- Data for Name: round_holes; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.round_holes (id, round_id, tee_box_hole_id, score, gir, fairway, putts, penalties, sand, water, created_on) FROM stdin;
01JRK718B1K7Q638MJ1B3NZFGP	01JRK704JTF5QBYXVTTBDSQAYH	01JRK6XDZQW6ERA3XAQHF4C580	4	t	>	2	\N	\N	\N	2025-04-11 20:00:37.726263
01JRK71FQHGWAQZ83C26TF333V	01JRK704JTF5QBYXVTTBDSQAYH	01JRK6XDZR54HZDSQN510659SE	5	f	o	3	\N	\N	\N	2025-04-11 20:00:45.29641
01JRK71P5HMVJFSQE2NF2TH15F	01JRK704JTF5QBYXVTTBDSQAYH	01JRK6XDZSJAF7M2WKNNVDXGKW	3	t	^	1	\N	\N	\N	2025-04-11 20:00:51.888246
01JRKPCZYHDRCRTPEKW7B2J1SP	01JRKPCP28X3N9B9AR65BXD5A8	01JRKPBWB791A6SQMTVTPVWCBS	5	f	o	2	\N	\N	\N	2025-04-12 00:29:10.991238
\.


--
-- Data for Name: rounds; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.rounds (id, player_id, course_id, tee_box_id, total_score, holes, created_on, start_time, end_time, status) FROM stdin;
01JRK6ZHTETQG61F8QJJAZK5Y4	01JRK6RDYV2QVXECVJYDJVSFPQ	01JRK6SAZY9MAQ5V6CH8761FSJ	01JRK6XDZNEAZBFY14RQHQH93C	87	18	2025-04-11 19:59:41.903524	\N	\N	\N
01JRK6ZX2J4QEXBB8PVGKAYAQX	01JRK6RPKHE6GEF54FZV1K5ADR	01JRK6SAZY9MAQ5V6CH8761FSJ	01JRK6XE06QT8X3JAYWQ247VEE	94	18	2025-04-11 19:59:53.427001	\N	\N	\N
01JRK704JTF5QBYXVTTBDSQAYH	01JRK6S290S1Y01HPW9FMSH5AM	01JRK6SAZY9MAQ5V6CH8761FSJ	01JRK6XDZNEAZBFY14RQHQH93C	12	3	2025-04-11 20:00:01.115099	\N	\N	\N
01JRKPCP28X3N9B9AR65BXD5A8	01JRKNGMKM022862FRA8F1HHA1	01JRKPA0XK8024YBB1Y3Y1Y4VA	01JRKPBWB2VAKMF5Q0V3KY8SJ5	5	1	2025-04-12 00:29:00.873234	\N	\N	\N
01JRKPTVS7DC4P6DWMG5H1R4Y2	01JRKPQHWA5DBWQ9TGGRSW9P3P	01JRKPA0XK8024YBB1Y3Y1Y4VA	01JRKPBWB2VAKMF5Q0V3KY8SJ5	80	9	2025-04-12 00:36:45.479836	\N	\N	\N
01JRNBXSQ3JF94Z56PC2G1F2YD	01JRNBWAH1DXWR53FGHHVMDQA9	01JRKPA0XK8024YBB1Y3Y1Y4VA	01JRKPBWB2VAKMF5Q0V3KY8SJ5	85	9	2025-04-12 16:04:36.1985	\N	\N	\N
\.


--
-- Data for Name: tee_box_holes; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.tee_box_holes (id, tee_box_id, hole_number, par, yardage, handicap, created_on) FROM stdin;
01JRK6XDZQW6ERA3XAQHF4C580	01JRK6XDZNEAZBFY14RQHQH93C	1	4	378	11	2025-04-11 19:58:32.439319
01JRK6XDZR54HZDSQN510659SE	01JRK6XDZNEAZBFY14RQHQH93C	2	4	436	7	2025-04-11 19:58:32.440539
01JRK6XDZSJAF7M2WKNNVDXGKW	01JRK6XDZNEAZBFY14RQHQH93C	3	3	181	17	2025-04-11 19:58:32.441388
01JRK6XDZT6QCY126S4CDMDCRE	01JRK6XDZNEAZBFY14RQHQH93C	4	4	490	3	2025-04-11 19:58:32.44235
01JRK6XDZVY9DM13PATWP4GY0A	01JRK6XDZNEAZBFY14RQHQH93C	5	5	591	1	2025-04-11 19:58:32.443332
01JRK6XDZWJF2W31X531YCHDME	01JRK6XDZNEAZBFY14RQHQH93C	6	3	224	13	2025-04-11 19:58:32.444276
01JRK6XDZXTNR51WW545RD5778	01JRK6XDZNEAZBFY14RQHQH93C	7	4	397	9	2025-04-11 19:58:32.445322
01JRK6XDZY766DEBGDNM3EDGYR	01JRK6XDZNEAZBFY14RQHQH93C	8	3	220	15	2025-04-11 19:58:32.446235
01JRK6XDZZST44JNZ1N1ZW1Z82	01JRK6XDZNEAZBFY14RQHQH93C	9	4	432	5	2025-04-11 19:58:32.447024
01JRK6XDZZHGETXC67K70B85WA	01JRK6XDZNEAZBFY14RQHQH93C	10	4	428	6	2025-04-11 19:58:32.447721
01JRK6XE00Z2M2TST579J3NFST	01JRK6XDZNEAZBFY14RQHQH93C	11	3	210	14	2025-04-11 19:58:32.44854
01JRK6XE010B9DZMZQ4N59X3MZ	01JRK6XDZNEAZBFY14RQHQH93C	12	4	467	4	2025-04-11 19:58:32.449515
01JRK6XE02W068SP0Q4KDM7SXB	01JRK6XDZNEAZBFY14RQHQH93C	13	5	562	2	2025-04-11 19:58:32.450284
01JRK6XE03M60DDA8PB924YXMK	01JRK6XDZNEAZBFY14RQHQH93C	14	3	178	16	2025-04-11 19:58:32.450965
01JRK6XE03HDRXNCE12GE62MAF	01JRK6XDZNEAZBFY14RQHQH93C	15	4	421	10	2025-04-11 19:58:32.45167
01JRK6XE04TQ37YK5GQQSZYM6Q	01JRK6XDZNEAZBFY14RQHQH93C	16	4	442	8	2025-04-11 19:58:32.452313
01JRK6XE05Z51NT37JM82VFR8A	01JRK6XDZNEAZBFY14RQHQH93C	17	3	215	18	2025-04-11 19:58:32.45295
01JRK6XE052DZAPCJXS3PVQ86F	01JRK6XDZNEAZBFY14RQHQH93C	18	4	423	12	2025-04-11 19:58:32.453613
01JRK6XE0624J5MQWTW2JAFWBS	01JRK6XE06QT8X3JAYWQ247VEE	1	4	348	11	2025-04-11 19:58:32.454737
01JRK6XE07NJVG02PFYED2NX81	01JRK6XE06QT8X3JAYWQ247VEE	2	4	401	7	2025-04-11 19:58:32.455392
01JRK6XE089NFTQ61ETHXX40VN	01JRK6XE06QT8X3JAYWQ247VEE	3	3	164	17	2025-04-11 19:58:32.456085
01JRK6XE08BF0GRMCCMZ39HJ1J	01JRK6XE06QT8X3JAYWQ247VEE	4	4	452	3	2025-04-11 19:58:32.456734
01JRK6XE09Q61JHGRRPWT0AX3R	01JRK6XE06QT8X3JAYWQ247VEE	5	5	545	1	2025-04-11 19:58:32.457375
01JRK6XE0AWJJ9CB68Q3SBJ2ZF	01JRK6XE06QT8X3JAYWQ247VEE	6	3	198	13	2025-04-11 19:58:32.458025
01JRK6XE0B2K5M2M8DMSYNA1PX	01JRK6XE06QT8X3JAYWQ247VEE	7	4	366	9	2025-04-11 19:58:32.458715
01JRK6XE0CBJMJNMBD3AJT8C83	01JRK6XE06QT8X3JAYWQ247VEE	8	3	189	15	2025-04-11 19:58:32.45978
01JRK6XE0C2CTWSS71H64DDW5M	01JRK6XE06QT8X3JAYWQ247VEE	9	4	401	5	2025-04-11 19:58:32.460638
01JRK6XE0D76XEVT20V0ER6MM7	01JRK6XE06QT8X3JAYWQ247VEE	10	4	396	6	2025-04-11 19:58:32.461386
01JRK6XE0EFVGA5PXC5S87RD15	01JRK6XE06QT8X3JAYWQ247VEE	11	3	185	14	2025-04-11 19:58:32.462129
01JRK6XE0F5GGP6JVPP6BF61ZD	01JRK6XE06QT8X3JAYWQ247VEE	12	4	427	4	2025-04-11 19:58:32.462822
01JRK6XE0FT61FBSFZJQ78HAYT	01JRK6XE06QT8X3JAYWQ247VEE	13	5	519	2	2025-04-11 19:58:32.463466
01JRK6XE0G6HH32DX6WXK8VTBC	01JRK6XE06QT8X3JAYWQ247VEE	14	3	155	16	2025-04-11 19:58:32.464077
01JRK6XE0HYVAPKMQNTXQMV17H	01JRK6XE06QT8X3JAYWQ247VEE	15	4	389	10	2025-04-11 19:58:32.464958
01JRK6XE0HPZX0S12DFW1YV9HK	01JRK6XE06QT8X3JAYWQ247VEE	16	4	407	8	2025-04-11 19:58:32.465626
01JRK6XE0JKQ1H0T0M7C47G4N5	01JRK6XE06QT8X3JAYWQ247VEE	17	3	186	18	2025-04-11 19:58:32.466277
01JRK6XE0J0BSB75C1DQ09NHBB	01JRK6XE06QT8X3JAYWQ247VEE	18	4	392	12	2025-04-11 19:58:32.466807
01JRKPBWB791A6SQMTVTPVWCBS	01JRKPBWB2VAKMF5Q0V3KY8SJ5	1	4	350	10	2025-04-12 00:28:34.534651
01JRKPBWBCBJBNJM1S81H81KWZ	01JRKPBWB2VAKMF5Q0V3KY8SJ5	2	4	400	8	2025-04-12 00:28:34.539506
01JRKPBWBDAK2Z2KXYNTG8RAY3	01JRKPBWB2VAKMF5Q0V3KY8SJ5	3	3	170	16	2025-04-12 00:28:34.540964
01JRKPBWBEBYPZM94F061NTQ6P	01JRKPBWB2VAKMF5Q0V3KY8SJ5	4	5	520	2	2025-04-12 00:28:34.542216
01JRKPBWBF2J4ZXZTKJBR05PT0	01JRKPBWB2VAKMF5Q0V3KY8SJ5	5	4	380	12	2025-04-12 00:28:34.54314
01JRKPBWBG66Q44MTD3V50ZH5E	01JRKPBWB2VAKMF5Q0V3KY8SJ5	6	3	180	14	2025-04-12 00:28:34.543957
01JRKPBWBH9CMD3QQJTXEVC5C5	01JRKPBWB2VAKMF5Q0V3KY8SJ5	7	4	410	6	2025-04-12 00:28:34.544729
01JRKPBWBH9G6JYYK7AT81H1S7	01JRKPBWB2VAKMF5Q0V3KY8SJ5	8	5	540	4	2025-04-12 00:28:34.545463
01JRKPBWBJDDTC0J1M9W3Q2DM5	01JRKPBWB2VAKMF5Q0V3KY8SJ5	9	4	390	18	2025-04-12 00:28:34.546206
\.


--
-- Data for Name: tee_boxes; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.tee_boxes (id, course_id, rating, slope, yardage, name, hex, created_on) FROM stdin;
01JRK6WHZZSEGA0Q9KG7KA6FRK	01JRK6SAZY9MAQ5V6CH8761FSJ	74.2	148	7181	Championship	\N	2025-04-11 19:58:03.77599
01JRK6X1Z8XHRWZXV4N1T5J7F0	01JRK6SAZY9MAQ5V6CH8761FSJ	74.2	148	7181	Championship	\N	2025-04-11 19:58:20.136629
01JRK6XDZNEAZBFY14RQHQH93C	01JRK6SAZY9MAQ5V6CH8761FSJ	74.2	148	7181	Championship	\N	2025-04-11 19:58:32.437311
01JRK6XE06QT8X3JAYWQ247VEE	01JRK6SAZY9MAQ5V6CH8761FSJ	71.8	138	6579	Regular	\N	2025-04-11 19:58:32.454284
01JRKPBWB2VAKMF5Q0V3KY8SJ5	01JRKPA0XK8024YBB1Y3Y1Y4VA	72	130	6500	Test Tees	\N	2025-04-12 00:28:34.530236
\.


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
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);


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
-- Name: tee_box_holes tee_box_holes_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_box_holes
    ADD CONSTRAINT tee_box_holes_pkey PRIMARY KEY (id);


--
-- Name: tee_boxes tee_boxes_pkey; Type: CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_boxes
    ADD CONSTRAINT tee_boxes_pkey PRIMARY KEY (id);


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
-- Name: rounds rounds_golfer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.rounds
    ADD CONSTRAINT rounds_golfer_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(id);


--
-- Name: tee_box_holes tee_box_holes_tee_box_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: golf_api
--

ALTER TABLE ONLY public.tee_box_holes
    ADD CONSTRAINT tee_box_holes_tee_box_id_fkey FOREIGN KEY (tee_box_id) REFERENCES public.tee_boxes(id);


--
-- PostgreSQL database dump complete
--

