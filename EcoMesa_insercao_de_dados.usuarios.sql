USE ecomesa;
-- tbl_tipo_usuario
INSERT INTO tbl_tipo_usuario (tipo) VALUES 
('Doador'), 
('Receptor');

-- tbl_tipo_entidade
INSERT INTO tbl_tipo_entidade (entidade) VALUES 
('Pessoa Fisica'), 
('Estabelecimento');

-- tbl_usuario
INSERT INTO tbl_usuarios (nome_usuario, email_usuario, senha_usuario, tipo_usuario, tipo_entidade) VALUES
('joao123', 'joao@email.com', '1234', 1, 1),
('maria456', 'maria@email.com', '1234', 2, 1),
('padaria_pao', 'padaria@email.com', '1234', 1, 2),
('restaurante_sol', 'sol@email.com', '1234', 1, 2),
('ana789', 'ana@email.com', '1234', 2, 1);

-- tbl_pessoa_fisica
INSERT INTO tbl_pessoa_fisica (nome_pessoa, cpf_pessoa, telefone_pessoa, endereco_pessoa, fk_usuario_pessoa) VALUES
('João Silva', '111.111.111-11', '(11)91111-1111', 'Rua A, 10', 1),
('Maria Souza', '222.222.222-22', '(11)92222-2222', 'Rua B, 20', 2),
('Ana Lima', '333.333.333-33', '(11)93333-3333', 'Rua C, 30', 5);

-- tbl_estabelecimentos
INSERT INTO tbl_estabelecimentos (nome_estabelecimento, cnpj_estabelecimento, telefone_estabelecimento, endereco_estabelecimento, fk_usuario_estabelecimento) VALUES
('Padaria Pão Quente', '11.111.111/0001-11', '(11)94444-4444', 'Av. D, 40', 3),
('Restaurante Sol', '22.222.222/0001-22', '(11)95555-5555', 'Av. E, 50', 4);