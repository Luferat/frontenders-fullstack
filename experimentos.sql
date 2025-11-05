-- Exemplos de operação do banco de dados SQLite

-- Apaga as tabelas caso elas já existam
-- Devtime → Isso não deve ser feito com o banco de dados de produção
DROP TABLE IF EXISTS pads;
DROP TABLE IF EXISTS owners;

-- Cria a tabela "owners"
CREATE TABLE owners (
	-- Chave primária
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid TEXT UNIQUE, 
	displayName TEXT,
	email TEXT UNIQUE,
	photoURL TEXT,
	createdAt t DEFAULT CURRENT_TIMESTAMP,
	lastLoginAt TIMASTAMP DEFAULT CURRENT_TIMESTAMP,
	status TEXT NOT NULL DEFAULT 'ON' CHECK (status IN ('ON', 'OFF', 'DEL')),
	-- "metadata" é reservado para uso futuro
	metadata TEXT
);

-- Cadastra alguns "owners"

-- Cria a tabela "pads"

--- Cadastra alguns "pads" para alguns "owners"





