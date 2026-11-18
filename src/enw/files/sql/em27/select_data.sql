WITH data AS (
	SELECT
		DATETIME(CAST(f_height.m_time AS INTEGER), 'unixepoch') AS datetime,
		f_height.m_time,
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
		f_surface.altitude,
		f_surface.azimuth,
		f_surface.appSZA,
		(d_height.pressure_b - d_height.pressure_t) / f_surface.pressure AS Wp
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
	AND 
		d_height.height * 1000 <= :height_limit
	AND
		UNIXEPOCH(:start_time) <= f_height.m_time
	AND
		UNIXEPOCH(:end_time) > f_height.m_time
),
grouped AS 
(
	SELECT
		datetime,
		species,
		device_name,
		SUM(Wp) AS SUM_Wp,
		SUM(averaging_kernel) AS SUM_averaging_kernel,
		SUM(Wp * averaging_kernel) AS SUM_product
	FROM
		data
	GROUP BY
		datetime,
		species,
		device_name
)
SELECT
	DATETIME(FLOOR(d.m_time / :num_seconds) * :num_seconds, 'unixepoch') AS datetime,
	d.species,
	d.device_name,
	d.site_name,
	d.height * 1000 AS height,
	d.pressure_b,
	d.pressure_t,
	d.latitude,
	d.longitude,
	d.altitude,
	AVG(d.azimuth) AS azimuth,
	AVG(d.appSZA) AS appSZA,
	AVG((d.Wp * d.averaging_kernel) / grouped.SUM_product) AS source_strength
FROM 
	data as d
LEFT JOIN
	grouped AS grouped
ON
	grouped.datetime = d.datetime
AND
	grouped.species = d.species
AND
	grouped.device_name = d.device_name
GROUP BY
	d.device_name,
	d.site_name,
	d.species,
	d.height,
	FLOOR(d.m_time / :num_seconds)
ORDER BY
	d.device_name,
	d.site_name,
	d.species,
	datetime,
	d.height
;
