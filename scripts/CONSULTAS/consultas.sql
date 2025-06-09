-- valores médios de ambiencia: Velocidade do vento
select
	aviario,
    feed_phase,
    vel_vento   
from
	vw_report_wind_by_days
where
	vel_vento > 0;

-- valores médios de ambiencia: Temperatura ambiente
select
	aviario,
    feed_phase,
    amb_temp
from
	vw_report_atemp_by_days
where
	amb_temp > 0;

-- valores médios de ambiencia: Temperatura da cama
select
	aviario,
    feed_phase,
    bed_temp
from
	vw_report_btemp_by_days
where
	bed_temp > 0;

-- valores médios de ambiencia: luminosidade
select
	aviario,
    feed_phase,
    light
from
	vw_report_light_by_days
where
	light > 0;

-- valores médios de ambiencia: umidade relativa
select
	aviario,
    feed_phase,
    umidade
from
	vw_report_humidity_by_days
where
	umidade > 0;

-- valores médios de ambiencia: temperatura da agua
select
	aviario,
    feed_phase,
    temp_agua
from
	vw_report_wtemp_by_days
where
	temp_agua > 0;

--quantidade de água por fase de criação
select
	aviario,
	feed_phase,
	consumo_agua
from
	vw_report_water_by_days
where
	consumo_agua > 0;

--quantidade de eletricidade por fase de criação
select
	aviario,
	feed_phase,
	total_electricity_by_days as eletricidade
from
	vw_report_electricity_by_days
WHERE
	total_electricity_by_days > 0;

--quantidade de ração por fase de criação
select
    aviario,
    feed_phase,
    total_feed_by_days as total_racao
from
    vw_report_feed_by_days
where
    total_feed_by_days > 0;


-- Consulta para criar uma visão combinada de todos os relatórios
-- Esta consulta combina os dados de várias visões para criar um relatório abrangente
-- A consulta abaixo está comentada para evitar a criação de uma tabela permanente
-- Caso queira criar uma tabela permanente, descomente a consulta abaixo


/*
    CREATE TABLE report_combined AS
    SELECT 
        w.aviario,
        w.feed_phase,
        w.vel_vento,
        at.amb_temp,
        bt.bed_temp,
        l.light,
        h.umidade,
        wt.temp_agua,
        wa.consumo_agua,
        e.eletricidade,
        f.total_feed_by_days as total_racao
    FROM vw_report_wind_by_days w
    LEFT JOIN vw_report_atemp_by_days at ON w.aviario = at.aviario AND w.feed_phase = at.feed_phase
    LEFT JOIN vw_report_btemp_by_days bt ON w.aviario = bt.aviario AND w.feed_phase = bt.feed_phase
    LEFT JOIN vw_report_light_by_days l ON w.aviario = l.aviario AND w.feed_phase = l.feed_phase
    LEFT JOIN vw_report_humidity_by_days h ON w.aviario = h.aviario AND w.feed_phase = h.feed_phase
    LEFT JOIN vw_report_wtemp_by_days wt ON w.aviario = wt.aviario AND w.feed_phase = wt.feed_phase
    LEFT JOIN vw_report_water_by_days wa ON w.aviario = wa.aviario AND w.feed_phase = wa.feed_phase
    LEFT JOIN vw_report_electricity_by_days e ON w.aviario = e.aviario AND w.feed_phase = e.feed_phase
    LEFT JOIN vw_report_feed_by_days f ON w.aviario = f.aviario AND w.feed_phase = f.feed_phase;
*/

CREATE TABLE ambiencia_consumo (
    aviario TEXT,
    feed_phase TEXT,
    vel_vento REAL,
    amb_temp REAL,
    bed_temp REAL,
    light REAL,
    umidade REAL,
    temp_agua REAL,
    consumo_agua REAL,
    eletricidade REAL,
    total_racao REAL
);

INSERT INTO ambiencia_consumo
SELECT 
    w.aviario,
    w.feed_phase,
    w.vel_vento,
    t.amb_temp,
    b.bed_temp,
    l.light,
    h.umidade,
    wt.temp_agua,
    total_electricity_by_days as eletricidade,
    total_water_by_days as consumo_agua,
    total_feed_by_days as total_racao
FROM vw_report_wind_by_days w
LEFT JOIN vw_report_atemp_by_days t ON w.aviario = t.aviario AND w.feed_phase = t.feed_phase
LEFT JOIN vw_report_btemp_by_days b ON w.aviario = b.aviario AND w.feed_phase = b.feed_phase
LEFT JOIN vw_report_light_by_days l ON w.aviario = l.aviario AND w.feed_phase = l.feed_phase
LEFT JOIN vw_report_humidity_by_days h ON w.aviario = h.aviario AND w.feed_phase = h.feed_phase
LEFT JOIN vw_report_wtemp_by_days wt ON w.aviario = wt.aviario AND w.feed_phase = wt.feed_phase
LEFT JOIN vw_report_water_by_days wa ON w.aviario = wa.aviario AND w.feed_phase = wa.feed_phase
LEFT JOIN vw_report_electricity_by_days e ON w.aviario = e.aviario AND w.feed_phase = e.feed_phase
LEFT JOIN vw_report_feed_by_days f ON w.aviario = f.aviario AND w.feed_phase = f.feed_phase;


select * from ambiencia_consumo;
