CREATE DATABASE Projeto;
USE	Projeto


CREATE TABLE condutores
(
  idc INT NOT NULL,
  nome VARCHAR(100) NOT NULL,  -- Nome do condutor como texto
  carta INT NOT NULL,  -- Número da carta de condução (inteiro)
  data_inicio DATE NOT NULL,  -- Data de início como data
  PRIMARY KEY (idc)
);

CREATE TABLE paragens
(
  localizacao INT NOT NULL,  -- Localização (inteiro, como um código ou referência geográfica)
  idp INT NOT NULL,  -- Identificador da paragem (inteiro)
  tipo INT NOT NULL,  -- Tipo da paragem (inteiro)
  PRIMARY KEY (idp)
);

CREATE TABLE rotas
(
  idr INT NOT NULL,  -- Identificador da rota (inteiro)
  nome VARCHAR(100) NOT NULL,  -- Nome da rota (texto)
  PRIMARY KEY (idr)
);

CREATE TABLE ruas
(
  idr INT NOT NULL,  -- Identificador da rua (inteiro)
  nome VARCHAR(100) NOT NULL,  -- Nome da rua (texto)
  PRIMARY KEY (idr)
);

CREATE TABLE segmento
(
  idsegmento INT NOT NULL,  -- Identificador do segmento (inteiro)
  tamanho INT NOT NULL,  -- Tamanho do segmento em metros (inteiro)
  n_faixas INT NOT NULL,  -- Número de faixas de trânsito (inteiro)
  idr INT NOT NULL,  -- Identificador da rua associada (inteiro)
  PRIMARY KEY (idsegmento),
  FOREIGN KEY (idr) REFERENCES ruas(idr)
);

CREATE TABLE veiculo
(
  matricula INT NOT NULL,  -- Matricula do veículo (inteiro)
  tipo INT NOT NULL,  -- Tipo de veículo (inteiro, por exemplo, 1 para autocarro, 2 para carro)
  velocidade INT NOT NULL,  -- Velocidade máxima (inteiro)
  PRIMARY KEY (matricula)
);

CREATE TABLE estacionamento
(
  ide INT NOT NULL,  -- Identificador do estacionamento (inteiro)
  capacidade INT NOT NULL,  -- Capacidade do estacionamento (inteiro)
  tipo INT NOT NULL,  -- Tipo de estacionamento (inteiro)
  PRIMARY KEY (ide)
);

CREATE TABLE lugar
(
  idl INT NOT NULL,  -- Identificador do lugar de estacionamento (inteiro)
  estado INT NOT NULL,  -- Estado do lugar (0 para ocupado, 1 para livre)
  ide INT NOT NULL,  -- Identificador do estacionamento (inteiro)
  PRIMARY KEY (idl),
  FOREIGN KEY (ide) REFERENCES estacionamento(ide)
);

CREATE TABLE possui
(
  idr INT NOT NULL,  -- Identificador da rota (inteiro)
  idp INT NOT NULL,  -- Identificador da paragem (inteiro)
  PRIMARY KEY (idr, idp),
  FOREIGN KEY (idr) REFERENCES rotas(idr),
  FOREIGN KEY (idp) REFERENCES paragens(idp)
);

CREATE TABLE circula
(
  matricula INT NOT NULL,  -- Matricula do veículo (inteiro)
  idsegmento INT NOT NULL,  -- Identificador do segmento (inteiro)
  PRIMARY KEY (matricula, idsegmento),
  FOREIGN KEY (matricula) REFERENCES veiculo(matricula),
  FOREIGN KEY (idsegmento) REFERENCES segmento(idsegmento)
);

CREATE TABLE sensor
(
  ids INT NOT NULL,  -- Identificador do sensor (inteiro)
  humidade INT NOT NULL,  -- Humidade (%) (inteiro)
  temperatura INT NOT NULL,  -- Temperatura (em graus Celsius) (inteiro)
  concetracao_CO2 INT NOT NULL,  -- Concentração de CO2 (em ppm) (inteiro)
  concetracao_CO INT NOT NULL,  -- Concentração de CO (em ppm) (inteiro)
  concetracao_NO2 INT NOT NULL,  -- Concentração de NO2 (em ppm) (inteiro)
  O3 INT NOT NULL,  -- Concentração de O3 (em ppb) (inteiro)
  PM10 INT NOT NULL,  -- Concentração de PM10 (em µg/m³) (inteiro)
  n_pessoas INT NOT NULL,  -- Número de pessoas detectadas (inteiro)
  idp INT NOT NULL,  -- Identificador da paragem (inteiro)
  PRIMARY KEY (ids),
  FOREIGN KEY (idp) REFERENCES paragens(idp)
);

