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
  run_id integer NOT NULL,
  CONSTRAINT commits_comment_pkey PRIMARY KEY (id, commit_id, user_id, run_id),
  CONSTRAINT cc_commitfk FOREIGN KEY (commit_id, repository_id, run_id)
      REFERENCES commits (sha, repository_id, run_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT cc_userfk FOREIGN KEY (user_id, run_id)
      REFERENCES users (id, run_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT commits_comments_unique UNIQUE (id, run_id),
  CONSTRAINT cc_runfk FOREIGN KEY (run_id)
      REFERENCES runs (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE commits_comments OWNER TO wikiteams;