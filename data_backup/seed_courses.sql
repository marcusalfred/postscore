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
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: golf_api
--

COPY public.courses (id, name, address, city, state, zip, website, created_on, par) FROM stdin;
01JRK6SAZY9MAQ5V6CH8761FSJ	Pine Valley Golf Club	1234 Pine Valley Road	Pine Valley	NJ	08021	https://pinevalleygolfclub.com	2025-04-11 19:56:18.302216	\N
01JRKPA0XK8024YBB1Y3Y1Y4VA	Test Golf Club	123 Fairway Drive	Golf City	CA	12345	https://testgolfclub.com	2025-04-12 00:27:33.683307	\N
01JRNBZ4QJT57A2C92RXQPBJS8	Admin Course	123 Admin St	Admin City	CA	12345	https://admin-example.com	2025-04-12 16:05:20.24277	\N
013930306362343539363166633734373466646236613536333362643066623736	Test Course Via SQL	123 Golf Lane	Golfville	CA	12345	https://testcourse.com	2025-04-13 00:02:18.321611	\N
\.


--
-- PostgreSQL database dump complete
--

