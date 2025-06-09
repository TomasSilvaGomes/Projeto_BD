# 📊 Cidade Inteligente - Projeto de Base de Dados

Este repositório contém o projeto desenvolvido no âmbito da Unidade Curricular de **Bases de Dados** do curso de **Inteligência Artificial e Ciência de Dados** (1.º ciclo), cujo objetivo foi modelar, implementar e interagir com uma base de dados relacionada com o conceito de cidade inteligente.

---

## 🎯 Objetivo

Este projeto simula a gestão urbana inteligente, utilizando uma base de dados relacional para representar diferentes componentes de uma cidade, como transporte público, tráfego, sensores ambientais e estacionamento.

O trabalho inclui:
- Modelação do sistema através de diagramas E-R;
- Implementação no **SQL Server Management Studio**;
- Desenvolvimento de uma **aplicação Python** com interface gráfica para interação com a base de dados.

---

## 📁 Estrutura do Projeto

### 1. Modelação da Base de Dados
- Criação do **Diagrama Entidade-Relacionamento (DER)** com duas versões (antes e depois da análise dos dados).
- Identificação das entidades principais: `Condutores`, `Autocarros`, `Rotas`, `Paragens`, `Dados Ambientais`, `Veículos`, `Segmentos`, `Estacionamentos`, entre outros.
- Normalização das tabelas até à **3ª Forma Normal (3FN)**, garantindo integridade e ausência de redundância.

### 2. Implementação no SQL Server
- Utilização da ferramenta **ERDPlus** para gerar o modelo relacional.
- Criação da estrutura da base de dados no **SQL Server Management Studio (SSMS)**.
- Importação dos dados a partir de ficheiros CSV, com validação de tipos e estrutura.

### 3. Validações e Triggers
- Restrições com `CHECK` e `UNIQUE` em colunas críticas como `cartão de cidadão`, `matrícula`, `tipo de estacionamento`, `humidade`, entre outras.
- **Triggers** criadas para:
  - Ligação entre `autocarros` e `veículos`;
  - Evitar remoção de autocarros sem rota associada;
  - Exibir mensagens de erro amigáveis para entradas inválidas.

### 4. Aplicação Python
- Interface gráfica criada com **Tkinter**.
- Conexão à base de dados via **pyodbc**, suportando operações remotas por IP.
- Organização da aplicação em **abas funcionais**:
  - `Adicionar`: Inserção de novos dados;
  - `Visualizar`: Consulta dos dados em tabela;
  - `Atualizar`: Modificação de registos;
  - `Remover`: Eliminação de dados;
  - `Informações`: Perguntas e respostas relevantes do enunciado;
  - `Desconectar`: Encerramento da sessão.

---

## 🧪 Testes e Validação

- Validação de integridade através de:
  - Chaves primárias e estrangeiras;
  - Restrições `CHECK`;
  - **Triggers** de validação automática.
- Mensagens de erro claras e dirigidas ao utilizador final.

---

## 🛠 Tecnologias Utilizadas

- **Python**: `Tkinter`, `pyodbc`
- **Microsoft SQL Server Management Studio (SSMS)**
- **ERDPlus** (modelação E-R)
- **CSV**: formato dos dados de entrada
- **SQL**: implementação relacional

---

## 📚 Referências

- [ERDPlus](https://erdplus.com/)
- [W3Schools - SQL](https://www.w3schools.com/sql/)
- [Tkinter - Python Docs](https://docs.python.org/3/library/tkinter.html)
- [pyodbc - PyPI](https://pypi.org/project/pyodbc/)
- [SSMS - Microsoft](https://learn.microsoft.com/en-us/sql/ssms/)
- [Normalização - Filipacardosoblog](https://filipacardosoblog.wordpress.com/normalizacao-de-uma-base-de-dados-tres-formas-normais/)
- [Importação CSV para SQL Server](https://support.discountasp.net/kb/a1179/how-to-import-a-csv-file-into-a-database-using-sql-server-management-studio.aspx)

---

## 👨‍💻 Autores

- Tomás Gomes – Nº 51726  
- Tiago Marques – Nº 51653  
- Tiago Riscadão – Nº 52935  

**Orientador**: Prof. Rui Cardoso  
**Data**: Janeiro de 2025
