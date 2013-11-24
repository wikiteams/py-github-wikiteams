CREATE TABLE commits
(
  sha character varying(40) NOT NULL,
  repository_id integer NOT NULL,
  author_id integer NOT NULL,
  committer_id integer NOT NULL,
  message text,
  additions integer,
  deletions integer,
  CONSTRAINT commits_pkey PRIMARY KEY (sha, repository_id),
  CONSTRAINT u_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT u_authorfk FOREIGN KEY (author_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT u_commiterfk FOREIGN KEY (committer_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE commits OWNER TO wikiteams;