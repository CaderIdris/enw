CREATE TABLE IF NOT EXISTS fact_surface_vars (
	surface_var_hash_sha256 TEXT NOT NULL CHECK (LENGTH (surface_var_hash_sha256) = 64),
	--SHA256 (site_hash_sha256 + device_hash_sha256 + m_time)
	site_hash_sha256 TEXT NOT NULL CHECK (LENGTH (site_hash_sha256) = 64),
	device_hash_sha256 TEXT NOT NULL CHECK (LENGTH (device_hash_sha256) = 64),
	m_time INTEGER NOT NULL CHECK (m_time > 0),
	pressure REAL NOT NULL CHECK (pressure > 0),
	temperature REAL NOT NULL,
	azimuth REAL NOT NULL,
	appSZA REAL NOT NULL,
	qual_flag INT NOT NULL CHECK (qual_flag IN (0, 1)),
	FOREIGN KEY (site_hash_sha256) REFERENCES dim_site (site_hash_sha256),
	PRIMARY KEY (surface_var_hash_sha256)
) STRICT;
