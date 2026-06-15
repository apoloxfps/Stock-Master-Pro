# StockMaster Pro - Sistema de Gestão de Inventário

Um sistema de controle de estoque simples, rápido e com interface gráfica moderna, desenvolvido em Python aplicando os conceitos da metodologia RAD (*Rapid Application Development*).

## Sobre o Projeto

O **StockMaster Pro** foi criado para resolver o desafio de pequenos comerciantes e autônomos no gerenciamento diário de entrada e saída de mercadorias. O sistema substitui o controle manual (planilhas e cadernos) por uma interface *Single-Window* intuitiva, garantindo que todas as operações essenciais estejam a um clique de distância.

Este projeto foi desenvolvido como Atividade Avaliativa Final de Desenvolvimento Rápido de Aplicações, demonstrando na prática o uso de persistência de dados, interfaces gráficas e tratamento de exceções em Python.

## Funcionalidades

- **CRUD Completo:** Cadastro, leitura (visualização em tabela), atualização e exclusão de produtos em tempo real.
- **Interface Gráfica Premium:** Design limpo e profissional (*Flat Design*) utilizando a biblioteca nativa `Tkinter` estilizada.
- **Relatório Inteligente:** Filtro de "Alerta de Estoque Baixo" que exibe instantaneamente itens com 5 ou menos unidades.
- **Exportação de Dados:** Recurso de backup automático gerando arquivos `.json` estruturados.
- **Validação e Segurança:** Bloqueio e alertas visuais contra campos vazios, quantidades negativas ou erros de digitação (letras em campos numéricos).

## Tecnologias Utilizadas

- **[Python 3](https://www.python.org/):** Linguagem back-end do projeto.
- **Tkinter & TTK:** Módulos nativos para construção e estilização da interface gráfica.
- **SQLite3:** Banco de dados relacional embutido para armazenamento local persistente (gerando o arquivo `estoque.db`).
- **JSON:** Biblioteca utilizada para a serialização e exportação de dados estruturados.

## Como Executar na Sua Máquina

### Pré-requisitos
Você precisa ter o [Python](https://www.python.org/downloads/) instalado no seu computador. Nenhuma biblioteca externa (*pip install*) é necessária, pois o projeto usa apenas módulos nativos.

### Passos
1. Clone este repositório ou faça o download da pasta.
2. Abra o terminal (Prompt de Comando, PowerShell ou Git Bash) na pasta onde os arquivos estão localizados.
3. Execute o script principal digitando o comando:
   ```bash
   python app_estoque.py
### O sistema abrirá a interface gráfica automaticamente e criará o banco de dados estoque.db na primeira execução.
