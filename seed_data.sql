USE ao_smith_monitoring;

INSERT INTO stations (station_code, station_name, line_name, cycle_time_set, target_batches)
VALUES
('ST10', 'STATION 10', 'LINE 1', 45, 120),
('ST26', 'STATION 26', 'LINE 1', 52, 110)
ON DUPLICATE KEY UPDATE station_name = VALUES(station_name);

INSERT INTO delay_reasons (code, reason_name, reason_group)
VALUES
('PALLET_DELAY', 'Pallet Delayed', 'Material'),
('PLUNGER_MANUAL', 'Plunger In Manual Mode', 'Machine'),
('BATCH_CYCLE', 'Batch Cycle Time High', 'Process')
ON DUPLICATE KEY UPDATE reason_name = VALUES(reason_name);

INSERT INTO batch_logs (station_id, batch_no, model_name, started_at, completed_at, status)
SELECT s.id, 'BCH-1001', 'Model-A', NOW() - INTERVAL 8 HOUR, NOW() - INTERVAL 7 HOUR 20 MINUTE, 'completed' FROM stations s WHERE s.station_code='ST10'
UNION ALL
SELECT s.id, 'BCH-1002', 'Model-A', NOW() - INTERVAL 6 HOUR, NOW() - INTERVAL 5 HOUR 15 MINUTE, 'completed' FROM stations s WHERE s.station_code='ST10'
UNION ALL
SELECT s.id, 'BCH-2001', 'Model-B', NOW() - INTERVAL 4 HOUR, NOW() - INTERVAL 3 HOUR 10 MINUTE, 'completed' FROM stations s WHERE s.station_code='ST26';

INSERT INTO delay_logs (station_id, reason_id, started_at, ended_at, remarks)
SELECT s.id, r.id, NOW() - INTERVAL 5 HOUR, NOW() - INTERVAL 4 HOUR 40 MINUTE, 'Material not available'
FROM stations s, delay_reasons r WHERE s.station_code='ST10' AND r.code='PALLET_DELAY'
UNION ALL
SELECT s.id, r.id, NOW() - INTERVAL 3 HOUR, NOW() - INTERVAL 2 HOUR 45 MINUTE, 'Operator switched to manual'
FROM stations s, delay_reasons r WHERE s.station_code='ST10' AND r.code='PLUNGER_MANUAL'
UNION ALL
SELECT s.id, r.id, NOW() - INTERVAL 2 HOUR, NOW() - INTERVAL 1 HOUR 50 MINUTE, 'Cycle exceeded set time'
FROM stations s, delay_reasons r WHERE s.station_code='ST26' AND r.code='BATCH_CYCLE';