CREATE TABLE autocarro
(
  matricula INT NOT NULL,  -- Matricula do autocarro (inteiro)
  tipo INT NOT NULL,  -- Tipo de autocarro (inteiro, exemplo: 1 para autocarro, 2 para minibus)
  capacidade_pe INT NOT NULL,  -- Capacidade para pé (inteiro)
  capacidade_sentado INT NOT NULL,  -- Capacidade sentada (inteiro)
  ids INT NOT NULL,  -- Identificador do sensor (inteiro)
  PRIMARY KEY (matricula),
  FOREIGN KEY (ids) REFERENCES sensor(ids)
);

CREATE TABLE conduz
(
  idc INT NOT NULL,  -- Identificador do condutor (inteiro)
  matricula INT NOT NULL,  -- Matricula do autocarro (inteiro)
  PRIMARY KEY (idc, matricula),
  FOREIGN KEY (idc) REFERENCES condutores(idc),
  FOREIGN KEY (matricula) REFERENCES autocarro(matricula)
);

CREATE TABLE realiza
(
  matricula INT NOT NULL,  -- Matricula do autocarro (inteiro)
  idr INT NOT NULL,  -- Identificador da rota (inteiro)
  PRIMARY KEY (matricula, idr),
  FOREIGN KEY (matricula) REFERENCES autocarro(matricula),
  FOREIGN KEY (idr) REFERENCES rotas(idr)
);

--Inserir dados na tabela condutores
INSERT INTO condutores (idc, nome, carta, data_inicio) VALUES
(1, 'João Silva', 123456, '2005-10-5'),
(2, 'Maria Pereira', 654321, '2005-10-5'),
(3, 'Carlos Souza', 112233, '2005-10-5');

-- Inserir dados na tabela paragens
INSERT INTO paragens (localizacao, idp, tipo) VALUES
(1001, 1, 1),
(1002, 2, 2),
(1003, 3, 1);

-- Inserir dados na tabela rotas
INSERT INTO rotas (idr, nome) VALUES
(1, 'Rota 1'),
(2, 'Rota 2'),
(3, 'Rota 3');

-- Inserir dados na tabela ruas
INSERT INTO ruas (idr, nome) VALUES
(1, 'Rua A'),
(2, 'Rua B'),
(3, 'Rua C');

-- Inserir dados na tabela segmento
INSERT INTO segmento (idsegmento, tamanho, n_faixas, idr) VALUES
(1, 500, 2, 1),
(2, 700, 3, 2),
(3, 600, 4, 3);

-- Inserir dados na tabela veiculo
INSERT INTO veiculo (matricula, tipo, velocidade) VALUES
(101, 1, 80),
(102, 2, 60),
(103, 1, 90);

-- Inserir dados na tabela estacionamento
INSERT INTO estacionamento (ide, capacidade, tipo) VALUES
(1, 50, 1),
(2, 30, 2),
(3, 20, 1);

-- Inserir dados na tabela lugar
INSERT INTO lugar (idl, estado, ide) VALUES
(1, 0, 1),
(2, 1, 1),
(3, 0, 2);

-- Inserir dados na tabela possui
INSERT INTO possui (idr, idp) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Inserir dados na tabela circula
INSERT INTO circula (matricula, idsegmento) VALUES
(101, 1),
(102, 2),
(103, 3);

-- Inserir dados na tabela sensor
INSERT INTO sensor (ids, humidade, temperatura, concetracao_CO2, concetracao_CO, concetracao_NO2, O3, PM10, n_pessoas, idp) VALUES
(1, 70, 22, 400, 100, 50, 25, 20, 10, 1),
(2, 65, 19, 350, 80, 40, 20, 18, 8, 2),
(3, 75, 21, 450, 110, 55, 30, 22, 12, 3);

-- Inserir dados na tabela autocarro
INSERT INTO autocarro (matricula, tipo, capacidade_pe, capacidade_sentado, ids) VALUES
(101, 1, 10, 20, 1),
(102, 2, 15, 25, 2),
(103, 1, 12, 18, 3);

-- Inserir dados na tabela conduz
INSERT INTO conduz (idc, matricula) VALUES
(1, 101),
(2, 102),
(3, 103);

-- Inserir dados na tabela realiza
INSERT INTO realiza (matricula, idr) VALUES
(101, 1),
(102, 2),
(103, 3);
