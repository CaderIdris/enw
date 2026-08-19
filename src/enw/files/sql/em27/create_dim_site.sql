CREATE TABLE IF NOT EXISTS dim_site (
	site_hash_sha256 TEXT NOT NULL CHECK (LENGTH (site_hash_sha256) = 64), --SHA256 (site_name)
	site_name TEXT NOT NULL,
	PRIMARY KEY (site_hash_sha256)
) STRICT;
