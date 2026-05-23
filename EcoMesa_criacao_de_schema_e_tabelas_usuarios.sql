CREATE DATABASE IF NOT EXISTS ecomesa;
USE ecomesa;

CREATE TABLE tbl_tipo_usuario (
id_tipo INT AUTO_INCREMENT PRIMARY KEY,
tipo VARCHAR(50) NOT NULL
);

CREATE TABLE tbl_tipo_entidade (
id_entidade INT AUTO_INCREMENT PRIMARY KEY,
entidade VARCHAR(50) NOT NULL
);

CREATE TABLE tbl_usuarios (
id_usuario INT AUTO_INCREMENT PRIMARY KEY,
nome_usuario VARCHAR(100) NOT NULL,
email_usuario VARCHAR(100) NOT NULL UNIQUE,
senha_usuario VARCHAR(100) NOT NULL,
tipo_usuario INT,
tipo_entidade INT
);

CREATE TABLE tbl_pessoa_fisica (
id_pessoa INT AUTO_INCREMENT PRIMARY KEY,
nome_pessoa VARCHAR(100) NOT NULL,
cpf_pessoa VARCHAR(20) NOT NULL UNIQUE,
telefone_pessoa VARCHAR(20) NOT NULL UNIQUE,
endereco_pessoa VARCHAR(250),
fk_usuario_pessoa INT
);

CREATE TABLE tbl_estabelecimentos (
id_estabelecimento INT AUTO_INCREMENT PRIMARY KEY,
nome_estabelecimento VARCHAR(100) NOT NULL,
cnpj_estabelecimento VARCHAR(20) NOT NULL UNIQUE,
telefone_estabelecimento VARCHAR(20) NOT NULL UNIQUE,
endereco_estabelecimento VARCHAR(250),
fk_usuario_estabelecimento INT
);

ALTER TABLE tbl_usuarios
ADD CONSTRAINT tipo_usuario
FOREIGN KEY (tipo_usuario)
REFERENCES tbl_tipo_usuario(id_tipo),
ADD CONSTRAINT tipo_entidade
FOREIGN KEY (tipo_entidade)
REFERENCES tbl_tipo_entidade(id_entidade);

ALTER TABLE tbl_pessoa_fisica
ADD CONSTRAINT fk_usuario_pessoa
FOREIGN KEY (fk_usuario_pessoa)
REFERENCES tbl_usuarios(id_usuario);

ALTER TABLE tbl_estabelecimentos
ADD CONSTRAINT fk_usuario_estabelecimento
FOREIGN KEY (fk_usuario_estabelecimento)
REFERENCES tbl_usuarios(id_usuario);