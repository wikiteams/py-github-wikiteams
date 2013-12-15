CREATE TABLE languages
(
  id serial NOT NULL,
  name character varying(60) NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  run_id integer NOT NULL,
  CONSTRAINT languages_pkey PRIMARY KEY (id, run_id),
  CONSTRAINT languages_unique UNIQUE (name, run_id),
  CONSTRAINT l_runfk FOREIGN KEY (run_id)
      REFERENCES runs (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE languages OWNER TO wikiteams;