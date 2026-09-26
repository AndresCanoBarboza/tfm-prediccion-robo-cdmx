--
-- PostgreSQL database dump
--

\restrict Pvn70b5tcteZ5NPRZuR6aFcZ1nbyr1mA1rPZNjPlQl7kbPhhv8htYQmKv0702fy

-- Dumped from database version 17.11 (8a81ecb)
-- Dumped by pg_dump version 18.6

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
-- Name: contexto_robo_alcaldia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contexto_robo_alcaldia (
    alcaldia text NOT NULL,
    anio smallint NOT NULL,
    robos_registrados bigint
);


--
-- Name: TABLE contexto_robo_alcaldia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.contexto_robo_alcaldia IS 'Carpetas de investigación por robo, por alcaldía y año (FGJ CDMX).';


--
-- Name: dataset_integrado; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dataset_integrado (
    id bigint NOT NULL,
    id_origen character varying(50),
    clase character varying(2) NOT NULL,
    sexo character(1),
    edad smallint,
    nivel_instruccion smallint,
    nivel_instruccion_etq character varying(50),
    ocupacion character varying(3),
    cve_ent_residencia smallint,
    cve_mun_residencia integer,
    es_cdmx boolean,
    anio smallint,
    familia_procesal character varying(2),
    estado_conyugal character varying(50),
    condicion_psicofisica character varying(50)
);


--
-- Name: TABLE dataset_integrado; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.dataset_integrado IS 'Dataset integrado y analítico (EHRIIJ + ENVIPE), 884,471 filas esperadas. Alcance NACIONAL.';


--
-- Name: dataset_integrado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dataset_integrado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dataset_integrado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dataset_integrado_id_seq OWNED BY public.dataset_integrado.id;


--
-- Name: dataset_modelo_balanceado; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dataset_modelo_balanceado (
    id bigint NOT NULL,
    id_origen character varying(50),
    clase character varying(2) NOT NULL,
    sexo character(1),
    edad smallint,
    nivel_instruccion smallint,
    nivel_instruccion_etq character varying(50),
    ocupacion character varying(3),
    cve_ent_residencia smallint,
    cve_mun_residencia integer,
    es_cdmx boolean,
    anio smallint,
    familia_procesal character varying(2),
    estado_conyugal character varying(50),
    condicion_psicofisica character varying(50)
);


--
-- Name: TABLE dataset_modelo_balanceado; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.dataset_modelo_balanceado IS 'Conjunto balanceado por submuestreo aleatorio (35%/65%), semilla=42, 163,203 filas esperadas.';


--
-- Name: dataset_modelo_balanceado_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dataset_modelo_balanceado_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dataset_modelo_balanceado_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dataset_modelo_balanceado_id_seq OWNED BY public.dataset_modelo_balanceado.id;


--
-- Name: envipe_demograficos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.envipe_demograficos (
    id_per character varying(24) NOT NULL,
    id_viv character varying(15),
    id_hog character varying(18),
    upm character varying(10),
    sexo smallint,
    edad smallint,
    nivel_instruccion smallint,
    grados_estudio smallint,
    cve_ent character varying(2),
    nom_ent character varying(250),
    cve_mun character varying(3),
    nom_mun character varying(250),
    condicion_actividad smallint,
    posicion_ocupacion smallint,
    factor_hogar integer,
    dominio character varying(1),
    anio smallint
);


--
-- Name: fgj_carpetas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fgj_carpetas (
    id bigint NOT NULL,
    anio_inicio smallint,
    mes_inicio character varying(20),
    fecha_inicio date,
    hora_inicio character varying(10),
    anio_hecho smallint,
    mes_hecho character varying(20),
    fecha_hecho date,
    hora_hecho character varying(10),
    delito character varying(255),
    categoria_delito character varying(255),
    competencia character varying(100),
    fiscalia character varying(255),
    agencia character varying(255),
    unidad_investigacion character varying(255),
    colonia_hecho character varying(255),
    colonia_catalogo character varying(255),
    alcaldia_hecho character varying(100),
    alcaldia_catalogo character varying(100),
    municipio_hecho character varying(100),
    latitud numeric(10,6),
    longitud numeric(10,6)
);


