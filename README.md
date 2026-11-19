# Projeto de Bloco: Sistema de Atendimento com IA

# TP1
**Aluno:** Grazielli Soares Pereira
**Disciplina:** Projeto de Bloco  
**Professor:** Tiago Xavier

---

## Objetivo do Projeto
Desenvolvimento da estrutura base de um sistema de atendimento ao cliente alimentado por Inteligência Artificial. Este projeto contempla a Análise Exploratória de Dados (EDA) do dataset *customer support Ticket Dataset* e a construção de uma API modular utilizando FastAPI com autenticação via token JWT.

---

## Estrutura do repositório

```text
meu-projeto-pb/
-- data 
    -> customer_support_tickets.csv
-- eda 
    -> eda_atendimento.ipynb
-- fastapi
   -> main.py
   -> models/
       -- schemas.py
   -> routes/
       -- auth.py
       -- health.py
       -- predict.py
   ->security/
        -- authentication.py
-- others/
       --dfd_diagram.png
-- README
    -> README.md
```

### Instalação de Dependências
1.No terminal do seu sistema operacional, instale os pacotes necessários com o seguinte comando:
pip install fastapi uvicorn python-jose passlib pydantic pandas matplotlib seaborn python-

### Execução da API
1.Navegue até a pasta da API no vscode:
cd fastapi

2.Inicie o servidor Uvicorn:
python -m uvicorn main:app --reload

3.Acesse a documentação interativa no seu navegador:
http://localhost:8000/docs
http://127.0.0.1:8000/docs

## Segurança e Modelagem (DFD / Tríade CIA)
O siagrama de fluxo de sados (DFD) do sistema está disponível em others/dfd_diagrama.png

### Aplicação da Tríade CIA aos Componentes

**Endpoint de Autenticação (POST /auth/token)**
- **Confidencialidade:** As credenciais de login trafegam protegidas por criptografia em trânsito (HTTPS/TLS) para evitar vazamentos.
- **Integridade:** As entradas de usuário e senha são validadas de forma estrita para impedir a emissão indevida de tokens.
- **Disponibilidade:** Aplicação de limites de requisição para proteger a rota contra ataques de força bruta e indisponibilidade.

**Token JWT (JSON Web Token)**
- **Confidencialidade:** A chave secreta (SECRET_KEY) é mantida apenas no servidor para impedir que terceiros criem tokens falsos.
- **Integridade:** O uso do algoritmo HS256 garante a assinatura digital do token, impedindo qualquer alteração nos dados do payload.
- **Disponibilidade:** A validação é feita de forma stateless (em memória), permitindo alto desempenho sem sobrecarregar bancos de dados.

**Endpoint de Predição (POST /predict)**
- **Confidencialidade:** Rota restrita e protegida que exige obrigatoriamente um Bearer Token válido para acesso.
- **Integridade:** Garantia de que o texto enviado pelo usuário e a resposta da predição não sejam interceptados ou modificados.
- **Disponibilidade:** Controle do volume de requisições enviadas ao modelo para evitar gargalos e manter o serviço sempre ativo.



#  (TP2)

### Objetivo do projeto

Dar continuidade ao desenvolvimento de um sistema de atendimento ao cliente com Inteligência Artificial, utilizando o dataset *Customer Support Ticket Dataset*.

O TP2 tem como objetivo aprofundar a análise exploratória dos dados, aplicar testes estatísticos e evoluir a API FastAPI, incluindo persistência em banco de dados, autenticação JWT e controles de segurança.

### Exercício 1 — Análise Exploratória de Dados (EDA)

Foi realizada a ampliação da análise exploratória desenvolvida no TP1, utilizando Python, Pandas, NumPy, Matplotlib, Seaborn e SciPy.

O notebook está localizado em:

`eda/eda_atendimento.ipynb`

A análise contempla as seguintes etapas:

