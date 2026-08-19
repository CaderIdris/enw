CREATE TABLE IF NOT EXISTS fact_height_vars (
	height_var_hash_sha256 TEXT NOT NULL CHECK (LENGTH (height_var_hash_sha256) = 64),
	--SHA256 (height_hash_sha256 + m_time + species)
	height_hash_sha256 TEXT NOT NULL CHECK (LENGTH (height_hash_sha256) = 64),
	m_time INTEGER NOT NULL CHECK (m_time > 0),
	species TEXT NOT NULL CHECK (species IN ('CH4', 'CO2', 'CO')),
	averaging_kernel REAL NOT NULL CHECK (averaging_kernel > 0),
	averaging_kernel_alt REAL,
	FOREIGN KEY (height_hash_sha256) REFERENCES dim_height (height_hash_sha256),
	PRIMARY KEY (height_var_hash_sha256)
) STRICT;
