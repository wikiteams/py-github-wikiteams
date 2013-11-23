CREATE TABLE languages
(
  id serial NOT NULL,
  name character varying(300),
  CONSTRAINT languages_pkey PRIMARY KEY (id),
  CONSTRAINT languages_name_key UNIQUE (name)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE languages OWNER TO wikiteams;