1. Compreensão do problema e do dataset.
2. Inspeção inicial das variáveis numéricas, categóricas e textuais.
3. Verificação da qualidade dos dados, incluindo valores ausentes, duplicatas e inconsistências.
4. Limpeza e preparação dos dados.
5. Análise univariada com estatísticas descritivas e gráficos.
6. Análise multivariada com correlações de Spearman e testes de hipóteses.
7. Identificação de outliers pelo método IQR.
8. Documentação dos resultados e conclusões.

**Principais resultados:**

- Dataset com 8.469 registros e 17 colunas originais.
- Ausência de registros duplicados e IDs repetidos.
- Identificação de valores ausentes em campos de satisfação e resolução.
- Criação da variável `Description Length`, que representa o tamanho das descrições dos tickets.
- Correlações de Spearman próximas de zero entre idade, satisfação e tamanho das descrições.
- Identificação de 579 outliers (6,84%) na variável `Description Length`, preservados para análise.

**Testes de hipóteses:**

Foram realizados dois testes não paramétricos de Mann-Whitney, considerando nível de significância de 5%:

| Hipótese | Valor-p | Resultado |
|---|---|---|
| Diferença de satisfação entre tickets de prioridade High e Low | 0,370563 | Não rejeitamos H₀ |
| Diferença no tamanho das descrições entre canais Email e Chat | 0,572288 | Não rejeitamos H₀ |

Os testes não apresentaram evidências estatísticas suficientes de diferenças entre os grupos analisados.

### Exercício 2 — Banco de Dados SQLite e SQLModel

Foi implementada a persistência de dados da API utilizando SQLite e SQLModel.

O banco está localizado em:

`fastapi/database.db`

O script de criação e população inicial está em:

`fastapi/sqlite_database.py`

**Estrutura do banco:**

- `users`: armazena identificador, nome de usuário e hash da senha.
- `predictions`: armazena identificador, proprietário (`owner_id`), texto do chamado e categoria prevista.

Cada prediction possui uma chave estrangeira `owner_id`, que referencia o usuário responsável.

Foram cadastrados dois usuários de demonstração, `usuario1` e `usuario2`, com senhas armazenadas utilizando hash Argon2.

A aplicação utiliza SQLModel para realizar consultas e gravações no banco, sem SQL raw nas rotas da API.

**Autenticação e persistência:**

- A rota `POST /auth/token` consulta os usuários cadastrados no SQLite, verifica suas senhas e gera tokens JWT.
- A rota `POST /predict` exige autenticação e registra a previsão no banco, associando-a ao usuário autenticado.
- A chave de assinatura JWT é configurada por meio da variável de ambiente `JWT_SECRET_KEY`.

**Validação realizada:**

Foram realizados testes manuais utilizando Swagger UI, confirmando que os dois usuários conseguem autenticar-se e criar predictions vinculadas aos seus respectivos IDs.

### Instalação e execução

Instale as dependências necessárias no ambiente virtual do projeto:

```bash
pip install fastapi uvicorn python-jose python-multipart sqlmodel "pwdlib[argon2]" pandas numpy matplotlib seaborn scipy jupyter
```

Para criar e popular o banco de dados, execute a partir da raiz do projeto:

```bash
python fastapi/sqlite_database.py
```

Para iniciar a API, acesse a pasta `fastapi`:

```bash
cd fastapi
```

No PowerShell, configure uma chave JWT para a sessão atual:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Inicie a aplicação:

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs

O notebook de EDA pode ser executado no Jupyter Notebook ou no VS Code, utilizando um ambiente Python com as bibliotecas instaladas.

### Próximas etapas

Os próximos exercícios do TP2 abordarão o fortalecimento dos controles de segurança da API, incluindo validação de entradas, autorização por propriedade dos recursos, headers de segurança, CORS, rate limiting, testes automatizados e auditoria com OWASP ZAP.


### Exercício 3 — Validação de Dados com Pydantic

