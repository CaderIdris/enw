CREATE TABLE IF NOT EXISTS dim_height (
	height_hash_sha256 TEXT NOT NULL CHECK (LENGTH (height_hash_sha256) = 64),
	--SHA256 (site_hash_sha256 + device_hash_sha256 + height)
	site_hash_sha256 TEXT NOT NULL CHECK (LENGTH (site_hash_sha256) = 64),
	device_hash_sha256 TEXT NOT NULL CHECK (LENGTH (device_hash_sha256) = 64),
	height REAL CHECK (height > 0),
	pressure_b REAL NOT NULL CHECK (pressure_b > 0),
	pressure_t REAL NOT NULL CHECK (pressure_t > 0),
	FOREIGN KEY (site_hash_sha256) REFERENCES dim_site (site_hash_sha256),
	PRIMARY KEY (height_hash_sha256)
) STRICT;
