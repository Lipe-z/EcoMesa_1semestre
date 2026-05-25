USE ecomesa;

-- tbl_doacoes
INSERT INTO tbl_doacoes (fk_usuario_doacao, data_doacao) VALUES
(1, '2025-05-01'),
(3, '2025-05-05'),
(4, '2025-05-10'),
(1, '2025-05-15'),
(3, '2025-05-20');

-- tbl_itens_doacoes
INSERT INTO tbl_itens_doacoes (descricao_item, quantidade_item, validade_item, fk_doacao_itens) VALUES
('Arroz', '5kg', '2026-01-01', 1),
('Feijão', '3kg', '2026-02-01', 1),
('Macarrão', '2kg', '2026-03-01', 2),
('Óleo de soja', '2 litros', '2025-12-01', 3),
('Farinha de trigo', '1kg', '2025-11-01', 3),
('Leite em pó', '400g', '2025-10-01', 4),
('Açúcar', '2kg', '2026-04-01', 4),
('Sal', '1kg', '2027-01-01', 5),
('Sardinha em lata', '2 latas', '2026-06-01', 5),
('Molho de tomate', '3 unidades', '2025-09-01', 2);