Foi configurado o modelo Pydantic `PredictRequest`, localizado em `fastapi/models/schemas.py`, utilizando `ConfigDict(extra="forbid")`.

Essa configuração impede que a API aceite campos adicionais que não estejam definidos no modelo esperado, fortalecendo a validação dos dados recebidos.

**Implementação:**
- Adição de `model_config = ConfigDict(extra="forbid")` ao modelo `PredictRequest`.
- Restrição das requisições de previsão ao campo `text`.
- Rejeição automática de campos não autorizados, como `owner_id`.

**Teste realizado:**

Foi enviada uma requisição à rota `POST /predict` contendo os campos `text` e `owner_id`.

A API retornou **HTTP 422 (Unprocessable Entity)**, confirmando que campos extras são rejeitados corretamente.

**Resultado:** o requisito de validação de campos extras foi atendido, impedindo que o cliente envie propriedades não previstas no modelo de entrada.



### Exercício 4 — Controle de Acesso por Ownership (BOLA)

Foi implementado um controle de autorização por propriedade (*ownership*) para prevenir vulnerabilidades do tipo BOLA (*Broken Object Level Authorization*).

**Implementação:**

- Criação da rota `GET /predictions/{prediction_id}` no arquivo `fastapi/routes/predict.py`.
- Identificação do usuário autenticado por meio do token JWT.
- Consulta das predictions no banco SQLite utilizando SQLModel.
- Verificação de que o campo `owner_id` corresponde ao ID do usuário autenticado.
- Retorno de HTTP 404 quando a prediction não existe ou pertence a outro usuário, evitando a exposição de informações privadas.

**Testes realizados:**

| Usuário autenticado | Prediction consultada | Resultado |
|---|---|---|
| usuario1 | ID 4 (própria) | HTTP 200 |
| usuario1 | ID 5 (outro usuário) | HTTP 404 |
| usuario1 | ID 9999 (inexistente) | HTTP 404 |
| usuario2 | ID 5 (própria) | HTTP 200 |
| usuario2 | ID 4 (outro usuário) | HTTP 404 |

**Resultado:** todos os testes manuais realizados pelo Swagger UI apresentaram os resultados esperados, confirmando que a rota implementada restringe o acesso aos recursos pertencentes ao usuário autenticado.



### Exercício 5 — Headers de Segurança HTTP e CORS

Foram implementados mecanismos adicionais de segurança na API FastAPI por meio de middlewares, configurados no arquivo `fastapi/main.py`.

**Headers HTTP configurados:**

- **Strict-Transport-Security (HSTS):** orienta o navegador a utilizar HTTPS em conexões futuras, quando a aplicação é acessada por HTTPS.
- **X-Frame-Options:** configurado como `DENY`, impedindo a exibição da aplicação em iframes.
- **X-Content-Type-Options:** configurado como `nosniff`, evitando a interpretação automática de tipos de conteúdo.
- **Content-Security-Policy (CSP):** estabelece restrições sobre fontes de conteúdo, reduzindo riscos de determinadas formas de injeção.

**Configuração de CORS:**

Foi utilizado o middleware `CORSMiddleware` do FastAPI, com uma lista explícita de origens permitidas, sem utilização de `allow_origins=["*"]`.

Também foram restringidos os métodos HTTP e os headers autorizados nas requisições entre origens.

**Testes realizados:**

- Verificação da presença dos quatro headers de segurança nas respostas HTTP.
- Envio de requisição CORS a partir de uma origem autorizada, com retorno HTTP 200.
- Envio de requisição CORS a partir de uma origem não autorizada, com retorno HTTP 400.

**Resultado:** os testes realizados pelo PowerShell confirmaram a configuração dos headers HTTP e a aplicação da política de CORS com origens explicitamente autorizadas.

**Observação:** o HSTS somente é aplicado pelos navegadores em conexões HTTPS válidas. Durante os testes locais em HTTP, foi verificada a presença do header na resposta.


### Exercício 6 — Rate Limiting com SlowAPI

