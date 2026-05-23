USE ecomesa;

CREATE TABLE tbl_doacoes (
id_doacao INT AUTO_INCREMENT PRIMARY KEY,
fk_usuario_doacao INT,
data_doacao DATE
);

CREATE TABLE tbl_itens_doacoes (
id_item INT AUTO_INCREMENT PRIMARY KEY,
descricao_item VARCHAR(150) NOT NULL,
quantidade_item VARCHAR(20) NOT NULL,
validade_item DATE,
fk_doacao_itens INT
);

ALTER TABLE tbl_doacoes
ADD CONSTRAINT fk_usuario_doacao
FOREIGN KEY (fk_usuario_doacao)
REFERENCES tbl_usuarios(id_usuario);

ALTER TABLE tbl_itens_doacoes
ADD CONSTRAINT fk_doacao_itens
FOREIGN KEY (fk_doacao_itens)
REFERENCES tbl_doacoes(id_doacao);