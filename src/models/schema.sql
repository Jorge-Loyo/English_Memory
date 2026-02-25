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

-- Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    color TEXT
);

-- Relación palabra-categoría
CREATE TABLE IF NOT EXISTS palabra_categoria (
    palabra TEXT NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (palabra, categoria_id)
);

-- Backups
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruta TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo TEXT CHECK(tipo IN ('automatico', 'manual')),
    tamanio INTEGER
);

-- Configuración
CREATE TABLE IF NOT EXISTS configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT,
    tipo TEXT CHECK(tipo IN ('string', 'integer', 'boolean', 'json'))
);

-- Índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_practicas_palabra ON practicas(palabra);
CREATE INDEX IF NOT EXISTS idx_practicas_fecha ON practicas(fecha);
CREATE INDEX IF NOT EXISTS idx_practicas_correcta ON practicas(correcta);
CREATE INDEX IF NOT EXISTS idx_estadisticas_fecha ON estadisticas_diarias(fecha);
CREATE INDEX IF NOT EXISTS idx_palabra_categoria ON palabra_categoria(palabra);
