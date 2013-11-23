CREATE TABLE repositories_languages
(
  repository_id integer NOT NULL,
  language_id integer NOT NULL,
  bytes integer NOT NULL,
  CONSTRAINT repositories_languages_pkey PRIMARY KEY (repository_id, language_id),
  CONSTRAINT rl_languagefk FOREIGN KEY (language_id)
      REFERENCES languages (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT rl_repositoryfk FOREIGN KEY (repository_id)
      REFERENCES repositories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories_languages OWNER TO wikiteams;