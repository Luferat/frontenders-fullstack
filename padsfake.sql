-- padsfake.sql
-- Script para inserir dados fake na tabela pads para testes.
-- Execute este script no DB Browser for SQLite após criar as tabelas.
-- Assume que os owners com os UIDs especificados já existem.

-- Inserir owners fake se não existirem (usando INSERT OR IGNORE para evitar duplicatas por own_uid UNIQUE)
INSERT OR IGNORE INTO owners (own_uid, own_display_name, own_email, own_photo_url, own_created_at, own_last_login_at, own_status)
VALUES ('yzfYicMZxLM34M7CfYTPQl7Pj182', 'Usuário Teste 1', 'teste1@example.com', 'https://example.com/photo1.jpg', '2025-10-01 00:00:00', '2025-11-10 00:00:00', 'ON');

INSERT OR IGNORE INTO owners (own_uid, own_display_name, own_email, own_photo_url, own_created_at, own_last_login_at, own_status)
VALUES ('50kPEJMxfhdfk0mQHn60SnTSq192', 'Usuário Teste 2', 'teste2@example.com', 'https://example.com/photo2.jpg', '2025-09-01 00:00:00', '2025-11-11 00:00:00', 'ON');

-- Inserir 10 pads fake, com owner escolhido aleatoriamente entre os dois UIDs (via subquery)
-- Datas no passado variadas (baseado em 2025-11-12 como data atual)
INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Receita de Bolo de Chocolate', 'Ingredientes: 2 xícaras de farinha, 1 xícara de açúcar, 3 ovos. Modo: Misture tudo e asse por 30 min. Delícia!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-11 10:00:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Dicas para Viajar Barato', 'Compre passagens com antecedência, use hostels e coma street food. Aventura garantida!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-10 14:30:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Como Treinar Seu Cachorro', 'Use petiscos como recompensa, treine comandos básicos como senta e fica. Paciência é chave!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-09 09:15:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Receita de Pizza Caseira', 'Massa: farinha, água, fermento. Recheio: molho, queijo, pepperoni. Asse em forno quente.',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-08 16:45:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Melhores Filmes de Comédia', 'Recomendo "Se Beber Não Case" e "Superbad". Risadas non-stop!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-07 11:20:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Dicas de Jardinagem para Iniciantes', 'Escolha plantas resistentes, regue moderadamente e use sol adequado. Verde na casa!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-06 13:50:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Receita de Smoothie Energético', 'Banana, morango, iogurte e espinafre. Bata no liquidificador para um boost matinal.',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-05 08:30:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Histórias Engraçadas de Viagem', 'Uma vez, confundi o trem e acabei em outra cidade. Lição: leia as placas!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-04 15:10:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Como Fazer Exercícios em Casa', 'Flexões, abdominais e corrida no lugar. Sem academia necessária!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-03 17:40:00', 'ON');

INSERT INTO pads (pad_title, pad_content, pad_owner, pad_created_at, pad_status)
VALUES ('Receita de Cookies Perfeitos', 'Manteiga, açúcar, farinha e gotas de chocolate. Asse até dourar. Irresistíveis!',
        (SELECT own_id FROM owners WHERE own_uid IN ('yzfYicMZxLM34M7CfYTPQl7Pj182', '50kPEJMxfhdfk0mQHn60SnTSq192') ORDER BY RANDOM() LIMIT 1),
        '2025-11-02 12:00:00', 'ON');