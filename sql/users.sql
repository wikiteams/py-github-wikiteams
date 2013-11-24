CREATE TABLE users
(
  id integer NOT NULL,
  login character varying(300) NOT NULL,
  name character varying(300),
  type character varying(300) NOT NULL,
  email character varying(300),
  location character varying(300),
  company character varying(300),
  bio text,
  blog character varying(300),
  disk_usage character varying(300),
  gravatar_id character varying(300),
  hireable character varying(300),
  followers character varying(300) NOT NULL,
  following character varying(300) NOT NULL,
  collaborators character varying(300),
  contributions character varying(300) NOT NULL,
  public_repos character varying(300) NOT NULL,
  owned_private_repos character varying(300),
  total_private_repos character varying(300),
  public_gists character varying(300) NOT NULL,
  private_gists character varying(300),
  url character varying(300) NOT NULL,
  avatar_url character varying(300) NOT NULL,
  events_url character varying(300) NOT NULL,
  followers_url character varying(300) NOT NULL,
  following_url character varying(300) NOT NULL,
  gists_url character varying(300) NOT NULL,
  html_url character varying(300) NOT NULL,
  organizations_url character varying(300) NOT NULL,
  received_events_url character varying(300) NOT NULL,
  repos_url character varying(300) NOT NULL,
  starred_url character varying(300) NOT NULL,
  subscriptions_url character varying(300) NOT NULL,
  created_at character varying(300) NOT NULL,
  updated_at character varying(300) NOT NULL,
  CONSTRAINT users_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE users OWNER TO wikiteams;