--
-- Name: TABLE fgj_carpetas; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.fgj_carpetas IS 'Carpetas de investigación CDMX (FGJ). Fuente para clasificar categoria_delito = robo y para contexto geográfico por alcaldía.';


--
-- Name: meta_bitacora_validacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meta_bitacora_validacion (
    fuente text,
    regla text,
    registros_eliminados bigint
);


--
-- Name: TABLE meta_bitacora_validacion; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.meta_bitacora_validacion IS 'Reglas de validación y registros descartados por cada una.';


--
-- Name: meta_completitud_por_fuente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meta_completitud_por_fuente (
    variable text NOT NULL,
    fuente text NOT NULL,
    presentes bigint,
    faltantes bigint,
    pct_faltante double precision
);


--
-- Name: TABLE meta_completitud_por_fuente; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.meta_completitud_por_fuente IS 'Completitud de cada variable del esquema común, por fuente.';


--
-- Name: meta_sesgo_territorial; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.meta_sesgo_territorial (
    cve_ent smallint NOT NULL,
    pct_antes_filtro double precision,
    pct_despues_filtro double precision,
    diferencia double precision
);


--
-- Name: TABLE meta_sesgo_territorial; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.meta_sesgo_territorial IS 'Composición territorial de la clase positiva antes y después del filtro.';


--
-- Name: sensibilidad_ablacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sensibilidad_ablacion (
    subconjunto_predictoras text,
    num_variables bigint,
    auc_roc double precision
);


--
-- Name: sensibilidad_geografia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sensibilidad_geografia (
    escenario text,
    num_variables bigint,
    auc_roc double precision
);


--
-- Name: x_entrenamiento; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.x_entrenamiento (
    edad double precision,
    nivel_instruccion smallint,
    sexo_m smallint,
    ocupacion_nea smallint,
    clase smallint
);


--
-- Name: TABLE x_entrenamiento; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.x_entrenamiento IS 'Partición de entrenamiento (80%). Edad estandarizada.';


--
-- Name: x_prueba; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.x_prueba (
    edad double precision,
    nivel_instruccion smallint,
    sexo_m smallint,
    ocupacion_nea smallint,
    clase smallint
);


--
-- Name: TABLE x_prueba; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.x_prueba IS 'Partición de prueba (20%). Edad escalada con el ajuste del entrenamiento.';


--
-- Name: x_variante_con_geografia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.x_variante_con_geografia (
    edad smallint NOT NULL,
    nivel_instruccion smallint NOT NULL,
    es_cdmx smallint NOT NULL,
    sexo_m smallint NOT NULL,
    ocupacion_nea smallint NOT NULL,
    cve_ent_residencia_02 smallint NOT NULL,
    cve_ent_residencia_03 smallint NOT NULL,
    cve_ent_residencia_04 smallint NOT NULL,
    cve_ent_residencia_05 smallint NOT NULL,
    cve_ent_residencia_06 smallint NOT NULL,
    cve_ent_residencia_07 smallint NOT NULL,
    cve_ent_residencia_08 smallint NOT NULL,
    cve_ent_residencia_09 smallint NOT NULL,
    cve_ent_residencia_10 smallint NOT NULL,
    cve_ent_residencia_11 smallint NOT NULL,
    cve_ent_residencia_12 smallint NOT NULL,
    cve_ent_residencia_13 smallint NOT NULL,
    cve_ent_residencia_14 smallint NOT NULL,
    cve_ent_residencia_15 smallint NOT NULL,
    cve_ent_residencia_16 smallint NOT NULL,
    cve_ent_residencia_17 smallint NOT NULL,
    cve_ent_residencia_18 smallint NOT NULL,
    cve_ent_residencia_19 smallint NOT NULL,
    cve_ent_residencia_20 smallint NOT NULL,
    cve_ent_residencia_21 smallint NOT NULL,
    cve_ent_residencia_22 smallint NOT NULL,
    cve_ent_residencia_23 smallint NOT NULL,
    cve_ent_residencia_24 smallint NOT NULL,
    cve_ent_residencia_25 smallint NOT NULL,
    cve_ent_residencia_26 smallint NOT NULL,
    cve_ent_residencia_27 smallint NOT NULL,
    cve_ent_residencia_28 smallint NOT NULL,
    cve_ent_residencia_29 smallint NOT NULL,
    cve_ent_residencia_30 smallint NOT NULL,
    cve_ent_residencia_31 smallint NOT NULL,
    cve_ent_residencia_32 smallint NOT NULL,
    clase smallint NOT NULL
);


