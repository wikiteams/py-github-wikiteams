CREATE TABLE readmes
(
  repository_id integer NOT NULL,
  type character varying(60) NOT NULL,
  content text,
  fetched_at date NOT NULL DEFAULT now(),
  run_id integer NOT NULL,
  CONSTRAINT readmes_pkey PRIMARY KEY (repository_id, run_id),
  CONSTRAINT r_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT r_runfk FOREIGN KEY (run_id)
      REFERENCES runs (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE readmes OWNER TO wikiteams;