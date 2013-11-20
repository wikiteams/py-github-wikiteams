CREATE TABLE repositories_languages
(
  repository_id integer,
  language_id integer
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories_languages OWNER TO wikiteams;