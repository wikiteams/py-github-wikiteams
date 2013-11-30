CREATE TABLE repositories_users
(
  repository_id integer NOT NULL,
  user_id integer NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT repositories_users_pkey PRIMARY KEY (repository_id, user_id, fetched_at),
  CONSTRAINT ru_userfk FOREIGN KEY (user_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT ru_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories_users OWNER TO wikiteams;