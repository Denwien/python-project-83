--
-- PostgreSQL database dump
--

\restrict cfs0rY8yyBiPagW2dhm8n97sXlahuhayNDf1q25o9KFMocYTLncaN37PA3MmZZ7

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: urls; Type: TABLE; Schema: public; Owner: Besitzer
--

CREATE TABLE public.urls (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.urls OWNER TO "Besitzer";

--
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: Besitzer
--

CREATE SEQUENCE public.urls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.urls_id_seq OWNER TO "Besitzer";

--
-- Name: urls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Besitzer
--

ALTER SEQUENCE public.urls_id_seq OWNED BY public.urls.id;


--
-- Name: urls id; Type: DEFAULT; Schema: public; Owner: Besitzer
--

ALTER TABLE ONLY public.urls ALTER COLUMN id SET DEFAULT nextval('public.urls_id_seq'::regclass);


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: Besitzer
--

COPY public.urls (id, name, created_at) FROM stdin;
1	https://python-project-83-k4ol.onrender.com	2025-12-16 14:05:42.62821
\.


--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Besitzer
--

SELECT pg_catalog.setval('public.urls_id_seq', 1, true);


--
-- Name: urls urls_name_key; Type: CONSTRAINT; Schema: public; Owner: Besitzer
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_name_key UNIQUE (name);


--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: Besitzer
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict cfs0rY8yyBiPagW2dhm8n97sXlahuhayNDf1q25o9KFMocYTLncaN37PA3MmZZ7

