CREATE TABLE repositories_users
(
  repository_id integer NOT NULL,
  user_id integer NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  run_id integer NOT NULL,
  CONSTRAINT repositories_users_pkey PRIMARY KEY (repository_id, user_id, run_id),
  CONSTRAINT ru_userfk FOREIGN KEY (user_id, run_id)
      REFERENCES users (id, run_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT ru_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT ru_runfk FOREIGN KEY (run_id)
      REFERENCES runs (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories_users OWNER TO wikiteams;