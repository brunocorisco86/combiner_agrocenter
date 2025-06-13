/* select da base dados_sensores (Uma amostra da base de dados de sensores de aviários)
   para verificar a estrutura e os dados iniciais.
   A tabela contém informações sobre sensores em diferentes aviários, 
   incluindo tipo de evento, valor, unidade, nome do aviário, nome da fazenda, 
   nome do produtor, idade do lote, número do lote, id do sensor, posição do sensor e mês/ano.
*/

/*select * from dados_sensores ds limit 15; --Amostra os primeiros 15 registros da tabela dados_sensores
data               |tipo_de_evento     |valor  |unidade|nome_do_aviario|nome_da_fazenda|nome_do_produtor   |idade_do_lote|numero_do_lote|id_do_sensor                 |posicao_do_sensor|mes_ano|
-------------------+-------------------+-------+-------+---------------+---------------+-------------------+-------------+--------------+-----------------------------+-----------------+-------+
01/04/2025 00:00:00|Temperatura da Água|  25.75|ºC     |170            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|           169|0000:004B:0020:6016:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água|25.8125|ºC     |1077           |SK - JACINTO   |JACINTO JOSE ALFLEN|           37|            37|0000:0062:0027:6019:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água|  26.25|ºC     |171            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|           169|0000:005B:001A:6016:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água| 26.375|ºC     |170            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|           169|0000:0013:002B:6019:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água|   26.5|ºC     |884            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|            67|0000:0006:003D:6019:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água|26.8125|ºC     |171            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|           169|0000:0063:001D:6016:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água|26.9375|ºC     |659            |GRANJA PIOVESAN|HUMBERTO PIOVESAN  |           26|           100|0000:0063:0021:6016:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água|26.9375|ºC     |659            |GRANJA PIOVESAN|HUMBERTO PIOVESAN  |           26|           100|0000:0063:0021:6016:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água| 27.125|ºC     |1077           |SK - JACINTO   |JACINTO JOSE ALFLEN|           37|            37|0000:006B:003B:6019:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água|27.2349|ºC     |665            |GRANJA PIQUIRI |ALFREDO MORELATTO  |            3|            97|0000:0019:001F:6016:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água|27.3125|ºC     |884            |GRANJA MIOTTO  |LUIS CARLOS MIOTTO |           32|            67|0000:0041:003E:6019:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água|27.9375|ºC     |666            |GRANJA PIQUIRI |ALFREDO MORELATTO  |            3|            97|0000:0072:002A:6019:4883:4E45|FRENTE           |04-2025|
01/04/2025 00:00:00|Temperatura da Água| 28.125|ºC     |659            |GRANJA PIOVESAN|HUMBERTO PIOVESAN  |           26|           100|0000:000C:003D:6019:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água| 28.125|ºC     |659            |GRANJA PIOVESAN|HUMBERTO PIOVESAN  |           26|           100|0000:000C:003D:6019:4883:4E45|FUNDO            |04-2025|
01/04/2025 00:00:00|Temperatura da Água|28.4375|ºC     |1037           |GRANJA LUDEWIG |DALTON AURI LUDEWIG|           11|            45|0000:0028:003D:6019:4883:4E45|FUNDO            |04-2025|
*/

-- Segmento 1: Visualizar tipos de sensores
-- View 1: Visualizar tipos de sensores
CREATE VIEW vw_event_tipos AS
SELECT DISTINCT tipo_de_evento
FROM dados_sensores
ORDER BY tipo_de_evento;

/* Results of vw_event_tipos:
tipo_de_evento         |
-----------------------+
Consumo de Eletricidade|
Consumo de ração       |
Consumo de Água        |
Luminosidade           |
Temperatura Ambiente   |
Temperatura da Cama    |
Temperatura da Água    |
Umidade                |
Velocidade do Vento    |
*/

/*
List of tipo_de_evento values:
Consumo de Eletricidade, Consumo de ração, Consumo de Água, Luminosidade, Temperatura Ambiente, Temperatura da Cama, Temperatura da Água, Umidade, Velocidade do Vento
*/

-- Segmento 2: Valores Diários por idade de vida em cada aviario em cada segmento do aviario
-- View: Temperatura da Água

