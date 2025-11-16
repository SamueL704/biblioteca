-- 1. Modelagem e Criação do Banco de Dados
CREATE TABLE usuarios(
	id SERIAL PRIMARY KEY,
	nome VARCHAR (100) NOT NULL,
	email VARCHAR (100)UNIQUE NOT NULL,
	senha Varchar (20) NOT NULL
);

CREATE TABLE livros(
	id SERIAL PRIMARY KEY,
	titulo VARCHAR (150) NOT NULL
);

CREATE TABLE emprestimos(
	id SERIAL PRIMARY KEY,
	livro_id INT REFERENCES livros(id),
	usuario_id INT REFERENCES usuarios(id),
	data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	status_emprestimo VARCHAR(50) NOT NULL
);

CREATE TABLE log_emprestimos(
	id SERIAL PRIMARY KEY,
	operacao varchar(15),
	emprestimo_id INT,
	status_emprestimo VARCHAR(50),
	livro_id INT,
	usuario_id INT,
	usuario VARCHAR(25) NOT NULL,
	data_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--insert into livros(titulo) values
--	(session_user);

-- 2. Implementação de Trigger de Log
CREATE OR REPLACE FUNCTION logEmprestimos()
RETURNS TRIGGER AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO log_emprestimos(operacao, emprestimo_id, status_emprestimo, livro_id, usuario_id, usuario)
		VALUES ('INSERT', NEW.id, NEW.status_emprestimo, NEW.livro_id, NEW.usuario_id, session_user);
		RETURN NEW;
	ELSIF TG_OP = 'UPDATE' THEN
		INSERT INTO log_emprestimos(operacao, emprestimo_id, status_emprestimo, livro_id, usuario_id, usuario)
		VALUES ('UPDATE', NEW.id, NEW.status_emprestimo, NEW.livro_id, NEW.usuario_id, session_user);
		RETURN NEW;
	ELSIF TG_OP = 'DELETE' THEN
		INSERT INTO log_emprestimos(operacao, emprestimo_id, status_emprestimo, livro_id, usuario_id, usuario)
		VALUES ('DELETE', OLD.id, OLD.status_emprestimo, OLD.livro_id, OLD.usuario_id, session_user);
		RETURN OLD;
	END IF;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_emprestimos
AFTER INSERT OR UPDATE OR DELETE
ON emprestimos
FOR EACH ROW
EXECUTE FUNCTION logEmprestimos();

-- 3. Criação de View Agregada
CREATE OR REPLACE VIEW lista_emprestimo AS
SELECT 
	usuarios.nome AS nome, 
	usuarios.email AS email, 
	livros.titulo AS livro, 
	emprestimos.data_emprestimo AS data_emprestimo,
	emprestimos.status_emprestimo AS status_emprestimo
FROM emprestimos
JOIN usuarios ON usuarios.id = emprestimos.usuario_id
JOIN livros ON livros.id = emprestimos.livro_id;

-- 4. Controle de Usuários e Permissões
CREATE USER dev_db WITH PASSWORD 'adm123';
CREATE USER dev_junior WITH PASSWORD 'team123';

GRANT CONNECT ON DATABASE biblioteca_db TO dev_db;
GRANT CONNECT ON DATABASE biblioteca_db TO dev_junior;

ALTER USER dev_db WITH SUPERUSER;

GRANT SELECT ON lista_emprestimo TO dev_junior;

-- Inserindo um usuário
INSERT INTO usuarios (nome, email, senha)
VALUES ('João Silva', 'joao.silva@email.com', '12345');

INSERT INTO usuarios (nome, email, senha)
VALUES ('samuel Silva', 'samuel.silva@email.com', '12345');

-- Inserindo um livro
INSERT INTO livros (titulo)
VALUES ('Dom Casmurro');

INSERT INTO livros (titulo)
VALUES ('Código Limpo');
