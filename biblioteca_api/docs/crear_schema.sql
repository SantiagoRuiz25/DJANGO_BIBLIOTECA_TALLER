-- Script de creación del schema biblioteca en PostgreSQL
-- Ejecutar ANTES de las migraciones de Django

-- Crear el schema si no existe
CREATE SCHEMA IF NOT EXISTS biblioteca;

-- Establecer el schema por defecto para la sesión
SET search_path TO biblioteca;

-- Verificar
SELECT current_schema();
