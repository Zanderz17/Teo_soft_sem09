DROP TABLE logs;

CREATE TABLE logs (
    log_id serial PRIMARY KEY,
    log_timestamp timestamp,
    log_level text,
    module_name text,
    api text,
    func_name text,
    log_message text,
    elapsed_time_ms double precision
);

CREATE INDEX idx_log_timestamp ON logs (log_timestamp);


COPY logs(log_timestamp, log_level, module_name, api,func_name, log_message, elapsed_time_ms)
FROM '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana09/Tarea/POKE_API/app.csv' DELIMITER ';';


SELECT log_level,
    COUNT(*) AS cantidad
    FROM logs
    GROUP BY log_level;


SELECT AVG(elapsed_time_ms) AS promedio_elapsed_time
    FROM logs;