--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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

ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_user_permissions DROP CONSTRAINT IF EXISTS mi_admin_usuario_use_usuario_id_12b5103b_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_user_permissions DROP CONSTRAINT IF EXISTS mi_admin_usuario_use_permission_id_39bb7e2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario DROP CONSTRAINT IF EXISTS mi_admin_usuario_rol_id_1681c779_fk_mi_admin_rol_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_groups DROP CONSTRAINT IF EXISTS mi_admin_usuario_groups_group_id_c895e477_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_groups DROP CONSTRAINT IF EXISTS mi_admin_usuario_gro_usuario_id_248b6571_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_subcomponente DROP CONSTRAINT IF EXISTS mi_admin_subcomponen_trimestre_id_2e42685a_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_subcomponente DROP CONSTRAINT IF EXISTS mi_admin_subcomponen_tipo_componente_id_874e8340_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_subcomponente DROP CONSTRAINT IF EXISTS mi_admin_subcomponen_asignacion_id_bb1f5102_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_resumentrimestral DROP CONSTRAINT IF EXISTS mi_admin_resumentrim_trimestre_id_24010350_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_resumentrimestral DROP CONSTRAINT IF EXISTS mi_admin_resumentrim_estudiante_id_1479238b_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_resumentrimestral DROP CONSTRAINT IF EXISTS mi_admin_resumentrim_asignacion_id_d38bfd77_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_persona DROP CONSTRAINT IF EXISTS mi_admin_persona_usuario_id_e0c29bb2_fk_mi_admin_usuario_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_nota DROP CONSTRAINT IF EXISTS mi_admin_nota_evaluacion_id_87b47133_fk_mi_admin_evaluacion_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_nota DROP CONSTRAINT IF EXISTS mi_admin_nota_estudiante_id_7d9f3ddb_fk_mi_admin_estudiante_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_inscripcion DROP CONSTRAINT IF EXISTS mi_admin_inscripcion_estudiante_id_0c3438e2_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_inscripcion DROP CONSTRAINT IF EXISTS mi_admin_inscripcion_curso_id_8dee0232_fk_mi_admin_curso_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_evaluacion DROP CONSTRAINT IF EXISTS mi_admin_evaluacion_trimestre_id_37c50278_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_evaluacion DROP CONSTRAINT IF EXISTS mi_admin_evaluacion_subcomponente_id_4330b11d_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_evaluacion DROP CONSTRAINT IF EXISTS mi_admin_evaluacion_asignacion_id_8115ea3e_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_estudiante DROP CONSTRAINT IF EXISTS mi_admin_estudiante_persona_id_664a5bd4_fk_mi_admin_persona_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_estudiante DROP CONSTRAINT IF EXISTS mi_admin_estudiante_curso_actual_id_0970e4a9_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_docente DROP CONSTRAINT IF EXISTS mi_admin_docente_persona_id_25ebbc7f_fk_mi_admin_persona_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_desempenoestudiante DROP CONSTRAINT IF EXISTS mi_admin_desempenoes_trimestre_id_a3bf80ef_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_desempenoestudiante DROP CONSTRAINT IF EXISTS mi_admin_desempenoes_estudiante_id_b992a1c6_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_desempenoestudiante DROP CONSTRAINT IF EXISTS mi_admin_desempenoes_asignacion_id_db0a34b5_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asistencia DROP CONSTRAINT IF EXISTS mi_admin_asistencia_trimestre_id_686f5c8c_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asistencia DROP CONSTRAINT IF EXISTS mi_admin_asistencia_estudiante_id_ca4600ba_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asistencia DROP CONSTRAINT IF EXISTS mi_admin_asistencia_asignacion_id_3b5f93e8_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asignacion DROP CONSTRAINT IF EXISTS mi_admin_asignacion_materia_id_a290889c_fk_mi_admin_materia_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asignacion DROP CONSTRAINT IF EXISTS mi_admin_asignacion_docente_id_6eda5e97_fk_mi_admin_docente_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asignacion DROP CONSTRAINT IF EXISTS mi_admin_asignacion_curso_id_2af5c132_fk_mi_admin_curso_id;
ALTER TABLE IF EXISTS ONLY public.mi_admin_administrativo DROP CONSTRAINT IF EXISTS mi_admin_administrat_persona_id_71387532_fk_mi_admin_;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_mi_admin_usuario_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.mi_admin_usuario_username_0c408cb2_like;
DROP INDEX IF EXISTS public.mi_admin_usuario_user_permissions_usuario_id_12b5103b;
DROP INDEX IF EXISTS public.mi_admin_usuario_user_permissions_permission_id_39bb7e2c;
DROP INDEX IF EXISTS public.mi_admin_usuario_rol_id_1681c779;
DROP INDEX IF EXISTS public.mi_admin_usuario_groups_usuario_id_248b6571;
DROP INDEX IF EXISTS public.mi_admin_usuario_groups_group_id_c895e477;
DROP INDEX IF EXISTS public.mi_admin_usuario_email_0468591e_like;
DROP INDEX IF EXISTS public.mi_admin_tipocomponente_nombre_21256e36_like;
DROP INDEX IF EXISTS public.mi_admin_subcomponente_trimestre_id_2e42685a;
DROP INDEX IF EXISTS public.mi_admin_subcomponente_tipo_componente_id_874e8340;
DROP INDEX IF EXISTS public.mi_admin_subcomponente_asignacion_id_bb1f5102;
DROP INDEX IF EXISTS public.mi_admin_rol_nombre_f2fa2889_like;
DROP INDEX IF EXISTS public.mi_admin_resumentrimestral_trimestre_id_24010350;
DROP INDEX IF EXISTS public.mi_admin_resumentrimestral_estudiante_id_1479238b;
DROP INDEX IF EXISTS public.mi_admin_resumentrimestral_asignacion_id_d38bfd77;
DROP INDEX IF EXISTS public.mi_admin_persona_carnet_229b2620_like;
DROP INDEX IF EXISTS public.mi_admin_nota_evaluacion_id_87b47133;
DROP INDEX IF EXISTS public.mi_admin_nota_estudiante_id_7d9f3ddb;
DROP INDEX IF EXISTS public.mi_admin_materia_nombre_c1f9ebd1_like;
DROP INDEX IF EXISTS public.mi_admin_inscripcion_estudiante_id_0c3438e2;
DROP INDEX IF EXISTS public.mi_admin_inscripcion_curso_id_8dee0232;
DROP INDEX IF EXISTS public.mi_admin_evaluacion_trimestre_id_37c50278;
DROP INDEX IF EXISTS public.mi_admin_evaluacion_subcomponente_id_4330b11d;
DROP INDEX IF EXISTS public.mi_admin_evaluacion_asignacion_id_8115ea3e;
DROP INDEX IF EXISTS public.mi_admin_estudiante_curso_actual_id_0970e4a9;
DROP INDEX IF EXISTS public.mi_admin_estudiante_codigo_estudiante_fdd66482_like;
DROP INDEX IF EXISTS public.mi_admin_desempenoestudiante_trimestre_id_a3bf80ef;
DROP INDEX IF EXISTS public.mi_admin_desempenoestudiante_estudiante_id_b992a1c6;
DROP INDEX IF EXISTS public.mi_admin_desempenoestudiante_asignacion_id_db0a34b5;
DROP INDEX IF EXISTS public.mi_admin_asistencia_trimestre_id_686f5c8c;
DROP INDEX IF EXISTS public.mi_admin_asistencia_estudiante_id_ca4600ba;
DROP INDEX IF EXISTS public.mi_admin_asistencia_asignacion_id_3b5f93e8;
DROP INDEX IF EXISTS public.mi_admin_asignacion_materia_id_a290889c;
DROP INDEX IF EXISTS public.mi_admin_asignacion_docente_id_6eda5e97;
DROP INDEX IF EXISTS public.mi_admin_asignacion_curso_id_2af5c132;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.mi_admin_trimestre DROP CONSTRAINT IF EXISTS unique_trimestre_numero_gestion;
ALTER TABLE IF EXISTS ONLY public.mi_admin_trimestre DROP CONSTRAINT IF EXISTS unique_trimestre_nombre_gestion;
ALTER TABLE IF EXISTS ONLY public.mi_admin_resumentrimestral DROP CONSTRAINT IF EXISTS unique_resumen_trimestral;
ALTER TABLE IF EXISTS ONLY public.mi_admin_nota DROP CONSTRAINT IF EXISTS unique_nota;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asistencia DROP CONSTRAINT IF EXISTS unique_asistencia;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asignacion DROP CONSTRAINT IF EXISTS unique_asignacion;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario DROP CONSTRAINT IF EXISTS mi_admin_usuario_username_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_user_permissions DROP CONSTRAINT IF EXISTS mi_admin_usuario_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_user_permissions DROP CONSTRAINT IF EXISTS mi_admin_usuario_user_pe_usuario_id_permission_id_e260dcdb_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario DROP CONSTRAINT IF EXISTS mi_admin_usuario_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_groups DROP CONSTRAINT IF EXISTS mi_admin_usuario_groups_usuario_id_group_id_e6553ffa_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario_groups DROP CONSTRAINT IF EXISTS mi_admin_usuario_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_usuario DROP CONSTRAINT IF EXISTS mi_admin_usuario_email_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_trimestre DROP CONSTRAINT IF EXISTS mi_admin_trimestre_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_tipocomponente DROP CONSTRAINT IF EXISTS mi_admin_tipocomponente_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_tipocomponente DROP CONSTRAINT IF EXISTS mi_admin_tipocomponente_nombre_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_subcomponente DROP CONSTRAINT IF EXISTS mi_admin_subcomponente_tipo_componente_id_nombr_eed575bd_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_subcomponente DROP CONSTRAINT IF EXISTS mi_admin_subcomponente_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_rol DROP CONSTRAINT IF EXISTS mi_admin_rol_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_rol DROP CONSTRAINT IF EXISTS mi_admin_rol_nombre_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_resumentrimestral DROP CONSTRAINT IF EXISTS mi_admin_resumentrimestral_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_persona DROP CONSTRAINT IF EXISTS mi_admin_persona_usuario_id_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_persona DROP CONSTRAINT IF EXISTS mi_admin_persona_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_persona DROP CONSTRAINT IF EXISTS mi_admin_persona_carnet_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_nota DROP CONSTRAINT IF EXISTS mi_admin_nota_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_materia DROP CONSTRAINT IF EXISTS mi_admin_materia_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_materia DROP CONSTRAINT IF EXISTS mi_admin_materia_nombre_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_inscripcion DROP CONSTRAINT IF EXISTS mi_admin_inscripcion_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_inscripcion DROP CONSTRAINT IF EXISTS mi_admin_inscripcion_estudiante_id_anio_academico_424d4656_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_evaluacion DROP CONSTRAINT IF EXISTS mi_admin_evaluacion_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_evaluacion DROP CONSTRAINT IF EXISTS mi_admin_evaluacion_asignacion_id_trimestre__8454c4ea_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_estudiante DROP CONSTRAINT IF EXISTS mi_admin_estudiante_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_estudiante DROP CONSTRAINT IF EXISTS mi_admin_estudiante_persona_id_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_estudiante DROP CONSTRAINT IF EXISTS mi_admin_estudiante_codigo_estudiante_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_docente DROP CONSTRAINT IF EXISTS mi_admin_docente_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_docente DROP CONSTRAINT IF EXISTS mi_admin_docente_persona_id_key;
ALTER TABLE IF EXISTS ONLY public.mi_admin_desempenoestudiante DROP CONSTRAINT IF EXISTS mi_admin_desempenoestudiante_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_desempenoestudiante DROP CONSTRAINT IF EXISTS mi_admin_desempenoestudi_estudiante_id_asignacion_580ef4cf_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_curso DROP CONSTRAINT IF EXISTS mi_admin_curso_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_curso DROP CONSTRAINT IF EXISTS mi_admin_curso_niveles_grado_paralelo_493444e0_uniq;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asistencia DROP CONSTRAINT IF EXISTS mi_admin_asistencia_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_asignacion DROP CONSTRAINT IF EXISTS mi_admin_asignacion_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_administrativo DROP CONSTRAINT IF EXISTS mi_admin_administrativo_pkey;
ALTER TABLE IF EXISTS ONLY public.mi_admin_administrativo DROP CONSTRAINT IF EXISTS mi_admin_administrativo_persona_id_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.mi_admin_usuario_user_permissions;
DROP TABLE IF EXISTS public.mi_admin_usuario_groups;
DROP TABLE IF EXISTS public.mi_admin_usuario;
DROP TABLE IF EXISTS public.mi_admin_trimestre;
DROP TABLE IF EXISTS public.mi_admin_tipocomponente;
DROP TABLE IF EXISTS public.mi_admin_subcomponente;
DROP TABLE IF EXISTS public.mi_admin_rol;
DROP TABLE IF EXISTS public.mi_admin_resumentrimestral;
DROP TABLE IF EXISTS public.mi_admin_persona;
DROP TABLE IF EXISTS public.mi_admin_nota;
DROP TABLE IF EXISTS public.mi_admin_materia;
DROP TABLE IF EXISTS public.mi_admin_inscripcion;
DROP TABLE IF EXISTS public.mi_admin_evaluacion;
DROP TABLE IF EXISTS public.mi_admin_estudiante;
DROP TABLE IF EXISTS public.mi_admin_docente;
DROP TABLE IF EXISTS public.mi_admin_desempenoestudiante;
DROP TABLE IF EXISTS public.mi_admin_curso;
DROP TABLE IF EXISTS public.mi_admin_asistencia;
DROP TABLE IF EXISTS public.mi_admin_asignacion;
DROP TABLE IF EXISTS public.mi_admin_administrativo;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: mi_admin_administrativo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_administrativo (
    id bigint NOT NULL,
    cargo character varying(100) NOT NULL,
    persona_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_administrativo OWNER TO postgres;

--
-- Name: mi_admin_administrativo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_administrativo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_administrativo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_asignacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_asignacion (
    id bigint NOT NULL,
    anio_academico integer NOT NULL,
    curso_id bigint NOT NULL,
    docente_id bigint,
    materia_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_asignacion OWNER TO postgres;

--
-- Name: mi_admin_asignacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_asignacion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_asignacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_asistencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_asistencia (
    id bigint NOT NULL,
    fecha date NOT NULL,
    asistio boolean NOT NULL,
    justificacion text,
    asignacion_id bigint NOT NULL,
    estudiante_id bigint NOT NULL,
    trimestre_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_asistencia OWNER TO postgres;

--
-- Name: mi_admin_asistencia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_asistencia ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_asistencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_curso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_curso (
    id bigint NOT NULL,
    niveles character varying(20) NOT NULL,
    grado smallint NOT NULL,
    paralelo character varying(2) NOT NULL,
    CONSTRAINT mi_admin_curso_grado_check CHECK ((grado >= 0))
);


ALTER TABLE public.mi_admin_curso OWNER TO postgres;

--
-- Name: mi_admin_curso_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_curso ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_curso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_desempenoestudiante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_desempenoestudiante (
    id bigint NOT NULL,
    observacion_texto text,
    rango_cualitativo character varying(20),
    fecha_registro timestamp with time zone NOT NULL,
    asignacion_id bigint NOT NULL,
    estudiante_id bigint NOT NULL,
    trimestre_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_desempenoestudiante OWNER TO postgres;

--
-- Name: mi_admin_desempenoestudiante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_desempenoestudiante ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_desempenoestudiante_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_docente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_docente (
    id bigint NOT NULL,
    especialidad character varying(100),
    persona_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_docente OWNER TO postgres;

--
-- Name: mi_admin_docente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_docente ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_docente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_estudiante; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_estudiante (
    id bigint NOT NULL,
    codigo_estudiante character varying(20) NOT NULL,
    curso_actual_id bigint,
    persona_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_estudiante OWNER TO postgres;

--
-- Name: mi_admin_estudiante_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_estudiante ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_estudiante_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_evaluacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_evaluacion (
    id bigint NOT NULL,
    nombre character varying(255) NOT NULL,
    descripcion text,
    fecha_evaluacion date NOT NULL,
    ponderacion numeric(5,2) NOT NULL,
    asignacion_id bigint NOT NULL,
    subcomponente_id bigint NOT NULL,
    trimestre_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_evaluacion OWNER TO postgres;

--
-- Name: mi_admin_evaluacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_evaluacion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_evaluacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_inscripcion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_inscripcion (
    id bigint NOT NULL,
    anio_academico smallint NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    curso_id bigint NOT NULL,
    estudiante_id bigint NOT NULL,
    CONSTRAINT mi_admin_inscripcion_anio_academico_check CHECK ((anio_academico >= 0))
);


ALTER TABLE public.mi_admin_inscripcion OWNER TO postgres;

--
-- Name: mi_admin_inscripcion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_inscripcion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_inscripcion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_materia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_materia (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text
);


ALTER TABLE public.mi_admin_materia OWNER TO postgres;

--
-- Name: mi_admin_materia_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_materia ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_materia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_nota; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_nota (
    id bigint NOT NULL,
    nota_obtenida numeric(5,2),
    fecha_registro timestamp with time zone NOT NULL,
    estudiante_id bigint NOT NULL,
    evaluacion_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_nota OWNER TO postgres;

--
-- Name: mi_admin_nota_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_nota ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_nota_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_persona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_persona (
    id bigint NOT NULL,
    nombres character varying(150) NOT NULL,
    apellidos character varying(150) NOT NULL,
    carnet character varying(15) NOT NULL,
    fecha_nacimiento date,
    genero character varying(1),
    pais character varying(50),
    departamento character varying(50),
    provincia character varying(50),
    localidad character varying(100),
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    usuario_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_persona OWNER TO postgres;

--
-- Name: mi_admin_persona_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_persona ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_persona_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_resumentrimestral; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_resumentrimestral (
    id bigint NOT NULL,
    nota_saber numeric(5,2),
    nota_hacer numeric(5,2),
    nota_ser numeric(5,2),
    nota_decidir numeric(5,2),
    prom_gral numeric(5,2),
    autoeval numeric(5,2),
    rango character varying(50),
    situacion character varying(50),
    observaciones text,
    nota_final_trimestre numeric(5,2),
    fecha_generacion timestamp with time zone NOT NULL,
    asignacion_id bigint NOT NULL,
    estudiante_id bigint NOT NULL,
    trimestre_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_resumentrimestral OWNER TO postgres;

--
-- Name: mi_admin_resumentrimestral_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_resumentrimestral ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_resumentrimestral_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_rol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_rol (
    id bigint NOT NULL,
    nombre character varying(50) NOT NULL
);


ALTER TABLE public.mi_admin_rol OWNER TO postgres;

--
-- Name: mi_admin_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_rol ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_rol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_subcomponente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_subcomponente (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    porcentaje_maximo numeric(5,2) NOT NULL,
    ponderacion_evaluacion_unica numeric(5,2) NOT NULL,
    asignacion_id bigint NOT NULL,
    tipo_componente_id bigint NOT NULL,
    trimestre_id bigint NOT NULL
);


ALTER TABLE public.mi_admin_subcomponente OWNER TO postgres;

--
-- Name: mi_admin_subcomponente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_subcomponente ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_subcomponente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_tipocomponente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_tipocomponente (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    porcentaje_total_componente numeric(5,2) NOT NULL
);


ALTER TABLE public.mi_admin_tipocomponente OWNER TO postgres;

--
-- Name: mi_admin_tipocomponente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_tipocomponente ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_tipocomponente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_trimestre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_trimestre (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    gestion integer NOT NULL,
    numero smallint,
    CONSTRAINT mi_admin_trimestre_numero_check CHECK ((numero >= 0))
);


ALTER TABLE public.mi_admin_trimestre OWNER TO postgres;

--
-- Name: mi_admin_trimestre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_trimestre ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_trimestre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_usuario (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    rol_id bigint
);


ALTER TABLE public.mi_admin_usuario OWNER TO postgres;

--
-- Name: mi_admin_usuario_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_usuario_groups (
    id bigint NOT NULL,
    usuario_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.mi_admin_usuario_groups OWNER TO postgres;

--
-- Name: mi_admin_usuario_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_usuario_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_usuario_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_usuario ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mi_admin_usuario_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mi_admin_usuario_user_permissions (
    id bigint NOT NULL,
    usuario_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.mi_admin_usuario_user_permissions OWNER TO postgres;

--
-- Name: mi_admin_usuario_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mi_admin_usuario_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mi_admin_usuario_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Docente	6	add_docente
22	Can change Docente	6	change_docente
23	Can delete Docente	6	delete_docente
24	Can view Docente	6	view_docente
25	Can add Materia	7	add_materia
26	Can change Materia	7	change_materia
27	Can delete Materia	7	delete_materia
28	Can view Materia	7	view_materia
29	Can add Rol	8	add_rol
30	Can change Rol	8	change_rol
31	Can delete Rol	8	delete_rol
32	Can view Rol	8	view_rol
33	Can add Tipo de Componente	9	add_tipocomponente
34	Can change Tipo de Componente	9	change_tipocomponente
35	Can delete Tipo de Componente	9	delete_tipocomponente
36	Can view Tipo de Componente	9	view_tipocomponente
37	Can add Usuario	10	add_usuario
38	Can change Usuario	10	change_usuario
39	Can delete Usuario	10	delete_usuario
40	Can view Usuario	10	view_usuario
41	Can add Curso	11	add_curso
42	Can change Curso	11	change_curso
43	Can delete Curso	11	delete_curso
44	Can view Curso	11	view_curso
45	Can add Asignación	12	add_asignacion
46	Can change Asignación	12	change_asignacion
47	Can delete Asignación	12	delete_asignacion
48	Can view Asignación	12	view_asignacion
49	Can add Estudiante	13	add_estudiante
50	Can change Estudiante	13	change_estudiante
51	Can delete Estudiante	13	delete_estudiante
52	Can view Estudiante	13	view_estudiante
53	Can add Evaluación	14	add_evaluacion
54	Can change Evaluación	14	change_evaluacion
55	Can delete Evaluación	14	delete_evaluacion
56	Can view Evaluación	14	view_evaluacion
57	Can add Nota	15	add_nota
58	Can change Nota	15	change_nota
59	Can delete Nota	15	delete_nota
60	Can view Nota	15	view_nota
61	Can add Persona	16	add_persona
62	Can change Persona	16	change_persona
63	Can delete Persona	16	delete_persona
64	Can view Persona	16	view_persona
65	Can add Administrativo	17	add_administrativo
66	Can change Administrativo	17	change_administrativo
67	Can delete Administrativo	17	delete_administrativo
68	Can view Administrativo	17	view_administrativo
69	Can add Subcomponente	18	add_subcomponente
70	Can change Subcomponente	18	change_subcomponente
71	Can delete Subcomponente	18	delete_subcomponente
72	Can view Subcomponente	18	view_subcomponente
73	Can add Trimestre	19	add_trimestre
74	Can change Trimestre	19	change_trimestre
75	Can delete Trimestre	19	delete_trimestre
76	Can view Trimestre	19	view_trimestre
77	Can add Resumen Trimestral	20	add_resumentrimestral
78	Can change Resumen Trimestral	20	change_resumentrimestral
79	Can delete Resumen Trimestral	20	delete_resumentrimestral
80	Can view Resumen Trimestral	20	view_resumentrimestral
81	Can add Desempeño del Estudiante	21	add_desempenoestudiante
82	Can change Desempeño del Estudiante	21	change_desempenoestudiante
83	Can delete Desempeño del Estudiante	21	delete_desempenoestudiante
84	Can view Desempeño del Estudiante	21	view_desempenoestudiante
85	Can add Asistencia	22	add_asistencia
86	Can change Asistencia	22	change_asistencia
87	Can delete Asistencia	22	delete_asistencia
88	Can view Asistencia	22	view_asistencia
89	Can add Inscripción	23	add_inscripcion
90	Can change Inscripción	23	change_inscripcion
91	Can delete Inscripción	23	delete_inscripcion
92	Can view Inscripción	23	view_inscripcion
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-11-08 22:53:37.088687-04	1	administrativo	1	[{"added": {}}]	8	1
2	2025-11-08 22:53:43.21637-04	2	docente	1	[{"added": {}}]	8	1
3	2025-11-08 22:53:50.014479-04	3	estudiante	1	[{"added": {}}]	8	1
4	2025-11-08 22:54:17.798871-04	1	Freddy Calle (9909422)	1	[{"added": {}}]	16	1
5	2025-11-08 22:54:32.625951-04	1	admin	2	[{"changed": {"fields": ["Rol"]}}]	10	1
6	2025-11-08 23:35:11.281917-04	1	Ser	1	[{"added": {}}]	9	1
7	2025-11-08 23:35:25.27898-04	2	Saber	1	[{"added": {}}]	9	1
8	2025-11-08 23:35:36.1636-04	3	Hacer	1	[{"added": {}}]	9	1
9	2025-11-08 23:35:47.926812-04	4	Decidir	1	[{"added": {}}]	9	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	mi_admin	docente
7	mi_admin	materia
8	mi_admin	rol
9	mi_admin	tipocomponente
10	mi_admin	usuario
11	mi_admin	curso
12	mi_admin	asignacion
13	mi_admin	estudiante
14	mi_admin	evaluacion
15	mi_admin	nota
16	mi_admin	persona
17	mi_admin	administrativo
18	mi_admin	subcomponente
19	mi_admin	trimestre
20	mi_admin	resumentrimestral
21	mi_admin	desempenoestudiante
22	mi_admin	asistencia
23	mi_admin	inscripcion
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-11-08 22:52:20.703966-04
2	contenttypes	0002_remove_content_type_name	2025-11-08 22:52:20.716964-04
3	auth	0001_initial	2025-11-08 22:52:20.766971-04
4	auth	0002_alter_permission_name_max_length	2025-11-08 22:52:20.771964-04
5	auth	0003_alter_user_email_max_length	2025-11-08 22:52:20.77898-04
6	auth	0004_alter_user_username_opts	2025-11-08 22:52:20.783972-04
7	auth	0005_alter_user_last_login_null	2025-11-08 22:52:20.792514-04
8	auth	0006_require_contenttypes_0002	2025-11-08 22:52:20.795512-04
9	auth	0007_alter_validators_add_error_messages	2025-11-08 22:52:20.801503-04
10	auth	0008_alter_user_username_max_length	2025-11-08 22:52:20.806512-04
11	auth	0009_alter_user_last_name_max_length	2025-11-08 22:52:20.812508-04
12	auth	0010_alter_group_name_max_length	2025-11-08 22:52:20.916164-04
13	auth	0011_update_proxy_permissions	2025-11-08 22:52:20.921157-04
14	auth	0012_alter_user_first_name_max_length	2025-11-08 22:52:20.928157-04
15	mi_admin	0001_initial	2025-11-08 22:52:21.403783-04
16	admin	0001_initial	2025-11-08 22:52:21.449789-04
17	admin	0002_logentry_remove_auto_add	2025-11-08 22:52:21.461788-04
18	admin	0003_logentry_add_action_flag_choices	2025-11-08 22:52:21.469781-04
19	sessions	0001_initial	2025-11-08 22:52:21.4848-04
20	mi_admin	0002_alter_materia_options_remove_materia_area_and_more	2025-11-08 23:13:40.897486-04
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
m66ej5mypb9kza4j1kpq388mc3grdqu1	.eJxVjDsOwjAQBe_iGln-JLKXkp4zRJv94ABypDipEHeHSCmgfTPzXmbAbS3D1mQZJjZn483pdxuRHlJ3wHest9nSXNdlGu2u2IM2e51ZnpfD_Tso2MpeOxBMfa9j9JkosJcgCiGpdhE8sHKOX6ApEoDjgImg4y6qy0AOzfsD_l44fA:1vHvYL:tVSc0OXn2FNjgNK_JapALA3nDoge1mWqGyasVqE-s9A	2025-11-22 22:53:17.501458-04
xva11meucgr5in4rsv54brtqmb7db1y3	.eJxVjDsOwjAQBe_iGlm2499S0nMGa73r4ABypDipEHeHSCmgfTPzXiLhtta09bKkicVZGCNOv2NGepS2E75ju82S5rYuU5a7Ig_a5XXm8rwc7t9BxV6_NXodgld2MDxC9AU4EzCrnC0rTyHE4mgwEaKJVgM7H0GPThMxEhOK9wf-9DhP:1vHw3Q:e6J0Hgagln944Fz9i6dHDbOckDCj5xiRJVTD1RslkYA	2025-11-22 23:25:24.058132-04
\.


--
-- Data for Name: mi_admin_administrativo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_administrativo (id, cargo, persona_id) FROM stdin;
1	Superusuario	1
\.


--
-- Data for Name: mi_admin_asignacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_asignacion (id, anio_academico, curso_id, docente_id, materia_id) FROM stdin;
1	2025	1	1	1
\.


--
-- Data for Name: mi_admin_asistencia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_asistencia (id, fecha, asistio, justificacion, asignacion_id, estudiante_id, trimestre_id) FROM stdin;
1	2025-11-08	t	\N	1	7	1
2	2025-11-08	t	\N	1	14	1
3	2025-11-08	t	\N	1	5	1
4	2025-11-08	t	\N	1	17	1
5	2025-11-08	t	\N	1	2	1
6	2025-11-08	t	\N	1	13	1
7	2025-11-08	t	\N	1	8	1
8	2025-11-08	t	\N	1	10	1
9	2025-11-08	t	\N	1	19	1
10	2025-11-08	t	\N	1	16	1
11	2025-11-08	t	\N	1	4	1
12	2025-11-08	t	\N	1	12	1
13	2025-11-08	t	\N	1	6	1
14	2025-11-08	t	\N	1	9	1
15	2025-11-08	t	\N	1	18	1
16	2025-11-08	t	\N	1	20	1
17	2025-11-08	t	\N	1	11	1
18	2025-11-08	t	\N	1	1	1
19	2025-11-08	t	\N	1	3	1
20	2025-11-08	t	\N	1	15	1
\.


--
-- Data for Name: mi_admin_curso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_curso (id, niveles, grado, paralelo) FROM stdin;
1	PRIMARIA	1	A
\.


--
-- Data for Name: mi_admin_desempenoestudiante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_desempenoestudiante (id, observacion_texto, rango_cualitativo, fecha_registro, asignacion_id, estudiante_id, trimestre_id) FROM stdin;
\.


--
-- Data for Name: mi_admin_docente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_docente (id, especialidad, persona_id) FROM stdin;
1	ARTES PLASTICAS	22
\.


--
-- Data for Name: mi_admin_estudiante; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_estudiante (id, codigo_estudiante, curso_actual_id, persona_id) FROM stdin;
1	90121001	1	2
2	90121002	1	3
3	90121003	1	4
4	90121004	1	5
5	90121005	1	6
6	90121006	1	7
7	90121007	1	8
8	90121008	1	9
9	90121009	1	10
10	90121010	1	11
11	90121011	1	12
12	90121012	1	13
13	90121013	1	14
14	90121014	1	15
15	90121015	1	16
16	90121016	1	17
17	90121017	1	18
18	90121018	1	19
19	90121019	1	20
20	90121020	1	21
21	80731001	1	23
22	80731002	1	24
23	80731003	1	25
24	80731004	1	26
25	80731005	1	27
26	80731006	1	28
27	80731007	1	29
28	80731008	1	30
29	80731009	1	31
30	80731010	1	32
31	80731011	1	33
32	80731012	1	34
33	80731013	1	35
34	80731014	1	36
35	80731015	1	37
36	80731016	1	38
37	80731017	1	39
38	80731018	1	40
39	80731019	1	41
40	80731020	1	42
41	80731021	1	43
42	80731022	1	44
\.


--
-- Data for Name: mi_admin_evaluacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_evaluacion (id, nombre, descripcion, fecha_evaluacion, ponderacion, asignacion_id, subcomponente_id, trimestre_id) FROM stdin;
11	tarea 2	Evaluación de tarea 2 (Hacer)	2025-11-09	35.00	1	5	1
12	Parcial2	Evaluación de Parcial2 (Saber)	2025-11-09	35.00	1	6	1
3	Tarea	Evaluación de Tarea (Hacer)	2025-11-08	35.00	1	3	1
1	Parcial	Evaluación de Parcial (Saber)	2025-11-08	35.00	1	1	1
\.


--
-- Data for Name: mi_admin_inscripcion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_inscripcion (id, anio_academico, fecha_creacion, curso_id, estudiante_id) FROM stdin;
1	2025	2025-11-08 22:55:43.216679-04	1	1
2	2025	2025-11-08 22:55:43.933669-04	1	2
3	2025	2025-11-08 22:55:44.699328-04	1	3
4	2025	2025-11-08 22:55:45.462638-04	1	4
5	2025	2025-11-08 22:55:46.226398-04	1	5
6	2025	2025-11-08 22:55:46.97869-04	1	6
7	2025	2025-11-08 22:55:47.72143-04	1	7
8	2025	2025-11-08 22:55:48.475761-04	1	8
9	2025	2025-11-08 22:55:49.242572-04	1	9
10	2025	2025-11-08 22:55:49.991923-04	1	10
11	2025	2025-11-08 22:55:50.730676-04	1	11
12	2025	2025-11-08 22:55:51.474347-04	1	12
13	2025	2025-11-08 22:55:52.236381-04	1	13
14	2025	2025-11-08 22:55:53.01579-04	1	14
15	2025	2025-11-08 22:55:53.750141-04	1	15
16	2025	2025-11-08 22:55:54.49399-04	1	16
17	2025	2025-11-08 22:55:55.233264-04	1	17
18	2025	2025-11-08 22:55:55.960411-04	1	18
19	2025	2025-11-08 22:55:56.688829-04	1	19
20	2025	2025-11-08 22:55:57.438165-04	1	20
21	2025	2025-11-09 01:36:08.333253-04	1	21
22	2025	2025-11-09 01:36:08.976673-04	1	22
23	2025	2025-11-09 01:36:09.61962-04	1	23
24	2025	2025-11-09 01:36:10.292034-04	1	24
25	2025	2025-11-09 01:36:10.956929-04	1	25
26	2025	2025-11-09 01:36:11.603045-04	1	26
27	2025	2025-11-09 01:36:12.250055-04	1	27
28	2025	2025-11-09 01:36:12.889605-04	1	28
29	2025	2025-11-09 01:36:13.537582-04	1	29
30	2025	2025-11-09 01:36:14.184013-04	1	30
31	2025	2025-11-09 01:36:14.864134-04	1	31
32	2025	2025-11-09 01:36:15.509621-04	1	32
33	2025	2025-11-09 01:36:16.150583-04	1	33
34	2025	2025-11-09 01:36:16.812056-04	1	34
35	2025	2025-11-09 01:36:17.461073-04	1	35
36	2025	2025-11-09 01:36:18.096547-04	1	36
37	2025	2025-11-09 01:36:18.765545-04	1	37
38	2025	2025-11-09 01:36:19.43162-04	1	38
39	2025	2025-11-09 01:36:20.085626-04	1	39
40	2025	2025-11-09 01:36:20.733594-04	1	40
41	2025	2025-11-09 01:36:21.393092-04	1	41
42	2025	2025-11-09 01:36:22.022767-04	1	42
\.


--
-- Data for Name: mi_admin_materia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_materia (id, nombre, descripcion) FROM stdin;
1	Artes Plasticas	
\.


--
-- Data for Name: mi_admin_nota; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_nota (id, nota_obtenida, fecha_registro, estudiante_id, evaluacion_id) FROM stdin;
1	5.00	2025-11-08 23:38:12.877413-04	7	1
2	10.00	2025-11-08 23:38:17.55334-04	14	1
3	10.00	2025-11-08 23:38:20.13438-04	5	1
4	10.00	2025-11-08 23:38:23.214295-04	17	1
5	15.00	2025-11-08 23:38:26.586195-04	2	1
6	10.00	2025-11-09 16:41:56.516023-04	22	1
\.


--
-- Data for Name: mi_admin_persona; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_persona (id, nombres, apellidos, carnet, fecha_nacimiento, genero, pais, departamento, provincia, localidad, fecha_creacion, fecha_actualizacion, usuario_id) FROM stdin;
1	Freddy	Calle	9909422	1998-11-16	M	Bolivia	La Paz	Murrillo	la paz	2025-11-08 22:54:17.796866-04	2025-11-08 22:54:17.796866-04	1
2	Juan	Quispe Mamani	9876501	2008-03-15	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:43.213685-04	2025-11-08 22:55:43.213685-04	2
3	Maria	Flores Condori	9876502	2009-05-20	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:43.932668-04	2025-11-08 22:55:43.932668-04	3
4	Carlos	Rojas Garcia	9876503	2008-01-10	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:44.697337-04	2025-11-08 22:55:44.697337-04	4
5	Ana	Lopez Perez	9876504	2009-11-02	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:45.461644-04	2025-11-08 22:55:45.461644-04	5
6	Luis	Fernandez Gonzales	9876505	2008-07-19	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:46.225398-04	2025-11-08 22:55:46.225398-04	6
7	Sofia	Mamani Quispe	9876506	2009-02-28	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:46.977691-04	2025-11-08 22:55:46.977691-04	7
8	Diego	Condori Flores	9876507	2008-09-05	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:47.72043-04	2025-11-08 22:55:47.72043-04	8
9	Camila	Garcia Rojas	9876508	2009-04-12	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:48.473655-04	2025-11-08 22:55:48.473655-04	9
10	Javier	Perez Lopez	9876509	2008-12-01	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:49.241572-04	2025-11-08 22:55:49.241572-04	10
11	Valentina	Gonzales Fernandez	9876510	2009-06-30	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:49.990923-04	2025-11-08 22:55:49.990923-04	11
12	Miguel	Quispe Flores	9876511	2008-02-14	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:50.729665-04	2025-11-08 22:55:50.729665-04	12
13	Isabella	Mamani Condori	9876512	2009-08-22	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:51.473347-04	2025-11-08 22:55:51.473347-04	13
14	Jose	Flores Rojas	9876513	2008-05-03	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:52.235382-04	2025-11-08 22:55:52.235382-04	14
15	Gabriela	Condori Garcia	9876514	2009-10-17	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:53.012785-04	2025-11-08 22:55:53.012785-04	15
16	Andres	Rojas Perez	9876515	2008-04-09	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:53.74914-04	2025-11-08 22:55:53.74914-04	16
17	Lucia	Lopez Gonzales	9876516	2009-01-25	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:54.49299-04	2025-11-08 22:55:54.49299-04	17
18	David	Fernandez Quispe	9876517	2008-08-11	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:55.231274-04	2025-11-08 22:55:55.231274-04	18
19	Paula	Perez Mamani	9876518	2009-03-07	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:55.958411-04	2025-11-08 22:55:55.958411-04	19
20	Fernando	Gonzales Flores	9876519	2008-06-23	M	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:56.687821-04	2025-11-08 22:55:56.687821-04	20
21	Daniela	Quispe Condori	9876520	2009-12-14	F	Bolivia	La Paz	Murillo	San Pedro	2025-11-08 22:55:57.437165-04	2025-11-08 22:55:57.437165-04	21
22	Jorge	Yunque	9988745	2005-12-28	M	Bolivia	La Paz	Murrillo	Chasquipampa	2025-11-08 22:57:06.687572-04	2025-11-08 22:57:06.687572-04	22
23	Yerko Alejandro	Hilaya	12345601	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:08.331253-04	2025-11-09 01:36:08.331253-04	23
24	Cristhofer Robin	Alvarez Quispe	12345602	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:08.975673-04	2025-11-09 01:36:08.975673-04	24
25	Kael Sebastian	Ayllon Sailer	12345603	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:09.61862-04	2025-11-09 01:36:09.61862-04	25
26	Yoselin	Cabrera Apaza	12345604	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:10.291034-04	2025-11-09 01:36:10.291034-04	26
27	Fatima	Callejas Mariaca	12345605	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:10.955937-04	2025-11-09 01:36:10.955937-04	27
28	Ariari	Chavarro Tabares	12345606	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:11.602045-04	2025-11-09 01:36:11.602045-04	28
29	Jhonatan Yamil	Coque Machicado	12345607	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:12.249054-04	2025-11-09 01:36:12.249054-04	29
30	Hugo Wilfredo	Guzman Vaca	12345608	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:12.888609-04	2025-11-09 01:36:12.888609-04	30
31	Adgar Luis	Lujan Argote	12345609	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:13.536582-04	2025-11-09 01:36:13.536582-04	31
32	Maria Liz	Mamani Padilla	12345610	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:14.183013-04	2025-11-09 01:36:14.183013-04	32
33	Jhojan David	Marquez Cespedes	12345611	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:14.863125-04	2025-11-09 01:36:14.863125-04	33
34	Kiatto	Mendoza Arteaga	12345612	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:15.508622-04	2025-11-09 01:36:15.508622-04	34
35	Valeria	Miranda Sullca	12345613	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:16.149583-04	2025-11-09 01:36:16.149583-04	35
36	Carlos Dayron	Moya Escalante	12345614	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:16.811056-04	2025-11-09 01:36:16.811056-04	36
37	Elimey Jhanel	Perez Leon	12345615	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:17.460073-04	2025-11-09 01:36:17.460073-04	37
38	Julio Cesar	Quispe Mamani	12345616	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:18.095547-04	2025-11-09 01:36:18.095547-04	38
39	Antuan Yeron	Rodriguez Rodriguez	12345617	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:18.764552-04	2025-11-09 01:36:18.764552-04	39
40	Diego Jesus	Saavedra Ureña	12345618	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:19.430624-04	2025-11-09 01:36:19.430624-04	40
41	Deynor	Vega Zapata	12345619	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:20.084626-04	2025-11-09 01:36:20.084626-04	41
42	Adriana	Mamani Mamani	12345620	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:20.731588-04	2025-11-09 01:36:20.731588-04	42
43	David	Gonzales Cuellar	12345621	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:21.392092-04	2025-11-09 01:36:21.392092-04	43
44	Cecilia	Caspa Ramos	12345622	\N	\N	Bolivia	La Paz	Murillo	San Pedro	2025-11-09 01:36:22.020761-04	2025-11-09 01:36:22.020761-04	44
\.


--
-- Data for Name: mi_admin_resumentrimestral; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_resumentrimestral (id, nota_saber, nota_hacer, nota_ser, nota_decidir, prom_gral, autoeval, rango, situacion, observaciones, nota_final_trimestre, fecha_generacion, asignacion_id, estudiante_id, trimestre_id) FROM stdin;
7	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.289832-04	1	8	1
35	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.940678-04	1	32	1
8	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.299829-04	1	10	1
9	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.308189-04	1	19	1
10	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.316386-04	1	16	1
36	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.948677-04	1	33	1
11	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.325395-04	1	4	1
12	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.335904-04	1	12	1
13	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.34591-04	1	6	1
14	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.355903-04	1	9	1
37	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.957679-04	1	34	1
38	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.965678-04	1	35	1
15	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.364904-04	1	18	1
16	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.37391-04	1	20	1
39	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:38.010778-04	1	36	1
17	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.382907-04	1	11	1
18	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.39292-04	1	1	1
19	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.402427-04	1	3	1
40	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:38.021784-04	1	37	1
41	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:38.043777-04	1	38	1
20	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.413438-04	1	15	1
42	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:38.051777-04	1	39	1
22	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.746468-04	1	23	1
23	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.753467-04	1	24	1
24	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.761467-04	1	25	1
25	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.770312-04	1	42	1
26	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.778956-04	1	26	1
27	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.799548-04	1	27	1
28	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.840692-04	1	41	1
21	10.00	0.00	\N	10.00	\N	10.00	1	Reprobado	Hola	30.00	2025-11-09 01:43:37.736978-04	1	22	1
5	15.00	0.00	10.00	\N	\N	\N	2	Reprobado	\N	25.00	2025-11-08 23:33:09.272047-04	1	2	1
2	10.00	0.00	10.00	\N	\N	\N	3	Reprobado	\N	20.00	2025-11-08 23:33:09.242341-04	1	14	1
3	10.00	0.00	10.00	\N	\N	\N	3	Reprobado	\N	20.00	2025-11-08 23:33:09.251341-04	1	5	1
29	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.863956-04	1	28	1
4	10.00	0.00	10.00	\N	\N	\N	3	Reprobado	\N	20.00	2025-11-08 23:33:09.261043-04	1	17	1
1	5.00	0.00	10.00	\N	\N	\N	6	Reprobado	\N	15.00	2025-11-08 23:33:09.22172-04	1	7	1
30	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.872225-04	1	21	1
31	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.89274-04	1	29	1
32	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.907253-04	1	40	1
6	0.00	0.00	10.00	\N	\N	\N	7	Reprobado	\N	10.00	2025-11-08 23:33:09.281328-04	1	13	1
33	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.916065-04	1	30	1
34	0.00	0.00	\N	\N	\N	\N	22	Reprobado	\N	0.00	2025-11-09 01:43:37.931163-04	1	31	1
\.


--
-- Data for Name: mi_admin_rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_rol (id, nombre) FROM stdin;
1	administrativo
2	docente
3	estudiante
\.


--
-- Data for Name: mi_admin_subcomponente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_subcomponente (id, nombre, porcentaje_maximo, ponderacion_evaluacion_unica, asignacion_id, tipo_componente_id, trimestre_id) FROM stdin;
1	Parcial	100.00	35.00	1	2	1
3	Tarea	100.00	35.00	1	3	1
5	tarea 2	100.00	35.00	1	3	1
6	Parcial2	100.00	35.00	1	2	1
\.


--
-- Data for Name: mi_admin_tipocomponente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_tipocomponente (id, nombre, descripcion, porcentaje_total_componente) FROM stdin;
1	Ser		5.00
2	Saber		45.00
3	Hacer		40.00
4	Decidir		5.00
\.


--
-- Data for Name: mi_admin_trimestre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_trimestre (id, nombre, fecha_inicio, fecha_fin, gestion, numero) FROM stdin;
1	Tercer Trimestre	2025-09-01	2025-12-01	2025	3
\.


--
-- Data for Name: mi_admin_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_usuario (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, rol_id) FROM stdin;
23	pbkdf2_sha256$870000$lL4KZa4phn0PBV4tBkKZRS$QLpH1pd+K8i9lFRzdfEutNcg1TVOaJY6Md9j3zO+c2Q=	\N	f	80731001	Yerko Alejandro	Hilaya	f	t	2025-11-09 01:36:07.649336-04	yhilaya@colegio.com	3
24	pbkdf2_sha256$870000$zhHxLBs8S9N9Lk0KCFxXtR$nFGNhz2dHb9l6WuNmjM4nKMtn+cDk98tXFCxbzj6IrE=	\N	f	80731002	Cristhofer Robin	Alvarez Quispe	f	t	2025-11-09 01:36:08.336253-04	calvarez@colegio.com	3
25	pbkdf2_sha256$870000$FfOLxzTkmMFT7ySphqpkJM$DYgzrYadycVULBVNPPp7qufii01tfIX+EMPTRLO4n4c=	\N	f	80731003	Kael Sebastian	Ayllon Sailer	f	t	2025-11-09 01:36:08.978678-04	kayllon@colegio.com	3
2	pbkdf2_sha256$870000$Y34bsjVSUM1TsSFn9nxT1v$ODCJeEJQWUNap9NEGpvhR4W4ccyoY99BFVve9faO3O4=	\N	f	90121001	Juan	Quispe Mamani	f	t	2025-11-08 22:55:42.205236-04	jquispe@coleg.bolivia	3
3	pbkdf2_sha256$870000$tYCf5OjXseEqR0bXme7g91$z49slnXcCm9dwNYVNN82nqJUxkH69666xB1LsIp2GLg=	\N	f	90121002	Maria	Flores Condori	f	t	2025-11-08 22:55:43.219679-04	mflores@coleg.bolivia	3
4	pbkdf2_sha256$870000$5ca3xqJuPPPEnrShaovCvK$YDR2VmSjPqyyy7inrq0bI/niXrWlZzB8luUcRPPwo0Y=	\N	f	90121003	Carlos	Rojas Garcia	f	t	2025-11-08 22:55:43.935668-04	crojas@coleg.bolivia	3
5	pbkdf2_sha256$870000$G752UMF7cNfc01h8eQbE39$pbpjXyhA+YpYNHVHDHf6TKeF508xst7otwBbHHsPvqs=	\N	f	90121004	Ana	Lopez Perez	f	t	2025-11-08 22:55:44.701327-04	alopez@coleg.bolivia	3
6	pbkdf2_sha256$870000$xyNGcw5MlBrbHYXpBjc0aV$T7VpuZrY6Vm7jpyoCTRx8JYFEl/RR7jnHxQGmXNSvY8=	\N	f	90121005	Luis	Fernandez Gonzales	f	t	2025-11-08 22:55:45.464643-04	lfernandez@coleg.bolivia	3
7	pbkdf2_sha256$870000$hZfDSnBnCRWp6KFLP5Y60r$6FNLI9grILoWosjbFRx4QOwERQuWlL+AHsKcobMl8GA=	\N	f	90121006	Sofia	Mamani Quispe	f	t	2025-11-08 22:55:46.228398-04	smamani@coleg.bolivia	3
9	pbkdf2_sha256$870000$Jx1SW1mXudSOYl3sxifWIw$ndy/sV/CI9nYRjhmz32GBNzQBeaw9K43vagdR+AUldY=	\N	f	90121008	Camila	Garcia Rojas	f	t	2025-11-08 22:55:47.724434-04	cgarcia@coleg.bolivia	3
10	pbkdf2_sha256$870000$RGs4VRUPoJNWhLAlJLiu6c$cnIi7aPW12AGOTDmvY3he5eaBCIX4yimOECe7tTC3dQ=	\N	f	90121009	Javier	Perez Lopez	f	t	2025-11-08 22:55:48.478766-04	jperez@coleg.bolivia	3
11	pbkdf2_sha256$870000$lyxzrCgm0XwEQ74UgUNm9W$zKWs6MtqqFgAbsp1vn1Y7Ph8fgNONnIMiMYVteV6jGE=	\N	f	90121010	Valentina	Gonzales Fernandez	f	t	2025-11-08 22:55:49.244575-04	vgonzales@coleg.bolivia	3
12	pbkdf2_sha256$870000$Vxc4hop3KjX9tmavMIkRMf$GTSEHDxGs4c/h684CRE+dGlpbnAOzyLWez1fOS0XU2Q=	\N	f	90121011	Miguel	Quispe Flores	f	t	2025-11-08 22:55:49.993931-04	mquispe@coleg.bolivia	3
13	pbkdf2_sha256$870000$sBhvFMPAVW5jdzzsEMuCRu$GATzkEPsnhR+e/HXpO2NZ8WkyQNuQZ+0i+kyP77Args=	\N	f	90121012	Isabella	Mamani Condori	f	t	2025-11-08 22:55:50.733669-04	imamani@coleg.bolivia	3
14	pbkdf2_sha256$870000$PPPOHLebtG8mizPENaHwsb$olU3ub0M2TiaZB4satmufKg46iJL0yYXuVHX1+24zRQ=	\N	f	90121013	Jose	Flores Rojas	f	t	2025-11-08 22:55:51.476352-04	jflores@coleg.bolivia	3
15	pbkdf2_sha256$870000$l0lKbI5oIJ7St0tXtZR3hf$fBJurcVjnJGctYMwYU+LP+TMxaWDdHRDQ64qrF2/WA0=	\N	f	90121014	Gabriela	Condori Garcia	f	t	2025-11-08 22:55:52.238384-04	gcondori@coleg.bolivia	3
16	pbkdf2_sha256$870000$qTlvDO2dCAbAlY8FPHpJvt$nuZ6CHLNI/cWtZSNHHzpXtUTMf64o+wdARoOoTn6Wbg=	\N	f	90121015	Andres	Rojas Perez	f	t	2025-11-08 22:55:53.017785-04	arojas@coleg.bolivia	3
17	pbkdf2_sha256$870000$IulpDF1Cz4JrzMRpnbmaoS$W9b/AqCcuLusvjfqI0h4vK99YRB0hfhp5Vr9ztdrrqI=	\N	f	90121016	Lucia	Lopez Gonzales	f	t	2025-11-08 22:55:53.752145-04	llopez@coleg.bolivia	3
18	pbkdf2_sha256$870000$B7Vyfn1QTUMHTyXOpsHktv$gnZiZtElDkpMB5Qj6sVLJm1qMmLJP6tnG/tcT+yXgWQ=	\N	f	90121017	David	Fernandez Quispe	f	t	2025-11-08 22:55:54.495992-04	dfernandez@coleg.bolivia	3
19	pbkdf2_sha256$870000$lO6LTSebEsdOw3HAnRCTTM$uGILP5+c5FHHvAah3ty1NVk6W4BF+gtFmovbjj0yasg=	\N	f	90121018	Paula	Perez Mamani	f	t	2025-11-08 22:55:55.235262-04	pperez@coleg.bolivia	3
20	pbkdf2_sha256$870000$3ESnaCuLF2O78GE53422Qv$rYMPcsTwlhe1Lh+OeJ32j+y5fSTaclDBzFkjHM92N+o=	\N	f	90121019	Fernando	Gonzales Flores	f	t	2025-11-08 22:55:55.962411-04	fgonzales@coleg.bolivia	3
21	pbkdf2_sha256$870000$z4D1uTjqYfAjmjsBahrJCP$Y3bFCyGZkgRiezC4NBNqKyhysJj7fkxpUOqW0nsDQ4U=	\N	f	90121020	Daniela	Quispe Condori	f	t	2025-11-08 22:55:56.690821-04	dquispe@coleg.bolivia	3
26	pbkdf2_sha256$870000$VuTOt47YH4dsfUxv8nBshy$HSquJapGIRvkEhhmKREwXvmaI3oBBcczbc56NvmfODQ=	\N	f	80731004	Yoselin	Cabrera Apaza	f	t	2025-11-09 01:36:09.621627-04	ycabrera@colegio.com	3
27	pbkdf2_sha256$870000$yEqIVLoLEAan6rQ0o6H9op$pDdsEodiRdUQIPD1Uxy+ZXEhhoJHRSnSz0EfuQuA7SE=	\N	f	80731005	Fatima	Callejas Mariaca	f	t	2025-11-09 01:36:10.293034-04	fcallejas@colegio.com	3
28	pbkdf2_sha256$870000$bMLMTswdQ7UUt3E44IQn65$Ihf1jnWSXcAQ/FOWapD4jfYd1UHn0EIeY2CSNET09HU=	\N	f	80731006	Ariari	Chavarro Tabares	f	t	2025-11-09 01:36:10.959926-04	achavarro@colegio.com	3
29	pbkdf2_sha256$870000$mOBFr54FNC2WpPeqQTXzzz$EqJTG9Sjg1oWu0gxmfu3bf+1KhJ6ysURDSfHDutUfdw=	\N	f	80731007	Jhonatan Yamil	Coque Machicado	f	t	2025-11-09 01:36:11.605051-04	jcoque@colegio.com	3
30	pbkdf2_sha256$870000$2flFcGMsKgVRwW4VHDQp0J$x+4/c1dAA+NPm5an5N0b1QlWf9fVsU+AOm9qutFUHZ0=	\N	f	80731008	Hugo Wilfredo	Guzman Vaca	f	t	2025-11-09 01:36:12.252054-04	hguzman@colegio.com	3
31	pbkdf2_sha256$870000$DiGryd00Wrq2jsx0djdqBZ$8bTLxjcFLS4CbhnFO8Bn/6Zgu+mOoApWJTxQ/6o9vLA=	\N	f	80731009	Adgar Luis	Lujan Argote	f	t	2025-11-09 01:36:12.891605-04	alujan@colegio.com	3
32	pbkdf2_sha256$870000$0TJ7cNTUTrph1KS2hI6BJL$jFLKXlFD6U5wV3w9fy/jmGofW7desT8ujKzQFyvhB3Q=	\N	f	80731010	Maria Liz	Mamani Padilla	f	t	2025-11-09 01:36:13.540588-04	mmamani@colegio.com	3
33	pbkdf2_sha256$870000$PXiQagCk6K8FSS0qGvwALG$Q9D4sU2pO1XLNAJKMbVwLGWRTHYs6wqmquj9kyKDIT4=	\N	f	80731011	Jhojan David	Marquez Cespedes	f	t	2025-11-09 01:36:14.186013-04	jmarquez@colegio.com	3
1	pbkdf2_sha256$870000$Xg3ZFTpm74XqGmw9QPv5xp$7Xss0EYnGKT1yi5MKdHX+tMiZLe6nxLfiIdiBkB922U=	2025-11-08 22:53:17-04	t	admin			t	t	2025-11-08 22:52:58-04	admin@gmail.com	1
22	pbkdf2_sha256$870000$qW72ugHZiJclSe3Hkavycb$wNOBaRLrLjfwvntb4RJR6Dhvbpcg48Fa4xW86EqyUew=	2025-11-08 23:25:24.056129-04	f	JORGE233	Jorge	Yunque	f	t	2025-11-08 22:57:05.8123-04	JORGE@GMAIL.COM	2
8	pbkdf2_sha256$870000$uHYw5cBpSqM9nMuEQTWWqY$S7EwM146DXs2UgGE3MwdMYS50riz5uRU/5ziO/NsMfk=	2025-11-09 01:30:02.812611-04	f	90121007	Diego	Condori Flores	f	t	2025-11-08 22:55:46.981698-04	dcondori@coleg.bolivia	3
34	pbkdf2_sha256$870000$VriNUwkvD72WxAFRluS9gM$qOZcDCbtxY49oYWki/O4ptooT0sYtCjnuWE14fRDhmI=	\N	f	80731012	Kiatto	Mendoza Arteaga	f	t	2025-11-09 01:36:14.86713-04	kmendoza@colegio.com	3
35	pbkdf2_sha256$870000$3Y5eA2DZKq9SdR0YmD4BqV$rC0oObt1xUIqNmLENWb4+NLlhk+VcOJmr5uZxc1fNt0=	\N	f	80731013	Valeria	Miranda Sullca	f	t	2025-11-09 01:36:15.510621-04	vmiranda@colegio.com	3
36	pbkdf2_sha256$870000$2FJiD1ZP9fViqVS0aw0eWv$XmUyXP/Y5/50PWiPw7ASghEIuEFCa8aNvp9erI5hSpg=	\N	f	80731014	Carlos Dayron	Moya Escalante	f	t	2025-11-09 01:36:16.152583-04	cmoya@colegio.com	3
37	pbkdf2_sha256$870000$fqKie9P1ufdnk7eNasHpxC$F8ec2d6zUFWE7OK+bicCAgwQSq8TRTApIG4XshC6Qjc=	\N	f	80731015	Elimey Jhanel	Perez Leon	f	t	2025-11-09 01:36:16.813056-04	eperez@colegio.com	3
38	pbkdf2_sha256$870000$sABI13gKgCJ5D2CLdyUkQu$2X0u3hMK1QCohRVyBVhnxLUD9jYcR6pBji00Vnqx9vs=	\N	f	80731016	Julio Cesar	Quispe Mamani	f	t	2025-11-09 01:36:17.463078-04	jquispe@colegio.com	3
39	pbkdf2_sha256$870000$BvDtYsQ7Xv5t6xJGPrSxJv$0/jnCWGJCQv7CwQ6aDBOpfL2qRPrpTC7LE+4cxrO6O8=	\N	f	80731017	Antuan Yeron	Rodriguez Rodriguez	f	t	2025-11-09 01:36:18.098547-04	arodriguez@colegio.com	3
40	pbkdf2_sha256$870000$Jh7Fok5Va1wi7WF5p17kK7$qpkThz4WDus25GErpbKXamfX6255rcB9r0ZE+epGwkg=	\N	f	80731018	Diego Jesus	Saavedra Ureña	f	t	2025-11-09 01:36:18.767544-04	dsaavedra@colegio.com	3
41	pbkdf2_sha256$870000$ScwBfbUtTi8eFW7EPeMSRW$LNgBbPC7YMenArGdFhwui7wWrMGlsf3/MqgidzfbtZo=	\N	f	80731019	Deynor	Vega Zapata	f	t	2025-11-09 01:36:19.43462-04	dvega@colegio.com	3
42	pbkdf2_sha256$870000$9HxpavcPJFYq8HlhDuqWZk$2FIhwT7fgGnLdGHbOAeUnB9c7O31ZEd2HpcPcPqX0Yo=	\N	f	80731020	Adriana	Mamani Mamani	f	t	2025-11-09 01:36:20.089632-04	amamani@colegio.com	3
43	pbkdf2_sha256$870000$DBb5955vhyncD0opsz1WkM$CHvODnZ+c7RYn6L0utEY7hNyh53gJgJlABKekdD87R4=	\N	f	80731021	David	Gonzales Cuellar	f	t	2025-11-09 01:36:20.735588-04	dgonzales@colegio.com	3
44	pbkdf2_sha256$870000$bGseDcfy3BjgH23Ev86ore$CM5KKAcRy9LUefe5wO6GukVzZbUxOGVzh6vKp/lb+SY=	\N	f	80731022	Cecilia	Caspa Ramos	f	t	2025-11-09 01:36:21.394092-04	ccaspa@colegio.com	3
\.


--
-- Data for Name: mi_admin_usuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_usuario_groups (id, usuario_id, group_id) FROM stdin;
\.


--
-- Data for Name: mi_admin_usuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mi_admin_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 92, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 9, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 23, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: mi_admin_administrativo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_administrativo_id_seq', 1, true);


--
-- Name: mi_admin_asignacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_asignacion_id_seq', 1, true);


--
-- Name: mi_admin_asistencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_asistencia_id_seq', 20, true);


--
-- Name: mi_admin_curso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_curso_id_seq', 1, true);


--
-- Name: mi_admin_desempenoestudiante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_desempenoestudiante_id_seq', 1, false);


--
-- Name: mi_admin_docente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_docente_id_seq', 1, true);


--
-- Name: mi_admin_estudiante_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_estudiante_id_seq', 42, true);


--
-- Name: mi_admin_evaluacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_evaluacion_id_seq', 12, true);


--
-- Name: mi_admin_inscripcion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_inscripcion_id_seq', 42, true);


--
-- Name: mi_admin_materia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_materia_id_seq', 1, true);


--
-- Name: mi_admin_nota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_nota_id_seq', 6, true);


--
-- Name: mi_admin_persona_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_persona_id_seq', 44, true);


--
-- Name: mi_admin_resumentrimestral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_resumentrimestral_id_seq', 42, true);


--
-- Name: mi_admin_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_rol_id_seq', 3, true);


--
-- Name: mi_admin_subcomponente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_subcomponente_id_seq', 6, true);


--
-- Name: mi_admin_tipocomponente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_tipocomponente_id_seq', 4, true);


--
-- Name: mi_admin_trimestre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_trimestre_id_seq', 1, true);


--
-- Name: mi_admin_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_usuario_groups_id_seq', 1, false);


--
-- Name: mi_admin_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_usuario_id_seq', 44, true);


--
-- Name: mi_admin_usuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mi_admin_usuario_user_permissions_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: mi_admin_administrativo mi_admin_administrativo_persona_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_administrativo
    ADD CONSTRAINT mi_admin_administrativo_persona_id_key UNIQUE (persona_id);


--
-- Name: mi_admin_administrativo mi_admin_administrativo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_administrativo
    ADD CONSTRAINT mi_admin_administrativo_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_asignacion mi_admin_asignacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asignacion
    ADD CONSTRAINT mi_admin_asignacion_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_asistencia mi_admin_asistencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asistencia
    ADD CONSTRAINT mi_admin_asistencia_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_curso mi_admin_curso_niveles_grado_paralelo_493444e0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_curso
    ADD CONSTRAINT mi_admin_curso_niveles_grado_paralelo_493444e0_uniq UNIQUE (niveles, grado, paralelo);


--
-- Name: mi_admin_curso mi_admin_curso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_curso
    ADD CONSTRAINT mi_admin_curso_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_desempenoestudiante mi_admin_desempenoestudi_estudiante_id_asignacion_580ef4cf_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_desempenoestudiante
    ADD CONSTRAINT mi_admin_desempenoestudi_estudiante_id_asignacion_580ef4cf_uniq UNIQUE (estudiante_id, asignacion_id, trimestre_id);


--
-- Name: mi_admin_desempenoestudiante mi_admin_desempenoestudiante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_desempenoestudiante
    ADD CONSTRAINT mi_admin_desempenoestudiante_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_docente mi_admin_docente_persona_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_docente
    ADD CONSTRAINT mi_admin_docente_persona_id_key UNIQUE (persona_id);


--
-- Name: mi_admin_docente mi_admin_docente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_docente
    ADD CONSTRAINT mi_admin_docente_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_estudiante mi_admin_estudiante_codigo_estudiante_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_estudiante
    ADD CONSTRAINT mi_admin_estudiante_codigo_estudiante_key UNIQUE (codigo_estudiante);


--
-- Name: mi_admin_estudiante mi_admin_estudiante_persona_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_estudiante
    ADD CONSTRAINT mi_admin_estudiante_persona_id_key UNIQUE (persona_id);


--
-- Name: mi_admin_estudiante mi_admin_estudiante_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_estudiante
    ADD CONSTRAINT mi_admin_estudiante_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_evaluacion mi_admin_evaluacion_asignacion_id_trimestre__8454c4ea_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_evaluacion
    ADD CONSTRAINT mi_admin_evaluacion_asignacion_id_trimestre__8454c4ea_uniq UNIQUE (asignacion_id, trimestre_id, nombre, subcomponente_id);


--
-- Name: mi_admin_evaluacion mi_admin_evaluacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_evaluacion
    ADD CONSTRAINT mi_admin_evaluacion_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_inscripcion mi_admin_inscripcion_estudiante_id_anio_academico_424d4656_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_inscripcion
    ADD CONSTRAINT mi_admin_inscripcion_estudiante_id_anio_academico_424d4656_uniq UNIQUE (estudiante_id, anio_academico);


--
-- Name: mi_admin_inscripcion mi_admin_inscripcion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_inscripcion
    ADD CONSTRAINT mi_admin_inscripcion_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_materia mi_admin_materia_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_materia
    ADD CONSTRAINT mi_admin_materia_nombre_key UNIQUE (nombre);


--
-- Name: mi_admin_materia mi_admin_materia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_materia
    ADD CONSTRAINT mi_admin_materia_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_nota mi_admin_nota_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_nota
    ADD CONSTRAINT mi_admin_nota_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_persona mi_admin_persona_carnet_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_persona
    ADD CONSTRAINT mi_admin_persona_carnet_key UNIQUE (carnet);


--
-- Name: mi_admin_persona mi_admin_persona_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_persona
    ADD CONSTRAINT mi_admin_persona_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_persona mi_admin_persona_usuario_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_persona
    ADD CONSTRAINT mi_admin_persona_usuario_id_key UNIQUE (usuario_id);


--
-- Name: mi_admin_resumentrimestral mi_admin_resumentrimestral_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_resumentrimestral
    ADD CONSTRAINT mi_admin_resumentrimestral_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_rol mi_admin_rol_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_rol
    ADD CONSTRAINT mi_admin_rol_nombre_key UNIQUE (nombre);


--
-- Name: mi_admin_rol mi_admin_rol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_rol
    ADD CONSTRAINT mi_admin_rol_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_subcomponente mi_admin_subcomponente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_subcomponente
    ADD CONSTRAINT mi_admin_subcomponente_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_subcomponente mi_admin_subcomponente_tipo_componente_id_nombr_eed575bd_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_subcomponente
    ADD CONSTRAINT mi_admin_subcomponente_tipo_componente_id_nombr_eed575bd_uniq UNIQUE (tipo_componente_id, nombre, asignacion_id, trimestre_id);


--
-- Name: mi_admin_tipocomponente mi_admin_tipocomponente_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_tipocomponente
    ADD CONSTRAINT mi_admin_tipocomponente_nombre_key UNIQUE (nombre);


--
-- Name: mi_admin_tipocomponente mi_admin_tipocomponente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_tipocomponente
    ADD CONSTRAINT mi_admin_tipocomponente_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_trimestre mi_admin_trimestre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_trimestre
    ADD CONSTRAINT mi_admin_trimestre_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_usuario mi_admin_usuario_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario
    ADD CONSTRAINT mi_admin_usuario_email_key UNIQUE (email);


--
-- Name: mi_admin_usuario_groups mi_admin_usuario_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_groups
    ADD CONSTRAINT mi_admin_usuario_groups_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_usuario_groups mi_admin_usuario_groups_usuario_id_group_id_e6553ffa_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_groups
    ADD CONSTRAINT mi_admin_usuario_groups_usuario_id_group_id_e6553ffa_uniq UNIQUE (usuario_id, group_id);


--
-- Name: mi_admin_usuario mi_admin_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario
    ADD CONSTRAINT mi_admin_usuario_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_usuario_user_permissions mi_admin_usuario_user_pe_usuario_id_permission_id_e260dcdb_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_user_permissions
    ADD CONSTRAINT mi_admin_usuario_user_pe_usuario_id_permission_id_e260dcdb_uniq UNIQUE (usuario_id, permission_id);


--
-- Name: mi_admin_usuario_user_permissions mi_admin_usuario_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_user_permissions
    ADD CONSTRAINT mi_admin_usuario_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: mi_admin_usuario mi_admin_usuario_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario
    ADD CONSTRAINT mi_admin_usuario_username_key UNIQUE (username);


--
-- Name: mi_admin_asignacion unique_asignacion; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asignacion
    ADD CONSTRAINT unique_asignacion UNIQUE (curso_id, materia_id, anio_academico);


--
-- Name: mi_admin_asistencia unique_asistencia; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asistencia
    ADD CONSTRAINT unique_asistencia UNIQUE (estudiante_id, asignacion_id, trimestre_id, fecha);


--
-- Name: mi_admin_nota unique_nota; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_nota
    ADD CONSTRAINT unique_nota UNIQUE (estudiante_id, evaluacion_id);


--
-- Name: mi_admin_resumentrimestral unique_resumen_trimestral; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_resumentrimestral
    ADD CONSTRAINT unique_resumen_trimestral UNIQUE (estudiante_id, asignacion_id, trimestre_id);


--
-- Name: mi_admin_trimestre unique_trimestre_nombre_gestion; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_trimestre
    ADD CONSTRAINT unique_trimestre_nombre_gestion UNIQUE (nombre, gestion);


--
-- Name: mi_admin_trimestre unique_trimestre_numero_gestion; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_trimestre
    ADD CONSTRAINT unique_trimestre_numero_gestion UNIQUE (numero, gestion);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: mi_admin_asignacion_curso_id_2af5c132; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asignacion_curso_id_2af5c132 ON public.mi_admin_asignacion USING btree (curso_id);


--
-- Name: mi_admin_asignacion_docente_id_6eda5e97; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asignacion_docente_id_6eda5e97 ON public.mi_admin_asignacion USING btree (docente_id);


--
-- Name: mi_admin_asignacion_materia_id_a290889c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asignacion_materia_id_a290889c ON public.mi_admin_asignacion USING btree (materia_id);


--
-- Name: mi_admin_asistencia_asignacion_id_3b5f93e8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asistencia_asignacion_id_3b5f93e8 ON public.mi_admin_asistencia USING btree (asignacion_id);


--
-- Name: mi_admin_asistencia_estudiante_id_ca4600ba; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asistencia_estudiante_id_ca4600ba ON public.mi_admin_asistencia USING btree (estudiante_id);


--
-- Name: mi_admin_asistencia_trimestre_id_686f5c8c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_asistencia_trimestre_id_686f5c8c ON public.mi_admin_asistencia USING btree (trimestre_id);


--
-- Name: mi_admin_desempenoestudiante_asignacion_id_db0a34b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_desempenoestudiante_asignacion_id_db0a34b5 ON public.mi_admin_desempenoestudiante USING btree (asignacion_id);


--
-- Name: mi_admin_desempenoestudiante_estudiante_id_b992a1c6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_desempenoestudiante_estudiante_id_b992a1c6 ON public.mi_admin_desempenoestudiante USING btree (estudiante_id);


--
-- Name: mi_admin_desempenoestudiante_trimestre_id_a3bf80ef; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_desempenoestudiante_trimestre_id_a3bf80ef ON public.mi_admin_desempenoestudiante USING btree (trimestre_id);


--
-- Name: mi_admin_estudiante_codigo_estudiante_fdd66482_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_estudiante_codigo_estudiante_fdd66482_like ON public.mi_admin_estudiante USING btree (codigo_estudiante varchar_pattern_ops);


--
-- Name: mi_admin_estudiante_curso_actual_id_0970e4a9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_estudiante_curso_actual_id_0970e4a9 ON public.mi_admin_estudiante USING btree (curso_actual_id);


--
-- Name: mi_admin_evaluacion_asignacion_id_8115ea3e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_evaluacion_asignacion_id_8115ea3e ON public.mi_admin_evaluacion USING btree (asignacion_id);


--
-- Name: mi_admin_evaluacion_subcomponente_id_4330b11d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_evaluacion_subcomponente_id_4330b11d ON public.mi_admin_evaluacion USING btree (subcomponente_id);


--
-- Name: mi_admin_evaluacion_trimestre_id_37c50278; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_evaluacion_trimestre_id_37c50278 ON public.mi_admin_evaluacion USING btree (trimestre_id);


--
-- Name: mi_admin_inscripcion_curso_id_8dee0232; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_inscripcion_curso_id_8dee0232 ON public.mi_admin_inscripcion USING btree (curso_id);


--
-- Name: mi_admin_inscripcion_estudiante_id_0c3438e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_inscripcion_estudiante_id_0c3438e2 ON public.mi_admin_inscripcion USING btree (estudiante_id);


--
-- Name: mi_admin_materia_nombre_c1f9ebd1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_materia_nombre_c1f9ebd1_like ON public.mi_admin_materia USING btree (nombre varchar_pattern_ops);


--
-- Name: mi_admin_nota_estudiante_id_7d9f3ddb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_nota_estudiante_id_7d9f3ddb ON public.mi_admin_nota USING btree (estudiante_id);


--
-- Name: mi_admin_nota_evaluacion_id_87b47133; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_nota_evaluacion_id_87b47133 ON public.mi_admin_nota USING btree (evaluacion_id);


--
-- Name: mi_admin_persona_carnet_229b2620_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_persona_carnet_229b2620_like ON public.mi_admin_persona USING btree (carnet varchar_pattern_ops);


--
-- Name: mi_admin_resumentrimestral_asignacion_id_d38bfd77; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_resumentrimestral_asignacion_id_d38bfd77 ON public.mi_admin_resumentrimestral USING btree (asignacion_id);


--
-- Name: mi_admin_resumentrimestral_estudiante_id_1479238b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_resumentrimestral_estudiante_id_1479238b ON public.mi_admin_resumentrimestral USING btree (estudiante_id);


--
-- Name: mi_admin_resumentrimestral_trimestre_id_24010350; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_resumentrimestral_trimestre_id_24010350 ON public.mi_admin_resumentrimestral USING btree (trimestre_id);


--
-- Name: mi_admin_rol_nombre_f2fa2889_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_rol_nombre_f2fa2889_like ON public.mi_admin_rol USING btree (nombre varchar_pattern_ops);


--
-- Name: mi_admin_subcomponente_asignacion_id_bb1f5102; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_subcomponente_asignacion_id_bb1f5102 ON public.mi_admin_subcomponente USING btree (asignacion_id);


--
-- Name: mi_admin_subcomponente_tipo_componente_id_874e8340; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_subcomponente_tipo_componente_id_874e8340 ON public.mi_admin_subcomponente USING btree (tipo_componente_id);


--
-- Name: mi_admin_subcomponente_trimestre_id_2e42685a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_subcomponente_trimestre_id_2e42685a ON public.mi_admin_subcomponente USING btree (trimestre_id);


--
-- Name: mi_admin_tipocomponente_nombre_21256e36_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_tipocomponente_nombre_21256e36_like ON public.mi_admin_tipocomponente USING btree (nombre varchar_pattern_ops);


--
-- Name: mi_admin_usuario_email_0468591e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_email_0468591e_like ON public.mi_admin_usuario USING btree (email varchar_pattern_ops);


--
-- Name: mi_admin_usuario_groups_group_id_c895e477; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_groups_group_id_c895e477 ON public.mi_admin_usuario_groups USING btree (group_id);


--
-- Name: mi_admin_usuario_groups_usuario_id_248b6571; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_groups_usuario_id_248b6571 ON public.mi_admin_usuario_groups USING btree (usuario_id);


--
-- Name: mi_admin_usuario_rol_id_1681c779; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_rol_id_1681c779 ON public.mi_admin_usuario USING btree (rol_id);


--
-- Name: mi_admin_usuario_user_permissions_permission_id_39bb7e2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_user_permissions_permission_id_39bb7e2c ON public.mi_admin_usuario_user_permissions USING btree (permission_id);


--
-- Name: mi_admin_usuario_user_permissions_usuario_id_12b5103b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_user_permissions_usuario_id_12b5103b ON public.mi_admin_usuario_user_permissions USING btree (usuario_id);


--
-- Name: mi_admin_usuario_username_0c408cb2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mi_admin_usuario_username_0c408cb2_like ON public.mi_admin_usuario USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_mi_admin_usuario_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_mi_admin_usuario_id FOREIGN KEY (user_id) REFERENCES public.mi_admin_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_administrativo mi_admin_administrat_persona_id_71387532_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_administrativo
    ADD CONSTRAINT mi_admin_administrat_persona_id_71387532_fk_mi_admin_ FOREIGN KEY (persona_id) REFERENCES public.mi_admin_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asignacion mi_admin_asignacion_curso_id_2af5c132_fk_mi_admin_curso_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asignacion
    ADD CONSTRAINT mi_admin_asignacion_curso_id_2af5c132_fk_mi_admin_curso_id FOREIGN KEY (curso_id) REFERENCES public.mi_admin_curso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asignacion mi_admin_asignacion_docente_id_6eda5e97_fk_mi_admin_docente_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asignacion
    ADD CONSTRAINT mi_admin_asignacion_docente_id_6eda5e97_fk_mi_admin_docente_id FOREIGN KEY (docente_id) REFERENCES public.mi_admin_docente(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asignacion mi_admin_asignacion_materia_id_a290889c_fk_mi_admin_materia_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asignacion
    ADD CONSTRAINT mi_admin_asignacion_materia_id_a290889c_fk_mi_admin_materia_id FOREIGN KEY (materia_id) REFERENCES public.mi_admin_materia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asistencia mi_admin_asistencia_asignacion_id_3b5f93e8_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asistencia
    ADD CONSTRAINT mi_admin_asistencia_asignacion_id_3b5f93e8_fk_mi_admin_ FOREIGN KEY (asignacion_id) REFERENCES public.mi_admin_asignacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asistencia mi_admin_asistencia_estudiante_id_ca4600ba_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asistencia
    ADD CONSTRAINT mi_admin_asistencia_estudiante_id_ca4600ba_fk_mi_admin_ FOREIGN KEY (estudiante_id) REFERENCES public.mi_admin_estudiante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_asistencia mi_admin_asistencia_trimestre_id_686f5c8c_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_asistencia
    ADD CONSTRAINT mi_admin_asistencia_trimestre_id_686f5c8c_fk_mi_admin_ FOREIGN KEY (trimestre_id) REFERENCES public.mi_admin_trimestre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_desempenoestudiante mi_admin_desempenoes_asignacion_id_db0a34b5_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_desempenoestudiante
    ADD CONSTRAINT mi_admin_desempenoes_asignacion_id_db0a34b5_fk_mi_admin_ FOREIGN KEY (asignacion_id) REFERENCES public.mi_admin_asignacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_desempenoestudiante mi_admin_desempenoes_estudiante_id_b992a1c6_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_desempenoestudiante
    ADD CONSTRAINT mi_admin_desempenoes_estudiante_id_b992a1c6_fk_mi_admin_ FOREIGN KEY (estudiante_id) REFERENCES public.mi_admin_estudiante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_desempenoestudiante mi_admin_desempenoes_trimestre_id_a3bf80ef_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_desempenoestudiante
    ADD CONSTRAINT mi_admin_desempenoes_trimestre_id_a3bf80ef_fk_mi_admin_ FOREIGN KEY (trimestre_id) REFERENCES public.mi_admin_trimestre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_docente mi_admin_docente_persona_id_25ebbc7f_fk_mi_admin_persona_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_docente
    ADD CONSTRAINT mi_admin_docente_persona_id_25ebbc7f_fk_mi_admin_persona_id FOREIGN KEY (persona_id) REFERENCES public.mi_admin_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_estudiante mi_admin_estudiante_curso_actual_id_0970e4a9_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_estudiante
    ADD CONSTRAINT mi_admin_estudiante_curso_actual_id_0970e4a9_fk_mi_admin_ FOREIGN KEY (curso_actual_id) REFERENCES public.mi_admin_curso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_estudiante mi_admin_estudiante_persona_id_664a5bd4_fk_mi_admin_persona_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_estudiante
    ADD CONSTRAINT mi_admin_estudiante_persona_id_664a5bd4_fk_mi_admin_persona_id FOREIGN KEY (persona_id) REFERENCES public.mi_admin_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_evaluacion mi_admin_evaluacion_asignacion_id_8115ea3e_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_evaluacion
    ADD CONSTRAINT mi_admin_evaluacion_asignacion_id_8115ea3e_fk_mi_admin_ FOREIGN KEY (asignacion_id) REFERENCES public.mi_admin_asignacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_evaluacion mi_admin_evaluacion_subcomponente_id_4330b11d_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_evaluacion
    ADD CONSTRAINT mi_admin_evaluacion_subcomponente_id_4330b11d_fk_mi_admin_ FOREIGN KEY (subcomponente_id) REFERENCES public.mi_admin_subcomponente(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_evaluacion mi_admin_evaluacion_trimestre_id_37c50278_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_evaluacion
    ADD CONSTRAINT mi_admin_evaluacion_trimestre_id_37c50278_fk_mi_admin_ FOREIGN KEY (trimestre_id) REFERENCES public.mi_admin_trimestre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_inscripcion mi_admin_inscripcion_curso_id_8dee0232_fk_mi_admin_curso_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_inscripcion
    ADD CONSTRAINT mi_admin_inscripcion_curso_id_8dee0232_fk_mi_admin_curso_id FOREIGN KEY (curso_id) REFERENCES public.mi_admin_curso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_inscripcion mi_admin_inscripcion_estudiante_id_0c3438e2_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_inscripcion
    ADD CONSTRAINT mi_admin_inscripcion_estudiante_id_0c3438e2_fk_mi_admin_ FOREIGN KEY (estudiante_id) REFERENCES public.mi_admin_estudiante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_nota mi_admin_nota_estudiante_id_7d9f3ddb_fk_mi_admin_estudiante_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_nota
    ADD CONSTRAINT mi_admin_nota_estudiante_id_7d9f3ddb_fk_mi_admin_estudiante_id FOREIGN KEY (estudiante_id) REFERENCES public.mi_admin_estudiante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_nota mi_admin_nota_evaluacion_id_87b47133_fk_mi_admin_evaluacion_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_nota
    ADD CONSTRAINT mi_admin_nota_evaluacion_id_87b47133_fk_mi_admin_evaluacion_id FOREIGN KEY (evaluacion_id) REFERENCES public.mi_admin_evaluacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_persona mi_admin_persona_usuario_id_e0c29bb2_fk_mi_admin_usuario_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_persona
    ADD CONSTRAINT mi_admin_persona_usuario_id_e0c29bb2_fk_mi_admin_usuario_id FOREIGN KEY (usuario_id) REFERENCES public.mi_admin_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_resumentrimestral mi_admin_resumentrim_asignacion_id_d38bfd77_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_resumentrimestral
    ADD CONSTRAINT mi_admin_resumentrim_asignacion_id_d38bfd77_fk_mi_admin_ FOREIGN KEY (asignacion_id) REFERENCES public.mi_admin_asignacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_resumentrimestral mi_admin_resumentrim_estudiante_id_1479238b_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_resumentrimestral
    ADD CONSTRAINT mi_admin_resumentrim_estudiante_id_1479238b_fk_mi_admin_ FOREIGN KEY (estudiante_id) REFERENCES public.mi_admin_estudiante(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_resumentrimestral mi_admin_resumentrim_trimestre_id_24010350_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_resumentrimestral
    ADD CONSTRAINT mi_admin_resumentrim_trimestre_id_24010350_fk_mi_admin_ FOREIGN KEY (trimestre_id) REFERENCES public.mi_admin_trimestre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_subcomponente mi_admin_subcomponen_asignacion_id_bb1f5102_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_subcomponente
    ADD CONSTRAINT mi_admin_subcomponen_asignacion_id_bb1f5102_fk_mi_admin_ FOREIGN KEY (asignacion_id) REFERENCES public.mi_admin_asignacion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_subcomponente mi_admin_subcomponen_tipo_componente_id_874e8340_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_subcomponente
    ADD CONSTRAINT mi_admin_subcomponen_tipo_componente_id_874e8340_fk_mi_admin_ FOREIGN KEY (tipo_componente_id) REFERENCES public.mi_admin_tipocomponente(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_subcomponente mi_admin_subcomponen_trimestre_id_2e42685a_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_subcomponente
    ADD CONSTRAINT mi_admin_subcomponen_trimestre_id_2e42685a_fk_mi_admin_ FOREIGN KEY (trimestre_id) REFERENCES public.mi_admin_trimestre(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_usuario_groups mi_admin_usuario_gro_usuario_id_248b6571_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_groups
    ADD CONSTRAINT mi_admin_usuario_gro_usuario_id_248b6571_fk_mi_admin_ FOREIGN KEY (usuario_id) REFERENCES public.mi_admin_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_usuario_groups mi_admin_usuario_groups_group_id_c895e477_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_groups
    ADD CONSTRAINT mi_admin_usuario_groups_group_id_c895e477_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_usuario mi_admin_usuario_rol_id_1681c779_fk_mi_admin_rol_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario
    ADD CONSTRAINT mi_admin_usuario_rol_id_1681c779_fk_mi_admin_rol_id FOREIGN KEY (rol_id) REFERENCES public.mi_admin_rol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_usuario_user_permissions mi_admin_usuario_use_permission_id_39bb7e2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_user_permissions
    ADD CONSTRAINT mi_admin_usuario_use_permission_id_39bb7e2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mi_admin_usuario_user_permissions mi_admin_usuario_use_usuario_id_12b5103b_fk_mi_admin_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mi_admin_usuario_user_permissions
    ADD CONSTRAINT mi_admin_usuario_use_usuario_id_12b5103b_fk_mi_admin_ FOREIGN KEY (usuario_id) REFERENCES public.mi_admin_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

