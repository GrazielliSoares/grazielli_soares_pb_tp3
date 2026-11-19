# Planejamento do Projeto — TP3

## 1. Objetivo

Planejar a evolução do Sistema de Atendimento com Inteligência Artificial, desenvolvido em FastAPI, para implementar a classificação automática de intenções em chamados de suporte ao cliente.

O planejamento também estabelece o escopo preliminar dos testes de segurança que serão realizados nas próximas etapas do projeto (TP4 e TP5).

## 2. Definição do problema de classificação

O problema consiste em identificar automaticamente a intenção de um cliente a partir do texto de sua solicitação de atendimento.

- **Variável de entrada (X):** `Ticket Description`, contendo a descrição textual do chamado.
- **Variável-alvo (y):** `Ticket Type`, utilizada como representação da intenção do cliente.
- **Tipo de problema:** classificação supervisionada multiclasse.

O conjunto de dados possui 8.469 registros válidos e cinco categorias:

| Classe | Quantidade | Percentual |
|---|---:|---:|
| Refund request | 1.752 | 20,69% |
| Technical issue | 1.747 | 20,63% |
| Cancellation request | 1.695 | 20,01% |
| Product inquiry | 1.641 | 19,38% |
| Billing inquiry | 1.634 | 19,29% |

As classes apresentam distribuição relativamente equilibrada, sem predominância expressiva de uma única categoria.

A variável `Ticket Type` representa uma categoria administrativa de atendimento e será utilizada como aproximação da intenção semântica do cliente.

## 3. Algoritmo proposto

O algoritmo inicialmente selecionado é a **Regressão Logística (Logistic Regression)**.

A escolha se justifica por sua aplicação em problemas de classificação supervisionada, capacidade de trabalhar com representações vetoriais de texto e relativa facilidade de interpretação.

A implementação futura poderá utilizar `LogisticRegression`, da biblioteca scikit-learn.

O modelo deverá ser avaliado por meio de métricas como acurácia, precisão, recall, F1-score e matriz de confusão.

## 4. Representação dos textos

Será utilizado o **CountVectorizer**, da biblioteca scikit-learn, para transformar as mensagens textuais em vetores numéricos.

Essa técnica representa cada documento por contagens de termos, permitindo que o algoritmo de classificação processe as descrições dos chamados.

O fluxo proposto é:

1. Selecionar as descrições textuais válidas.
2. Separar os dados em treinamento e teste, utilizando divisão estratificada.
3. Aplicar o CountVectorizer aos textos de treinamento.
4. Treinar o classificador LogisticRegression.
5. Avaliar o desempenho com dados de teste não utilizados no treinamento.

Para evitar vazamento de informações entre treinamento e teste, a vetorização e o classificador poderão ser integrados em um `Pipeline` do scikit-learn.

## 5. Integração futura com a API

O modelo de classificação poderá ser integrado ao endpoint `POST /predict` da API FastAPI.

O endpoint deverá receber uma mensagem textual e retornar a categoria prevista, juntamente com uma estimativa de confiança quando disponibilizada pelo modelo.

A autenticação JWT, a validação dos dados de entrada, o controle de acesso aos registros e a limitação de requisições deverão ser preservados.

## 6. Planejamento dos testes de segurança — TP4 e TP5

### 6.1. Ambiente autorizado

Os testes deverão ser realizados exclusivamente em ambiente local ou em ambiente de laboratório expressamente autorizado.

**Endereço-base previsto:**

`http://127.0.0.1:8000`

**IP:** `127.0.0.1` (loopback/local)

Esse endereço representa a instância local da aplicação e não autoriza testes contra servidores públicos ou sistemas de terceiros.

### 6.2. Endpoints previstos no escopo

| Método | Endpoint | Finalidade |
|---|---|---|
| POST | `/auth/token` | Autenticação |
| GET | `/health` | Verificação de disponibilidade |
| POST | `/predict` | Classificação de chamados |
| GET | `/predictions/{prediction_id}` | Consulta de previsões com controle de acesso |

### 6.3. Controles de segurança a verificar

- Autenticação e autorização com JWT.
- Proteção contra acesso indevido a registros de outros usuários (BOLA).
- Validação de entradas e rejeição de campos não permitidos.
- Limitação de requisições com SlowAPI.
- Configuração de CORS e cabeçalhos de segurança HTTP.
- Exposição de informações sensíveis em respostas e mensagens de erro.

### 6.4. Limites dos testes

Os testes deverão utilizar dados e contas de laboratório.

Não estão autorizadas ações destrutivas, ataques de negação de serviço, exploração de serviços de terceiros ou testes fora do ambiente expressamente permitido.

A execução deverá respeitar as regras de engajamento definidas para cada etapa.

## 7. Critérios de continuidade

Para as próximas etapas do projeto, estão previstas as seguintes atividades:

- Implementar o pipeline de classificação textual.
- Avaliar o desempenho do modelo supervisionado.
- Integrar o modelo treinado à API.
- Preservar e ampliar os testes automatizados de segurança.
- Executar avaliações de segurança no ambiente autorizado.
- Documentar resultados, limitações e evidências.

## 8. Conclusão

O planejamento estabelece a Regressão Logística como algoritmo candidato e o CountVectorizer como técnica inicial de representação textual.

A proposta utiliza as cinco categorias identificadas na análise exploratória e prevê a integração futura do classificador à API FastAPI.

Também define um escopo preliminar e restrito para os testes de segurança dos próximos trabalhos, priorizando a preservação dos controles já implementados.
