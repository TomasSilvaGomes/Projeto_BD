CREATE DATABASE projeto;
USE projeto;

CREATE TABLE condutores
(
  cartao_cidadao INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  carta_conduçao VARCHAR(12) NOT NULL,
  data_inicio DATE NOT NULL,
  PRIMARY KEY (cartao_cidadao)
);

CREATE TABLE autocarros
(
  matricula CHAR(8) NOT NULL,
  capacidade_sentados INT NOT NULL,
  capacidade_pe INT NOT NULL,
  combustivel VARCHAR(10) NOT NULL,
  marca VARCHAR(10) NOT NULL,
  modelo VARCHAR(20) NOT NULL,
  idade INT NOT NULL,
  PRIMARY KEY (matricula)
);

CREATE TABLE rotas
(
  linha_id VARCHAR(20) NOT NULL,
  paragem_inicial VARCHAR(20) NOT NULL,
  paragem_final VARCHAR(20) NOT NULL,
  PRIMARY KEY (linha_id)
);

CREATE TABLE paragens
(
  paragem_id INT NOT NULL,
  nome VARCHAR(40) NOT NULL,
  PRIMARY KEY (paragem_id)
);

CREATE TABLE pessoas_paragem
(
  hora DATE NOT NULL,
  quantidade_pessoas INT NOT NULL,
  paragem_id INT NOT NULL,
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id)
);

CREATE TABLE dados_ambientais
(
  hora SMALLDATETIME NOT NULL,
  temperatura DECIMAL(5,1) NOT NULL,
  co2 INT NOT NULL,
  co DECIMAL(5,1) NOT NULL,
  no2 INT NOT NULL,
  o3 INT NOT NULL,
  pm10 INT NOT NULL,
  humidade INT NOT NULL,
  id INT NOT NULL,
  paragem_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id)
);

CREATE TABLE veiculos
(
  matricula CHAR(8) NOT NULL,
  marca VARCHAR(20) NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  PRIMARY KEY (matricula)
);

CREATE TABLE ruas
(
  rua_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  zona INT NOT NULL,
  local INT NOT NULL,
  PRIMARY KEY (rua_id)
);

CREATE TABLE estacionamento
(
  estacionamento_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  horario INT NOT NULL,
  contacto INT NOT NULL,
  capacidade INT NOT NULL,
  rua_id INT NOT NULL,
  PRIMARY KEY (estacionamento_id),
  FOREIGN KEY (rua_id) REFERENCES ruas(rua_id)
);

CREATE TABLE lugares
(
  ligar_id INT NOT NULL,
  ocupaçao BIT NOT NULL,
  estacionamento_id INT NOT NULL,
  PRIMARY KEY (ligar_id),
  FOREIGN KEY (estacionamento_id) REFERENCES estacionamento(estacionamento_id)
);

CREATE TABLE condutores_autocarros
(
  cartao_cidadao INT NOT NULL,
  matricula CHAR(8) NOT NULL,
  PRIMARY KEY (cartao_cidadao, matricula),
  FOREIGN KEY (cartao_cidadao) REFERENCES condutores(cartao_cidadao),
  FOREIGN KEY (matricula) REFERENCES autocarros(matricula)
);

CREATE TABLE rotas_autocaross
(
  matricula VARCHAR(20) NOT NULL,
  linha_id CHAR(8) NOT NULL,
  PRIMARY KEY (matricula, linha_id),
  FOREIGN KEY (matricula) REFERENCES autocarros(matricula),
  FOREIGN KEY (linha_id) REFERENCES rotas(linha_id)
);

CREATE TABLE rotas_paragens
(
  linha_id INT NOT NULL,
  paragem_id VARCHAR(20) NOT NULL,
  PRIMARY KEY (linha_id, paragem_id),
  FOREIGN KEY (linha_id) REFERENCES rotas(linha_id),
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id)
);

CREATE TABLE segmentos
(
  segmento_id INT NOT NULL,
  rua_id INT NOT NULL,
  PRIMARY KEY (segmento_id),
  FOREIGN KEY (rua_id) REFERENCES ruas(rua_id)
);

CREATE TABLE velocidades
(
  velociades INT NOT NULL,
  hora_registo SMALLDATETIME NOT NULL,
  segmento_id INT NOT NULL,
  matricula CHAR(8) NOT NULL,
  FOREIGN KEY (segmento_id) REFERENCES segmentos(segmento_id),
  FOREIGN KEY (matricula) REFERENCES veiculos(matricula)
);