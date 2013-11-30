CREATE TABLE languages
(
  id serial NOT NULL,
  name character varying(60) NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT languages_pkey PRIMARY KEY (id, fetched_at),
  CONSTRAINT languages_unique UNIQUE (name, fetched_at)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE languages OWNER TO wikiteams;