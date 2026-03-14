CREATE DATABASE IF NOT EXISTS ao_smith_monitoring;
USE ao_smith_monitoring;

CREATE TABLE IF NOT EXISTS stations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    station_code VARCHAR(20) UNIQUE NOT NULL,
    station_name VARCHAR(120) NOT NULL,
    line_name VARCHAR(50) NOT NULL DEFAULT 'LINE 1',
    cycle_time_set INT NOT NULL DEFAULT 0,
    target_batches INT NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS delay_reasons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(40) UNIQUE NOT NULL,
    reason_name VARCHAR(120) NOT NULL,
    reason_group VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS batch_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    station_id INT NOT NULL,
    batch_no VARCHAR(50) NOT NULL,
    model_name VARCHAR(120),
    started_at DATETIME NOT NULL,
    completed_at DATETIME NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'completed',
    CONSTRAINT fk_batch_station FOREIGN KEY (station_id) REFERENCES stations(id)
);

CREATE TABLE IF NOT EXISTS delay_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    station_id INT NOT NULL,
    reason_id INT NOT NULL,
    started_at DATETIME NOT NULL,
    ended_at DATETIME NOT NULL,
    remarks VARCHAR(255),
    CONSTRAINT fk_delay_station FOREIGN KEY (station_id) REFERENCES stations(id),
    CONSTRAINT fk_delay_reason FOREIGN KEY (reason_id) REFERENCES delay_reasons(id)
);
