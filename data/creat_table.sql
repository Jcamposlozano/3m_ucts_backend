PRAGMA foreign_keys = ON;


-- =========================================================
-- SISTEMA 3MT
-- SCRIPT DE CREACIÓN COMPLETA DE BASE DE DATOS
-- =========================================================



-- =========================================================
-- 1. JURADOS
-- =========================================================

CREATE TABLE IF NOT EXISTS jurado (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cognito_sub TEXT UNIQUE,

    nombre TEXT NOT NULL,

    email TEXT NOT NULL UNIQUE,

    tipo TEXT NOT NULL DEFAULT 'PRINCIPAL'
        CHECK (
            tipo IN (
                'PRINCIPAL',
                'DESEMPATE'
            )
        ),

    activo INTEGER NOT NULL DEFAULT 1
        CHECK (
            activo IN (0, 1)
        ),

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);



-- =========================================================
-- 2. PARTICIPANTES
-- =========================================================

CREATE TABLE IF NOT EXISTS participante (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT NOT NULL UNIQUE,

    nombre TEXT NOT NULL,

    programa_doctoral TEXT,

    titulo_presentacion TEXT NOT NULL,

    -- Campo opcional para almacenar la ruta del archivo
    -- dentro de AWS S3.
    --
    -- Ejemplo:
    -- participantes/2026/P001/foto.jpg

    imagen_s3_key TEXT NULL,

    activo INTEGER NOT NULL DEFAULT 1
        CHECK (
            activo IN (0, 1)
        ),

    -- Define si el participante aparecerá
    -- en el tarjetón de votación pública.

    habilitado_votacion_publica INTEGER
        NOT NULL DEFAULT 0
        CHECK (
            habilitado_votacion_publica
            IN (0, 1)
        ),

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);



-- =========================================================
-- 3. RUBRICAS
-- =========================================================

CREATE TABLE IF NOT EXISTS rubrica (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT NOT NULL UNIQUE,

    nombre TEXT NOT NULL,

    version INTEGER NOT NULL DEFAULT 1,

    descripcion TEXT,

    puntaje_maximo REAL NOT NULL,

    activa INTEGER NOT NULL DEFAULT 1
        CHECK (
            activa IN (0, 1)
        ),

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);



-- =========================================================
-- 4. CRITERIOS
-- =========================================================