Foi implementado um mecanismo de limitação de requisições (*rate limiting*) no endpoint de autenticação `POST /auth/token`, utilizando a biblioteca SlowAPI.

O objetivo é reduzir o risco de ataques de força bruta (*brute force*), limitando a quantidade de tentativas de autenticação realizadas por um mesmo cliente.

**Implementação:**

- Instalação e configuração da biblioteca `slowapi`.
- Criação do arquivo `fastapi/limiter.py`, responsável pela configuração do limitador.
- Identificação dos clientes pelo endereço IP.
- Aplicação do decorador `@limiter.limit("10/minute")` na rota de autenticação.
- Registro do limitador e do tratamento da exceção `RateLimitExceeded` no arquivo `fastapi/main.py`.

**Testes realizados:**

Foi executado um teste automatizado via PowerShell, enviando 11 requisições consecutivas ao endpoint de autenticação com credenciais incorretas.

**Resultados esperados e verificados:**

- Até 10 requisições dentro do limite: HTTP 401, indicando credenciais inválidas.
- Ao ultrapassar o limite: HTTP 429 (*Too Many Requests*), indicando bloqueio temporário por excesso de requisições.

**Resultado:** a API passou a limitar o número de tentativas de autenticação por cliente, adicionando uma camada de proteção contra ataques de força bruta.

**Observação:** a implementação utiliza armazenamento em memória, adequado para o ambiente de desenvolvimento. Em produção, recomenda-se um armazenamento compartilhado, como Redis, para ambientes com múltiplos processos ou servidores.


### Exercício 7 — Análise Passiva de Segurança com OWASP ZAP

Foi realizada uma análise passiva de segurança na API FastAPI utilizando o **OWASP ZAP 2.17.0**, com a aplicação executada localmente em `http://127.0.0.1:8000`.

O objetivo foi identificar possíveis falhas de configuração e vulnerabilidades de segurança, sem realizar ataques ativos.

O relatório foi exportado em formato HTML, em 20/10/2026.

**Resumo dos resultados:**

| Severidade | Quantidade de tipos de alerta |
|---|---:|
| Alta | 0 |
| Média | 2 |
| Baixa | 6 |
| Informativa | 6 |
| **Total** | **14** |

A análise também capturou tráfego de serviços externos do navegador. Por isso, os findings foram classificados conforme sua relação com a API desenvolvida.

#### Finding 1 — Sub Resource Integrity Attribute Missing

**7.1. Finding:** Sub Resource Integrity Attribute Missing.

**7.2. Severidade:** Média.

**7.3. Confiança:** Alta.

**7.4. URL afetada:** `http://127.0.0.1:8000/docs`

**7.5. O que foi detectado:**

O OWASP ZAP identificou que a página de documentação Swagger UI utiliza recursos externos sem o atributo HTML `integrity`.

A evidência registrada inclui uma referência ao arquivo `swagger-ui.css`, hospedado no CDN jsDelivr.

**7.6. Por que é um problema:**

A ausência de Subresource Integrity (SRI) impede que o navegador verifique, por meio de um hash esperado, se o conteúdo externo foi alterado.

Caso o servidor externo seja comprometido, existe o risco de fornecimento de conteúdo malicioso à página de documentação.

**7.7. Correção realizada:**

Nenhuma correção específica foi implementada nesta etapa. A aplicação já possui headers de segurança configurados, incluindo Content-Security-Policy, mas isso não elimina automaticamente o alerta de SRI.

Como melhoria futura, recomenda-se hospedar os arquivos JavaScript e CSS do Swagger localmente ou utilizar referências externas com hashes de integridade válidos.

**7.8. Validação:**

O finding foi confirmado no relatório HTML exportado pelo OWASP ZAP. Não foi executada uma nova varredura após uma correção específica, portanto o alerta permanece pendente de validação de remediação.

**7.9. Risco aceito:**

