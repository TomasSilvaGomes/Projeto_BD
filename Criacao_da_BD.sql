CREATE DATABASE projeto;
USE projeto;



CREATE TABLE condutores
(
  cartao_cidadao INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  carta_conducao VARCHAR(12) NOT NULL,
  data_inicio DATE NOT NULL,
  PRIMARY KEY (cartao_cidadao)
);

CREATE TABLE autocarros
(
  matricula CHAR(8) NOT NULL,
  capacidade_sentados INT NOT NULL,
  capacida_pe INT NOT NULL,
  combustivel VARCHAR(10) NOT NULL,
  marca VARCHAR(10) NOT NULL,
  modelo VARCHAR(20) NOT NULL,
  idade INT NOT NULL,
  cartao_cidadao INT NOT NULL,
  PRIMARY KEY (matricula),
  FOREIGN KEY (cartao_cidadao) REFERENCES condutores(cartao_cidadao)
);

CREATE TABLE rotas
(
  linha_id VARCHAR(20) NOT NULL,
  paragem_inicial VARCHAR(20) NOT NULL,
  paragem_final VARCHAR(20) NOT NULL,
  PRIMARY KEY (linha_id)
);

CREATE TABLE rotas_autocarros
(
  linha_id VARCHAR(20) NOT NULL,
  matricula CHAR(8) NOT NULL,
  PRIMARY KEY (linha_id, matricula),
  FOREIGN KEY (linha_id) REFERENCES rotas(linha_id),
  FOREIGN KEY (matricula) REFERENCES autocarros(matricula)
);

CREATE TABLE paragens
(
  paragem_id INT NOT NULL,
  nome VARCHAR(20) NOT NULL,
  PRIMARY KEY (paragem_id)
);

CREATE TABLE rotas_paragens
(
  paragem_id INT NOT NULL,
  linha_id INT NOT NULL,
  PRIMARY KEY (paragem_id, linha_id),
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id),
  FOREIGN KEY (linha_id) REFERENCES rotas(linha_id)
);

CREATE TABLE pessoas_paragem
(
  timestamp DATE NOT NULL,
  quantidade_pessoas INT NOT NULL,
  paragem_id INT NOT NULL,
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id)
);

CREATE TABLE dados_ambientais
(
  timestamp DATE NOT NULL,
  temperatura FLOAT NOT NULL,
  co2 INT NOT NULL,
  co FLOAT NOT NULL,
  no2 INT NOT NULL,
  o3 INT NOT NULL,
  pm10 INT NOT NULL,
  humidade INT NOT NULL,
  paragem_id INT NOT NULL,
  PRIMARY KEY (paragem_id),
  FOREIGN KEY (paragem_id) REFERENCES paragens(paragem_id)
);

CREATE TABLE ruas
(
  rua_id INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  zona INT NOT NULL,
  local INT NOT NULL,
  PRIMARY KEY (rua_id)
);

CREATE TABLE segmentos
(
  segmento_id INT NOT NULL,
  rua_id INT NOT NULL,
  PRIMARY KEY (segmento_id),
  FOREIGN KEY (rua_id) REFERENCES ruas(rua_id)
);

CREATE TABLE veiculos
(
  matricula_veiculo CHAR(8) NOT NULL,
  marca INT NOT NULL,
  PRIMARY KEY (matricula_veiculo)
);

CREATE TABLE velocidades
(
  tipo INT NOT NULL,
  hora_registo DATE NOT NULL,
  velocidades INT NOT NULL,
  matricula_veiculo CHAR(8) NOT NULL,
  matricula CHAR(8) NOT NULL,
  segmento_id INT NOT NULL,
  PRIMARY KEY (matricula_veiculo, matricula),
  FOREIGN KEY (matricula_veiculo) REFERENCES veiculos(matricula_veiculo),
  FOREIGN KEY (matricula) REFERENCES autocarros(matricula),
  FOREIGN KEY (segmento_id) REFERENCES segmentos(segmento_id)
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
  lugar_id INT NOT NULL,
  ocupaçao 3 NOT NULL,
  estacionamento_id INT NOT NULL,
  PRIMARY KEY (lugar_id),
  FOREIGN KEY (estacionamento_id) REFERENCES estacionamento(estacionamento_id)
);