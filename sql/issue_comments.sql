CREATE TABLE issues_comments
(
  id integer NOT NULL,
  issue_id integer NOT NULL,
  user_id integer NOT NULL,
  repository_id integer NOT NULL,
  body text,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT issues_comment_pkey PRIMARY KEY (id, issue_id, user_id, fetched_at),
  CONSTRAINT ic_issuefk FOREIGN KEY (issue_id, repository_id, fetched_at)
      REFERENCES issues (number, repository_id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT ic_userfk FOREIGN KEY (user_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT issues_comments_unique UNIQUE (id, fetched_at)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE issues_comments OWNER TO wikiteams;