O risco foi aceito provisoriamente para o ambiente acadêmico de desenvolvimento local. A exposição identificada está associada à interface de documentação Swagger UI.

Essa aceitação não significa que a vulnerabilidade foi corrigida. Antes de disponibilizar a aplicação em produção, a dependência de recursos externos deverá ser revisada.

#### Finding 2 — Content Security Policy (CSP) Header Not Set

**7.1. Finding:** Content Security Policy (CSP) Header Not Set.

**7.2. Severidade:** Média.

**7.3. Confiança:** Alta.

**7.4. URL afetada:**

`https://ogads-pa.clients6.google.com/$rpc/google.internal.onegoogle.asyncdata.v1.AsyncDataService/GetAsyncData`

**7.5. O que foi detectado:**

O ZAP identificou uma resposta HTTP de um serviço externo do Google sem o header Content-Security-Policy.

A requisição foi capturada durante a navegação utilizada na análise passiva.

**7.6. Por que é um problema:**

A ausência de uma política CSP pode reduzir as proteções oferecidas pelo navegador contra determinadas formas de injeção de conteúdo e execução de scripts não autorizados.

Entretanto, a ocorrência identificada não pertence à API desenvolvida neste projeto.

**7.7. Correção realizada:**

Não foi realizada alteração no serviço externo, pois ele não está sob controle do projeto.

A API FastAPI já possui middleware responsável pela inclusão do header Content-Security-Policy, implementado no Exercício 5.

**7.8. Validação:**

Foi verificado no relatório que a URL afetada pertence a um domínio externo, diferente do endereço local da API.

A presença do header CSP nas respostas da API também havia sido verificada anteriormente por meio de testes HTTP.

**7.9. Risco aceito:**

O finding foi classificado como fora do escopo da aplicação, pois pertence a um serviço de terceiros. Não representa uma correção pendente no código da API.

#### Conclusão

O scan passivo permitiu identificar possíveis problemas de segurança e analisar sua relevância para o projeto.

Entre os dois findings de severidade média, um pertence à documentação Swagger UI da aplicação e permanece como risco aceito provisoriamente. O outro está associado a um serviço externo e foi classificado como fora do escopo.

Não foram identificados findings de severidade alta no tráfego analisado.

**Limitação da análise:** o relatório registrou três endpoints GET da API local. As rotas autenticadas não foram integralmente avaliadas nessa captura. Portanto, a ausência de novos alertas não garante a inexistência de outras vulnerabilidades.



### Exercício 8 — Testes Automatizados de Segurança com Pytest

Foram implementados três testes automatizados utilizando Pytest e FastAPI TestClient, com o objetivo de validar os controles de segurança desenvolvidos nos exercícios anteriores.

Os testes estão localizados em:

`fastapi/tests/test_security.py`

**Testes implementados:**

| Teste | Objetivo | Resultado esperado |
|---|---|---|
| `test_acesso_sem_token` | Verificar se uma rota protegida rejeita requisições sem token JWT | HTTP 401 |
| `test_acesso_prediction_outro_usuario` | Verificar se um usuário não consegue acessar predictions pertencentes a outro usuário | HTTP 404 |
| `test_campo_extra_rejeitado` | Verificar se o Pydantic rejeita campos não definidos no modelo de entrada | HTTP 422 |

**Ambiente de testes:**

Foi utilizado um banco SQLite temporário em memória, separado do banco de dados principal da aplicação. Foram criados usuários e predictions fictícios para garantir o isolamento dos testes.

**Execução:**

A partir da pasta `fastapi`, executar:

```bash
python -m pytest tests/test_security.py -v
```

**Resultado obtido:**

```text
test_acesso_sem_token PASSED
test_acesso_prediction_outro_usuario PASSED
test_campo_extra_rejeitado PASSED

3 passed
```

**Conclusão:**

Os três testes automatizados foram executados com sucesso, confirmando que:

