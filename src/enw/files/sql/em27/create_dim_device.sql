CREATE TABLE IF NOT EXISTS dim_device (
	device_hash_sha256 TEXT NOT NULL CHECK (LENGTH (device_hash_sha256) = 64), --SHA256 (device_name)
	device_name TEXT NOT NULL,
	PRIMARY KEY (device_hash_sha256)
) STRICT;