-- Adicionando uma coluna de segmento de idade à tabela dados_sensores
ALTER TABLE dados_sensores ADD COLUMN age_segment VARCHAR(20);

-- Atualizando a coluna com os valores apropriados baseados na idade do lote
UPDATE dados_sensores
SET age_segment = CASE 
    WHEN idade_do_lote BETWEEN 0 AND 7 THEN '1 - Pré-Inicial'
    WHEN idade_do_lote BETWEEN 8 AND 19 THEN '2 - Inicial 1'
    WHEN idade_do_lote BETWEEN 20 AND 28 THEN '3 - Inicial 2'
    WHEN idade_do_lote BETWEEN 29 AND 35 THEN '4 - Crescimento'
    WHEN idade_do_lote > 35 THEN '5 - Abate'
    ELSE NULL
END
WHERE idade_do_lote IS NOT NULL;

CREATE VIEW vw_daily_wtemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura da Água'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Temperatura Ambiente
CREATE VIEW vw_daily_atemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor, 
    idade_do_lote,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura Ambiente'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Temperatura da Cama
CREATE VIEW vw_daily_btemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura da Cama'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Umidade
CREATE VIEW vw_daily_humidity AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS humidity_max,
    MIN(valor) AS humidity_min,
    AVG(valor) AS humidity_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Umidade'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Luminosidade
CREATE VIEW vw_daily_light AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS light_max,
    MIN(valor) AS light_min,
    AVG(valor) AS light_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Luminosidade'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Consumo de Eletricidade
CREATE VIEW vw_daily_electricity AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS electricity_max,
    MIN(valor) AS electricity_min,
    AVG(valor) AS electricity_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de Eletricidade'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Consumo de ração
CREATE VIEW vw_daily_feed AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS feed_max,
    MIN(valor) AS feed_min,
    AVG(valor) AS feed_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de ração'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Consumo de Água
CREATE VIEW vw_daily_water AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS water_max,
    MIN(valor) AS water_min,
    AVG(valor) AS water_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de Água'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- View: Velocidade do Vento
CREATE VIEW vw_daily_wind AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    idade_do_lote,
    MAX(valor) AS wind_max,
    MIN(valor) AS wind_min,
    AVG(valor) AS wind_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Velocidade do Vento'
GROUP BY nome_do_aviario, posicao_do_sensor, idade_do_lote
ORDER BY nome_do_aviario, posicao_do_sensor, idade_do_lote;

-- Segmento 3: Estatísticas de temperatura por segmento de idade, aviário e posição do sensor
CREATE VIEW vw_age_segment_wtemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura da Água'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_atemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura Ambiente'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_btemp AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS temp_max,
    MIN(valor) AS temp_min,
    AVG(valor) AS temp_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Temperatura da Cama'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_humidity AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS humidity_max,
    MIN(valor) AS humidity_min,
    AVG(valor) AS humidity_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Umidade'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_light AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS light_max,
    MIN(valor) AS light_min,
    AVG(valor) AS light_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Luminosidade'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_electricity AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS electricity_max
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de Eletricidade'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_feed AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS feed_max,
    MIN(valor) AS feed_min,
    AVG(valor) AS feed_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de ração'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
HAVING feed_max < 20000
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_water AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS water_max,
    MIN(valor) AS water_min,
    AVG(valor) AS water_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Consumo de Água'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

CREATE VIEW vw_age_segment_wind AS
SELECT 
    nome_do_aviario,
    posicao_do_sensor,
    age_segment,
    MAX(valor) AS wind_max,
    MIN(valor) AS wind_min,
    AVG(valor) AS wind_avg
FROM dados_sensores
WHERE tipo_de_evento = 'Velocidade do Vento'
GROUP BY nome_do_aviario, posicao_do_sensor, age_segment
ORDER BY nome_do_aviario, posicao_do_sensor, age_segment;

-- Segmento 4: Agrupe a soma de valores por age_segment e por aviario
-- temperatura ambiente

CREATE VIEW vw_report_atemp_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(temp_avg) as amb_temp
FROM
	vw_age_segment_atemp
WHERE
	temp_avg > 0
	and posicao_do_sensor <> 'EXTERNO'
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Temperatura da cama do aviário

CREATE VIEW vw_report_btemp_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(temp_avg) as bed_temp
FROM
	vw_age_segment_btemp
