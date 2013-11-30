CREATE TABLE issues
(
  number integer NOT NULL,
  repository_id integer NOT NULL,
  user_id integer,
  assignee_id integer,
  state character varying(30) NOT NULL,
  title character varying(200) NOT NULL,
  body text,
  url character varying(200) NOT NULL,
  html_url character varying(200) NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT issues_pkey PRIMARY KEY (number, repository_id, fetched_at),
  CONSTRAINT i_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT i_userfk FOREIGN KEY (user_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT i_assigneefk FOREIGN KEY (assignee_id, fetched_at)
      REFERENCES users (id, fetched_at) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE issues OWNER TO wikiteams;