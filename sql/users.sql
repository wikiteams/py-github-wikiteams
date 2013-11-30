CREATE TABLE users
(
  id integer NOT NULL,
  login character varying(200) NOT NULL,
  name character varying(200),
  type character varying(20) NOT NULL,
  email character varying(200),
  location character varying(200),
  company character varying(200),
  bio text,
  blog character varying(200),
  disk_usage integer,
  gravatar_id character varying(200),
  hireable boolean,
  followers integer NOT NULL,
  following integer NOT NULL,
  collaborators integer,
  contributions integer NOT NULL,
  public_repos integer NOT NULL,
  owned_private_repos integer,
  total_private_repos integer,
  public_gists integer NOT NULL,
  private_gists integer,
  url character varying(200) NOT NULL,
  avatar_url character varying(200) NOT NULL,
  events_url character varying(200) NOT NULL,
  followers_url character varying(200) NOT NULL,
  following_url character varying(200) NOT NULL,
  gists_url character varying(200) NOT NULL,
  html_url character varying(200) NOT NULL,
  organizations_url character varying(200) NOT NULL,
  received_events_url character varying(200) NOT NULL,
  repos_url character varying(200) NOT NULL,
  starred_url character varying(200) NOT NULL,
  subscriptions_url character varying(200) NOT NULL,
  created_at character varying(200) NOT NULL,
  updated_at character varying(200) NOT NULL,
  fetched_at date NOT NULL DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (id, fetched_at)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE users OWNER TO wikiteams;