WHERE
	temp_avg > 0
	and posicao_do_sensor <> 'EXTERNO'
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Consumo de eletricidade

CREATE VIEW vw_report_electricity_by_days AS
SELECT
    nome_do_aviario as aviario,
    age_segment as feed_phase,
    electricity_max as eletricidade,
    CASE 
        WHEN age_segment = '1 - Pré-Inicial' THEN AVG(electricity_max) * 7  -- 0-7 days (7 days)
        WHEN age_segment = '2 - Inicial 1' THEN AVG(electricity_max) * 12   -- 8-19 days (12 days) 
        WHEN age_segment = '3 - Inicial 2' THEN AVG(electricity_max) * 9    -- 20-28 days (9 days)
        WHEN age_segment = '4 - Crescimento' THEN AVG(electricity_max) * 7  -- 29-35 days (7 days)
        WHEN age_segment = '5 - Abate' THEN AVG(electricity_max) * 11       -- >35 days (assuming 11 days)
    END AS total_electricity_by_days
FROM
    vw_age_segment_electricity
WHERE
	electricity_max > 0
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
    nome_do_aviario ASC,
    age_segment ASC;

-- Consumo de ração

CREATE VIEW vw_report_feed_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	feed_max as consumo_racao,
	CASE
		WHEN age_segment = '1 - Pré-Inicial' THEN AVG(feed_max) * 7
		-- 0-7 days (7 days)
		WHEN age_segment = '2 - Inicial 1' THEN AVG(feed_max) * 12
		-- 8-19 days (12 days) 
		WHEN age_segment = '3 - Inicial 2' THEN AVG(feed_max) * 9
		-- 20-28 days (9 days)
		WHEN age_segment = '4 - Crescimento' THEN AVG(feed_max) * 7
		-- 29-35 days (7 days)
		WHEN age_segment = '5 - Abate' THEN AVG(feed_max) * 11
		-- >35 days (assuming 11 days)
	END AS total_feed_by_days
FROM
	vw_age_segment_feed
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Umidade relativa dentro do aviário
CREATE VIEW vw_report_humidity_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(humidity_avg) as umidade
FROM
	vw_age_segment_humidity
WHERE
	humidity_avg > 0
	and posicao_do_sensor <> 'EXTERNO'
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Luminosidade dentro do aviario

CREATE VIEW vw_report_light_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(light_avg) as light
FROM
	vw_age_segment_light
WHERE
	light_avg > 0
	and posicao_do_sensor <> 'EXTERNO'
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Consumo de água

CREATE VIEW vw_report_water_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	water_max as consumo_agua,
	CASE
		WHEN age_segment = '1 - Pré-Inicial' THEN AVG(water_max) * 7
		-- 0-7 days (7 days)
		WHEN age_segment = '2 - Inicial 1' THEN AVG(water_max) * 12
		-- 8-19 days (12 days) 
		WHEN age_segment = '3 - Inicial 2' THEN AVG(water_max) * 9
		-- 20-28 days (9 days)
		WHEN age_segment = '4 - Crescimento' THEN AVG(water_max) * 7
		-- 29-35 days (7 days)
		WHEN age_segment = '5 - Abate' THEN AVG(water_max) * 11
		-- >35 days (assuming 11 days)
	END AS total_water_by_days
FROM
	vw_age_segment_water
WHERE
	water_max >0
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- velocidade do vento

CREATE VIEW vw_report_wind_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(wind_avg) as vel_vento
FROM
	vw_age_segment_wind
WHERE
	wind_avg <10
	and
	wind_avg > 0
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Temperatura da Água

CREATE VIEW vw_report_wtemp_by_days AS
SELECT
	nome_do_aviario as aviario,
	age_segment as feed_phase,
	AVG(temp_avg) as temp_agua
FROM
	vw_age_segment_wtemp
WHERE
	temp_avg > 0
GROUP BY
	nome_do_aviario,
	age_segment
ORDER BY
	nome_do_aviario ASC,
	age_segment ASC;

-- Segmento 5: Relatório combinado
-- Criação da tabela ambiencia_consumo com os dados combinados de todas as views
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
    total_water_by_days as consumo_agua,
    total_electricity_by_days as eletricidade,
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
