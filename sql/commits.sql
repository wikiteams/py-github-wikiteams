CREATE TABLE commits
(
  sha character varying(40) NOT NULL,
  repository_id integer NOT NULL,
  author_id integer,
  committer_id integer,
  message text,
  additions integer,
  deletions integer,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT commits_pkey PRIMARY KEY (sha, repository_id, fetched_at),
  CONSTRAINT u_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT u_authorfk FOREIGN KEY (author_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT u_commiterfk FOREIGN KEY (committer_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE commits OWNER TO wikiteams;