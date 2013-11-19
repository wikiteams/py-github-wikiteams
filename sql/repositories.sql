CREATE TABLE repositories
(
  id serial NOT NULL,
  owner character varying(300),
  name character varying(300),
  forks integer,
  watchers integer,
  CONSTRAINT repositories_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories OWNER TO wikiteams;