- As rotas protegidas exigem autenticação JWT.
- O controle de ownership impede o acesso a recursos de outros usuários.
- A API rejeita campos extras nas requisições utilizando `extra="forbid"`.

Os resultados demonstram o funcionamento dos controles de segurança avaliados.




# Sistema de Atendimento com Inteligência Artificial — TP3

**Projeto de Bloco — Engenharia de Software**

**Aluna:** Grazielli Soares

## 1. Apresentação

Este repositório contém o desenvolvimento do Projeto de Bloco **Sistema de Atendimento com Inteligência Artificial**, realizado ao longo dos Testes de Performance 1, 2 e 3 (TP1, TP2 e TP3).

O projeto utiliza um conjunto de dados de chamados de suporte ao cliente para realizar análises exploratórias, investigar problemas de aprendizado de máquina e desenvolver uma API REST com FastAPI, autenticação JWT e controles de segurança.

O TP3 dá continuidade às entregas anteriores, acrescentando experimentos de regressão linear, formalização de um problema de classificação textual, testes automatizados de segurança, integração contínua com GitHub Actions, auditoria passiva com OWASP ZAP e planejamento das próximas etapas.

## 2. Tecnologias utilizadas

- Python 3.13
- Pandas e NumPy
- Matplotlib e Seaborn
- Scikit-learn
- Jupyter Notebook
- FastAPI e Uvicorn
- SQLite e SQLModel
- JWT e OAuth2
- Pydantic
- SlowAPI
- Pytest e HTTPX
- OWASP ZAP
- Git e GitHub Actions

## 3. Dataset

Foi utilizado o **Customer Support Ticket Dataset**, disponibilizado na plataforma Kaggle.

O conjunto de dados contém informações relacionadas a chamados de atendimento ao cliente, incluindo:

- Tipo de chamado
- Assunto e descrição
- Prioridade
- Canal de atendimento
- Informações do cliente
- Status e resolução
- Avaliação de satisfação

O arquivo utilizado no projeto está localizado em:

`data/customer_support_tickets.csv`

Nas análises de classificação foram considerados **8.469 registros válidos**.

## 4. Evolução do projeto

### TP1 — Análise exploratória inicial

No primeiro Teste de Performance foram realizadas atividades de compreensão do problema e exploração inicial do dataset.

As análises incluíram:

- Inspeção da estrutura dos dados.
- Identificação de valores ausentes e duplicados.
- Limpeza e preparação de variáveis.
- Análise univariada.
- Visualização da distribuição dos tipos de chamados.
- Análise de prioridades, canais de atendimento e satisfação.
- Formulação de hipóteses sobre as intenções dos usuários.

Também foi iniciada a construção da API de atendimento com FastAPI.

### TP2 — Análise estatística e segurança da API

O segundo Teste de Performance ampliou a análise exploratória e os controles de segurança da aplicação.

Foram realizadas:

- Análises multivariadas e correlações.
- Testes estatísticos com Mann-Whitney.
- Identificação de outliers pelo método IQR.
- Documentação das conclusões do EDA.
- Persistência de dados com SQLite.
- Autenticação baseada em JWT.
- Proteção contra acesso indevido a registros de outros usuários.
- Validação de entradas com Pydantic.
- Configuração de CORS e cabeçalhos HTTP de segurança.
- Limitação de requisições com SlowAPI.
- Verificações de segurança com OWASP ZAP.

### TP3 — Regressão, classificação e validação de segurança

O terceiro Teste de Performance compreende seis exercícios.

#### Exercício 1 — Regressão Linear

Foi desenvolvido um experimento de regressão linear para prever a quantidade de palavras na descrição dos chamados.

**Variável-alvo:** quantidade de palavras em `Ticket Description`.

Foram utilizadas características do cliente e do chamado como variáveis explicativas.

Resultados obtidos:

| Métrica | Resultado |
|---|---:|
| R² | -0,0005 |
| RMSE | 8,7156 palavras |

Também foram produzidos gráficos de resíduos e Q-Q plot.

