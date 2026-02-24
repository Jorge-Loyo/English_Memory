-- English Memory Statistics Database Schema
-- Version: 1.4.0

-- Historial de prácticas
CREATE TABLE IF NOT EXISTS practicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra TEXT NOT NULL,
    modo TEXT NOT NULL CHECK(modo IN ('ingles_espanol', 'espanol_ingles')),
    correcta BOOLEAN NOT NULL,
    respuesta_usuario TEXT,
    tiempo_respuesta INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Progreso por palabra
CREATE TABLE IF NOT EXISTS progreso_palabras (
    palabra TEXT PRIMARY KEY,
    veces_vista INTEGER DEFAULT 0,
    veces_correcta INTEGER DEFAULT 0,
    veces_incorrecta INTEGER DEFAULT 0,
    ultima_practica TIMESTAMP,
    nivel_dominio INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Estadísticas diarias
CREATE TABLE IF NOT EXISTS estadisticas_diarias (
    fecha DATE PRIMARY KEY,
    palabras_practicadas INTEGER DEFAULT 0,
    practicas_totales INTEGER DEFAULT 0,
    practicas_correctas INTEGER DEFAULT 0,
    tiempo_total INTEGER DEFAULT 0
);

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_practicas_palabra ON practicas(palabra);
CREATE INDEX IF NOT EXISTS idx_practicas_fecha ON practicas(fecha);
CREATE INDEX IF NOT EXISTS idx_practicas_correcta ON practicas(correcta);
CREATE INDEX IF NOT EXISTS idx_estadisticas_fecha ON estadisticas_diarias(fecha);