--
-- Name: TABLE x_variante_con_geografia; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.x_variante_con_geografia IS 'Variante de diagnóstico con claves de entidad. Solo pruebas de sensibilidad.';


--
-- Name: dataset_integrado id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_integrado ALTER COLUMN id SET DEFAULT nextval('public.dataset_integrado_id_seq'::regclass);


--
-- Name: dataset_modelo_balanceado id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_modelo_balanceado ALTER COLUMN id SET DEFAULT nextval('public.dataset_modelo_balanceado_id_seq'::regclass);


--
-- Name: dataset_integrado dataset_integrado_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_integrado
    ADD CONSTRAINT dataset_integrado_pkey PRIMARY KEY (id);


--
-- Name: dataset_modelo_balanceado dataset_modelo_balanceado_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dataset_modelo_balanceado
    ADD CONSTRAINT dataset_modelo_balanceado_pkey PRIMARY KEY (id);


--
-- Name: envipe_demograficos envipe_demograficos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.envipe_demograficos
    ADD CONSTRAINT envipe_demograficos_pkey PRIMARY KEY (id_per);


--
-- Name: fgj_carpetas fgj_carpetas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fgj_carpetas
    ADD CONSTRAINT fgj_carpetas_pkey PRIMARY KEY (id);


--
-- Name: contexto_robo_alcaldia pk_contexto_robo_alcaldia; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contexto_robo_alcaldia
    ADD CONSTRAINT pk_contexto_robo_alcaldia PRIMARY KEY (alcaldia, anio);


--
-- Name: meta_completitud_por_fuente pk_meta_completitud; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meta_completitud_por_fuente
    ADD CONSTRAINT pk_meta_completitud PRIMARY KEY (variable, fuente);


--
-- Name: meta_sesgo_territorial pk_meta_sesgo_territorial; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.meta_sesgo_territorial
    ADD CONSTRAINT pk_meta_sesgo_territorial PRIMARY KEY (cve_ent);


--
-- Name: idx_balanceado_clase; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_balanceado_clase ON public.dataset_modelo_balanceado USING btree (clase);


--
-- Name: idx_dataset_clase; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dataset_clase ON public.dataset_integrado USING btree (clase);


--
-- Name: idx_dataset_cve_ent; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dataset_cve_ent ON public.dataset_integrado USING btree (cve_ent_residencia);


--
-- Name: idx_dataset_es_cdmx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_dataset_es_cdmx ON public.dataset_integrado USING btree (es_cdmx);


--
-- Name: idx_envipe_anio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_envipe_anio ON public.envipe_demograficos USING btree (anio);


--
-- Name: idx_envipe_cve_ent; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_envipe_cve_ent ON public.envipe_demograficos USING btree (cve_ent);


--
-- Name: idx_fgj_alcaldia; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fgj_alcaldia ON public.fgj_carpetas USING btree (alcaldia_hecho);


--
-- Name: idx_fgj_categoria_delito; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_fgj_categoria_delito ON public.fgj_carpetas USING btree (categoria_delito);


--
-- PostgreSQL database dump complete
--

\unrestrict Pvn70b5tcteZ5NPRZuR6aFcZ1nbyr1mA1rPZNjPlQl7kbPhhv8htYQmKv0702fy