O desempenho observado indica que as variáveis selecionadas possuem baixa capacidade explicativa para a quantidade de palavras das descrições.

O experimento demonstra as limitações da regressão linear para o problema proposto, cujo objetivo principal é identificar categorias de intenção.

#### Exercício 2 — Formalização da classificação

O problema foi definido como uma **classificação supervisionada multiclasse**.

- **Entrada (X):** texto de `Ticket Description`.
- **Saída (y):** categoria de `Ticket Type`.

Distribuição das classes:

| Categoria | Registros | Percentual |
|---|---:|---:|
| Refund request | 1.752 | 20,69% |
| Technical issue | 1.747 | 20,63% |
| Cancellation request | 1.695 | 20,01% |
| Product inquiry | 1.641 | 19,38% |
| Billing inquiry | 1.634 | 19,29% |

As cinco categorias apresentam distribuição relativamente equilibrada.

A coluna `Ticket Type` foi adotada como aproximação da intenção do usuário, reconhecendo-se que uma classificação administrativa não corresponde necessariamente à intenção semântica expressa no texto.

#### Exercício 3 — Testes automatizados de segurança

Foram implementados seis testes automatizados utilizando Pytest e TestClient.

| Teste | Verificação |
|---|---|
| Acesso sem token | Rejeição de acesso não autenticado |
| Acesso a registro de outro usuário | Proteção contra BOLA |
| Campo extra na requisição | Validação Pydantic |
| Credenciais inválidas | Rejeição de autenticação incorreta |
| Credenciais válidas | Emissão de token JWT |
| Rate limiting | Bloqueio após excesso de tentativas |

**Resultado local:** 6 testes aprovados.

Os testes utilizam um banco SQLite em memória, evitando alterações no banco principal da aplicação.

#### Exercício 4 — Integração contínua

Foi configurado um workflow do GitHub Actions para executar automaticamente os testes de segurança.

O workflow realiza:

1. Checkout do repositório.
2. Configuração do Python 3.13.
3. Instalação das dependências.
4. Execução do Pytest.
5. Sinalização de falha caso algum teste não seja aprovado.

**Observação:** a configuração foi preparada localmente; sua execução no GitHub Actions deverá ser validada após o envio ao repositório remoto.

#### Exercício 5 — Auditoria passiva com OWASP ZAP

Foi realizada uma auditoria passiva da API utilizando o OWASP ZAP.

Durante as verificações foram identificados alertas relacionados a recursos externos, políticas de segurança e bibliotecas JavaScript.

As melhorias implementadas incluíram:

- Ajuste da Content Security Policy (CSP).
- Hospedagem local dos arquivos do Swagger UI.
- Atualização do Swagger UI para a versão 5.35.0.
- Preservação dos cabeçalhos HTTP de segurança.
- Reexecução dos testes automatizados após as alterações.

Na sessão final analisada, foram observados:

| Nível de risco | Tipos de alertas |
|---|---:|
| Alto | 0 |
| Médio | 0 |
| Baixo | 1 |
| Informativo | 1 |

O resultado corresponde às requisições observadas durante a auditoria passiva e não representa garantia de ausência de vulnerabilidades.

As evidências e o relatório estão disponíveis na pasta `zap/`.

#### Exercício 6 — Planejamento

Foi elaborado um documento de planejamento para a evolução do sistema.

A abordagem inicialmente proposta utiliza:

- **CountVectorizer** para representação numérica das mensagens.
- **LogisticRegression** como algoritmo candidato de classificação.
- **Pipeline** do scikit-learn para integração das etapas.
- Avaliação com acurácia, precisão, recall, F1-score e matriz de confusão.

O documento também estabelece um escopo preliminar de testes de segurança para TP4 e TP5, limitado ao ambiente autorizado.

O planejamento está disponível em:

`others/planejamento.md`

## 5. Estrutura principal do projeto

