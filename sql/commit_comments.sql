CREATE TABLE commits_comments
(
  id integer NOT NULL,
  commit_id character varying(40) NOT NULL,
  user_id integer NOT NULL,
  repository_id integer NOT NULL,
  body text,
  path character varying(150),
  line integer,
  position integer,
  url character varying(150),
  html_url character varying(150),
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT commits_comment_pkey PRIMARY KEY (id, commit_id, user_id, fetched_at),
  CONSTRAINT cc_commitfk FOREIGN KEY (commit_id, repository_id, fetched_at)
      REFERENCES commits (sha, repository_id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT cc_userfk FOREIGN KEY (user_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT commits_comments_unique UNIQUE (id, fetched_at)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE commits_comments OWNER TO wikiteams;