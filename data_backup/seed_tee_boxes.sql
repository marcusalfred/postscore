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
-- PostgreSQL database dump complete
--

