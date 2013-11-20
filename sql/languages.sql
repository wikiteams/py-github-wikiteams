CREATE TABLE languages
(
  id serial NOT NULL,
  name character varying(300)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE languages OWNER TO wikiteams;