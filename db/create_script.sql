-- Remove conflicting tables
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS chanel CASCADE;
DROP TABLE IF EXISTS user_ CASCADE;
DROP TABLE IF EXISTS video CASCADE;
DROP TABLE IF EXISTS watchrecord CASCADE;
-- End of removing

CREATE TABLE category (
    id_category SERIAL NOT NULL,
    name VARCHAR(256) NOT NULL
);
ALTER TABLE category ADD CONSTRAINT pk_category PRIMARY KEY (id_category);

CREATE TABLE chanel (
    id_chanel VARCHAR(60) NOT NULL,
    name VARCHAR(256) NOT NULL
);
ALTER TABLE chanel ADD CONSTRAINT pk_chanel PRIMARY KEY (id_chanel);

CREATE TABLE user_ (
    id_user SERIAL NOT NULL
);
ALTER TABLE user_ ADD CONSTRAINT pk_user_ PRIMARY KEY (id_user);

CREATE TABLE video (
    id_video VARCHAR(60) NOT NULL,
    id_category INTEGER NOT NULL,
    id_chanel VARCHAR(60) NOT NULL,
    name VARCHAR(256) NOT NULL
);
ALTER TABLE video ADD CONSTRAINT pk_video PRIMARY KEY (id_video);

CREATE TABLE watchrecord (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    id_user INTEGER NOT NULL,
    id_video VARCHAR(60) NOT NULL
);
ALTER TABLE watchrecord ADD CONSTRAINT pk_watchrecord PRIMARY KEY (time, id_user, id_video);

ALTER TABLE video ADD CONSTRAINT fk_video_category FOREIGN KEY (id_category) REFERENCES category (id_category) ON DELETE CASCADE;
ALTER TABLE video ADD CONSTRAINT fk_video_chanel FOREIGN KEY (id_chanel) REFERENCES chanel (id_chanel) ON DELETE CASCADE;

ALTER TABLE watchrecord ADD CONSTRAINT fk_watchrecord_user_ FOREIGN KEY (id_user) REFERENCES user_ (id_user) ON DELETE CASCADE;
ALTER TABLE watchrecord ADD CONSTRAINT fk_watchrecord_video FOREIGN KEY (id_video) REFERENCES video (id_video) ON DELETE CASCADE;