```text
grazielli_soares_pb_tp3/
├── .github/
│   └── workflows/
│       └── testes.yml
├── data/
│   └── customer_support_tickets.csv
├── eda/
│   └── eda_tp3.ipynb
├── fastapi/
│   ├── main.py
│   ├── requirements.txt
│   ├── database.db
│   ├── routes/
│   ├── models/
│   ├── security/
│   ├── static/
│   │   └── swagger/
│   └── tests/
│       └── test_security.py
├── others/
│   └── planejamento.md
├── zap/
│   ├── evidencia_alertas_finais_tp3.png
│   ├── relatorio_zap_tp3.html
│   └── scan_passivo_zap_TP3.md
└── README.md
```

Outros arquivos auxiliares de configuração, banco de dados e documentação podem estar presentes nas respectivas pastas.

## 6. Como executar a API

### Pré-requisitos

- Python 3.13
- Git
- Dependências Python descritas em `requirements.txt`

Clone o repositório:

```bash
git clone https://github.com/GrazielliSoares/grazielli_soares_pb_tp3.git
```

Entre na pasta da API:

```bash
cd grazielli_soares_pb_tp3/fastapi
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Configure as variáveis de ambiente necessárias para a autenticação, conforme as configurações da aplicação.

Inicie o servidor:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs

O esquema OpenAPI poderá ser consultado em:

http://127.0.0.1:8000/openapi.json

## 7. Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/auth/token` | Autenticação e emissão de JWT |
| GET | `/health` | Verificação do funcionamento |
| POST | `/predict` | Endpoint de previsão/classificação |
| GET | `/predictions/{prediction_id}` | Consulta de previsão registrada |

Os endpoints protegidos exigem autenticação.

A implementação do classificador textual com CountVectorizer e LogisticRegression está prevista para uma etapa futura. O planejamento do modelo não deve ser confundido com um classificador já treinado e integrado à API.

## 8. Como executar os testes

No terminal, dentro da pasta `fastapi`, execute:

```bash
python -m pytest tests/ -v
```

O resultado local validado durante o TP3 foi:

```text
6 passed
```

Os testes verificam controles relacionados a autenticação, autorização, validação de dados e limitação de requisições.

## 9. Análise exploratória

O notebook:

`eda/eda_tp3.ipynb`

Reúne as análises dos três Testes de Performance em um único arquivo.

Sua organização contempla:

- TP1 — Análise exploratória inicial.
- TP2 — Análise estatística e aprofundamento do EDA.
- TP3 — Regressão linear, classificação e documentação dos testes.

O notebook pode ser aberto no Jupyter Notebook ou no Visual Studio Code com a extensão Jupyter.

## 10. Segurança e limitações

O projeto incorpora controles de autenticação, autorização, validação de dados, limitação de requisições e cabeçalhos HTTP de segurança.

A auditoria realizada com OWASP ZAP foi passiva e limitada às requisições efetivamente observadas.

O endereço `127.0.0.1` representa o ambiente local de desenvolvimento e não autoriza a execução de testes em sistemas externos.

As credenciais, tokens e chaves secretas reais não devem ser publicados no repositório.

## 11. Próximas etapas

As próximas entregas poderão incluir:

- Implementação do classificador de intenções.
- Treinamento e avaliação do modelo.
- Integração do pipeline à API.
- Ampliação dos testes automatizados.
- Testes de segurança adicionais em ambiente autorizado.
- Aprimoramento da documentação técnica.

## 12. Conclusão

O TP3 consolida a evolução do Sistema de Atendimento com Inteligência Artificial, integrando análise exploratória de dados, experimentação com aprendizado de máquina, desenvolvimento de API e práticas de segurança de software.

Os experimentos realizados fundamentam a escolha de um problema de classificação textual, enquanto os testes automatizados e a auditoria passiva contribuem para a validação dos controles de segurança implementados.

O projeto estabelece uma base para a futura implementação de um classificador de intenções integrado à API FastAPI.
