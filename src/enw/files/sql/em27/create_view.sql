DROP VIEW IF EXISTS view_data;
CREATE VIEW IF NOT EXISTS
	view_data
AS
SELECT
	DATETIME(CAST(f_height.m_time AS INTEGER), 'unixepoch') AS datetime,
	f_height.species,
	f_height.averaging_kernel,
	d_height.height,
	d_height.pressure_b,
	d_height.pressure_t,
	d_site.site_name,
	d_device.device_name,
	f_surface.pressure,
	f_surface.temperature,
	f_surface.latitude,
	f_surface.longitude,
	f_surface.azimuth,
	f_surface.appSZA
FROM
	fact_height_vars AS f_height
LEFT JOIN
	dim_height AS d_height
ON
	d_height.height_hash_sha256 = f_height.height_hash_sha256
LEFT JOIN
	dim_site AS d_site
ON
	d_site.site_hash_sha256 = d_height.site_hash_sha256
LEFT JOIN
	dim_device AS d_device
ON
	d_device.device_hash_sha256 = d_height.device_hash_sha256
LEFT JOIN 
	fact_surface_vars AS f_surface
ON
	f_surface.site_hash_sha256 = d_site.site_hash_sha256
AND
	f_surface.m_time = f_height.m_time
WHERE
	f_surface.qual_flag = 1
;
