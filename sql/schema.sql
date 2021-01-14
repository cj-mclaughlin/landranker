/* Table of Lands */
CREATE TYPE land_type as ENUM ('island', 'mountain', 'swamp', 'plains', 'forest');

CREATE TABLE lands (
	land_id SERIAL PRIMARY KEY,
	type land_type NOT NULL, 
	artist_name VARCHAR(50),
	s3_url VARCHAR(100) NOT NULL,
	elo integer DEFAULT 1000
);

/* Table of Game Records */
CREATE TABLE records (
	record_id SERIAL PRIMARY KEY,
	land_id1 integer REFERENCES lands (land_id),
	land_id2 integer REFERENCES lands (land_id),
	result boolean NOT NULL 
);
