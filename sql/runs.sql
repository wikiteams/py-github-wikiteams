CREATE TABLE runs
(
  id serial NOT NULL,
  added_at date NOT NULL DEFAULT now(),
  CONSTRAINT runs_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE runs OWNER TO wikiteams;