CREATE TABLE IF NOT EXISTS criterio (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    rubrica_id INTEGER NOT NULL,

    codigo TEXT NOT NULL,

    categoria TEXT,

    titulo TEXT NOT NULL,

    descripcion TEXT,

    orden INTEGER NOT NULL,

    puntaje_minimo REAL NOT NULL
        DEFAULT 0.5,

    puntaje_maximo REAL NOT NULL
        DEFAULT 5.0,

    incremento REAL NOT NULL
        DEFAULT 0.5,

    activo INTEGER NOT NULL DEFAULT 1
        CHECK (
            activo IN (0, 1)
        ),

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (
        rubrica_id
    )
        REFERENCES rubrica(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,


    UNIQUE (
        rubrica_id,
        codigo
    ),

    UNIQUE (
        rubrica_id,
        orden
    ),

    CHECK (
        puntaje_minimo >= 0
    ),

    CHECK (
        puntaje_maximo
        >= puntaje_minimo
    ),

    CHECK (
        incremento > 0
    )
);



-- =========================================================
-- 5. EVALUACIONES
-- =========================================================

CREATE TABLE IF NOT EXISTS evaluacion (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    jurado_id INTEGER NOT NULL,

    participante_id INTEGER NOT NULL,

    rubrica_id INTEGER NOT NULL,


    estado TEXT NOT NULL DEFAULT 'PENDIENTE'
        CHECK (
            estado IN (
                'PENDIENTE',
                'EN_PROGRESO',
                'FINALIZADA',
                'ANULADA'
            )
        ),


    puntaje_total REAL,


    aspecto_positivo TEXT,

    aspecto_por_mejorar TEXT,


    -- Firma del jurado almacenada en S3

    firma_s3_key TEXT,


    -- PDF oficial generado después
    -- de completar la evaluación

    pdf_s3_key TEXT,


    -- SHA-256 del PDF

    pdf_hash TEXT,


    fecha_asignacion DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    fecha_inicio DATETIME,

    fecha_finalizacion DATETIME,


    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (
        jurado_id
    )
        REFERENCES jurado(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,


    FOREIGN KEY (
        participante_id
    )
        REFERENCES participante(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,


    FOREIGN KEY (
        rubrica_id
    )
        REFERENCES rubrica(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,


    -- Un jurado solamente puede evaluar
    -- una vez al mismo participante
    -- con la misma rúbrica.

    UNIQUE (
        jurado_id,
        participante_id,
        rubrica_id
    ),


    CHECK (
        puntaje_total IS NULL
        OR puntaje_total >= 0
    )
);



-- =========================================================
-- 6. RESPUESTAS DE EVALUACION
-- =========================================================

CREATE TABLE IF NOT EXISTS respuesta_evaluacion (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    evaluacion_id INTEGER NOT NULL,

    criterio_id INTEGER NOT NULL,

    puntaje REAL NOT NULL,


    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (
        evaluacion_id
    )
        REFERENCES evaluacion(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,


    FOREIGN KEY (
        criterio_id
    )
        REFERENCES criterio(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,


    -- Un criterio solamente puede tener
    -- una respuesta dentro de la evaluación.

    UNIQUE (
        evaluacion_id,
        criterio_id
    ),


    CHECK (
        puntaje >= 0
    )
);



-- =========================================================
-- 7. CONFIGURACION DE VOTACION PUBLICA
-- =========================================================
--
-- Solo existe un registro:
-- id = 1
--
-- Este registro controla si el público puede
-- o no registrar votos.
-- =========================================================

CREATE TABLE IF NOT EXISTS votacion_publica_config (

    id INTEGER PRIMARY KEY
        CHECK (
            id = 1
        ),

    activa INTEGER NOT NULL DEFAULT 0
        CHECK (
            activa IN (0, 1)
        ),

    fecha_apertura DATETIME NULL,

    fecha_cierre DATETIME NULL,

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);



-- =========================================================
-- 8. VOTOS DEL PUBLICO
-- =========================================================

CREATE TABLE IF NOT EXISTS voto_publico (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    participante_id INTEGER NOT NULL,

    -- Identificador temporal utilizado
    -- para intentar limitar un voto por usuario.
    --
    -- Posteriormente definiremos si este valor
    -- proviene de cookie, token, fingerprint, etc.

    identificador_votante TEXT
        NOT NULL UNIQUE,

    -- No almacenamos directamente IP
    -- ni User-Agent.
    -- Se almacenan hashes.

    ip_hash TEXT,

    user_agent_hash TEXT,


    fecha_voto DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY (
        participante_id
    )
        REFERENCES participante(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);



-- =========================================================
-- INDICES
-- =========================================================


-- ---------------------------------------------------------
-- JURADOS
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_jurado_cognito_sub
ON jurado(
    cognito_sub
);


CREATE INDEX IF NOT EXISTS
idx_jurado_email
ON jurado(
    email
);


CREATE INDEX IF NOT EXISTS
idx_jurado_tipo
ON jurado(
    tipo
);


CREATE INDEX IF NOT EXISTS
idx_jurado_activo
ON jurado(
    activo
);



-- ---------------------------------------------------------
-- PARTICIPANTES
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_participante_codigo
ON participante(
    codigo
);


CREATE INDEX IF NOT EXISTS
idx_participante_activo
ON participante(
    activo
);


CREATE INDEX IF NOT EXISTS
idx_participante_votacion_publica
ON participante(
    habilitado_votacion_publica
);



-- ---------------------------------------------------------
-- RUBRICA / CRITERIOS
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_criterio_rubrica
ON criterio(
    rubrica_id
);


CREATE INDEX IF NOT EXISTS
idx_criterio_activo
ON criterio(
    activo
);



-- ---------------------------------------------------------
-- EVALUACIONES
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_evaluacion_jurado
ON evaluacion(
    jurado_id
);


CREATE INDEX IF NOT EXISTS
idx_evaluacion_participante
ON evaluacion(
    participante_id
);


CREATE INDEX IF NOT EXISTS
idx_evaluacion_rubrica
ON evaluacion(
    rubrica_id
);


CREATE INDEX IF NOT EXISTS
idx_evaluacion_estado
ON evaluacion(
    estado
);


CREATE INDEX IF NOT EXISTS
idx_evaluacion_jurado_participante
ON evaluacion(
    jurado_id,
    participante_id
);



-- ---------------------------------------------------------
-- RESPUESTAS
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_respuesta_evaluacion
ON respuesta_evaluacion(
    evaluacion_id
);


CREATE INDEX IF NOT EXISTS
idx_respuesta_criterio
ON respuesta_evaluacion(
    criterio_id
);



-- ---------------------------------------------------------
-- VOTACION PUBLICA
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS
idx_voto_participante
ON voto_publico(
    participante_id
);


CREATE INDEX IF NOT EXISTS
idx_voto_fecha
ON voto_publico(
    fecha_voto
);



-- =========================================================
-- CONFIGURACION INICIAL DE VOTACION PUBLICA
-- =========================================================
--
-- Votación inicialmente CERRADA.
-- =========================================================

INSERT OR IGNORE INTO votacion_publica_config (
    id,
    activa
)
VALUES (
    1,
    0
);



-- =========================================================
-- PRECARGA DE RUBRICA
-- =========================================================


-- =========================================================
-- 1. RUBRICA 3MT 2026
-- =========================================================

INSERT OR IGNORE INTO rubrica (

    codigo,

    nombre,

    version,

    descripcion,

    puntaje_maximo,

    activa

)
VALUES (

    'RUBRICA_3MT_2026',

    'Rúbrica de Evaluación 3MT 2026',

    1,

    'Rúbrica oficial para la evaluación de participantes del concurso 3MT.',

    30.0,

    1

);



-- =========================================================
-- 2. CRITERIOS - COMPRENSION Y CONTENIDO
-- =========================================================

INSERT OR IGNORE INTO criterio (

    rubrica_id,

    codigo,

    categoria,

    titulo,

    descripcion,

    orden,

    puntaje_minimo,

    puntaje_maximo,

    incremento,

    activo

)
VALUES

(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CC01',

    'Comprensión y contenido',

    'Motivación, contexto e importancia',

    'La presentación proporciona una motivación clara y un contexto, y resalta la importancia de la pregunta de investigación.',

    1,

    0.5,

    5.0,

    0.5,

    1
),


(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CC02',

    'Comprensión y contenido',

    'Estrategia, diseño y resultados',

    'La presentación describe claramente la estrategia/diseño de la investigación y los resultados/hallazgos (preliminares) de la investigación.',

    2,

    0.5,

    5.0,

    0.5,

    1
),


(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CC03',

    'Comprensión y contenido',

    'Resultados, conclusiones e impacto',

    'La presentación describe claramente los resultados, conclusiones y potencial impacto de la investigación.',

    3,

    0.5,

    5.0,

    0.5,

    1
);



-- =========================================================
-- 3. CRITERIOS
-- CONEXION CON LA AUDIENCIA Y COMUNICACION
-- =========================================================

INSERT OR IGNORE INTO criterio (

    rubrica_id,

    codigo,

    categoria,

    titulo,

    descripcion,

    orden,

    puntaje_minimo,

    puntaje_maximo,

    incremento,

    activo

)
VALUES

(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CA01',

    'Conexión con la audiencia y comunicación',

    'Claridad y lenguaje',

    'El discurso fue pronunciado con claridad y el lenguaje era apropiado para un público no especializado.',

    4,

    0.5,

    5.0,

    0.5,

    1
),


(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CA02',

    'Conexión con la audiencia y comunicación',

    'Apoyo visual',

    'La diapositiva de PowerPoint estaba bien definida y apoyó efectivamente la presentación.',

    5,

    0.5,

    5.0,

    0.5,

    1
),


(
    (
        SELECT id
        FROM rubrica
        WHERE codigo = 'RUBRICA_3MT_2026'
    ),

    'CA03',

    'Conexión con la audiencia y comunicación',

    'Entusiasmo y atención del público',

    'El presentador transmitió entusiasmo por su investigación, capturando y manteniendo la atención del público.',

    6,

    0.5,

    5.0,

    0.5,

    1
);



-- =========================================================
-- VALIDACION FINAL
-- =========================================================

SELECT
    'Base de datos 3MT creada correctamente'
    AS resultado;


SELECT
    id,
    codigo,
    nombre,
    activa
FROM rubrica;


SELECT
    id,
    codigo,
    categoria,
    titulo,
    orden
FROM criterio
ORDER BY orden;


SELECT
    id,
    activa,
    fecha_apertura,
    fecha_cierre
FROM votacion_publica_config;
