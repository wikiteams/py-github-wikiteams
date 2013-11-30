CREATE TABLE repositories
(
  id serial NOT NULL,
  owner character varying(150) NOT NULL,
  name character varying(150) NOT NULL,
  full_name character varying(150) NOT NULL,
  description text,
  private boolean,
  fork boolean,
  url character varying(150),
  html_url character varying(150),
  clone_url character varying(150),
  git_url character varying(150),
  ssh_url character varying(150),
  svn_url character varying(150),
  mirror_url character varying(150),
  homepage character varying(150),
  forks_count integer NOT NULL,
  stargazers_count integer NOT NULL,
  watchers_count integer NOT NULL,
  size integer NOT NULL,
  master_branch character varying(150) NOT NULL,
  open_issues_count integer NOT NULL,
  pushed_at timestamp without time zone,
  created_at timestamp without time zone,
  subscribers_count integer,
  has_issues boolean,
  has_wiki boolean,
  has_downloads boolean,
  CONSTRAINT repositories_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE repositories OWNER TO wikiteams;
