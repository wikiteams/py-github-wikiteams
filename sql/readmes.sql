CREATE TABLE readmes
(
  repository_id integer NOT NULL,
  type character varying(60) NOT NULL,
  content text,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT readmes_pkey PRIMARY KEY (repository_id, fetched_at),
  CONSTRAINT r_repositoryfk FOREIGN KEY (repository_id, fetched_at)
      REFERENCES languages (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE readmes OWNER TO wikiteams;