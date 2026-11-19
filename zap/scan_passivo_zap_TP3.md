# Relatório de Auditoria Passiva — OWASP ZAP (TP3)

## 1. Objetivo

Realizar uma auditoria passiva de segurança na API de Atendimento ao Cliente, desenvolvida com FastAPI, identificando possíveis configurações inseguras, bibliotecas vulneráveis e problemas relacionados aos cabeçalhos HTTP.

## 2. Ambiente de testes

- **Aplicação:** API de Atendimento ao Cliente
- **Framework:** FastAPI
- **Endereço:** http://127.0.0.1:8000
- **Documentação:** http://127.0.0.1:8000/docs
- **Ferramenta:** OWASP ZAP
- **Modalidade:** análise passiva, sem execução de ataques ativos

A análise foi realizada por meio da exploração manual da documentação Swagger e da observação das requisições HTTP pelo proxy do ZAP.

## 3. Alertas identificados inicialmente

Durante as primeiras verificações, foram identificados alertas relacionados a:

- Configuração incorreta entre domínios (CORS).
- Ausência do cabeçalho Content Security Policy (CSP).
- Ausência de Subresource Integrity (SRI).
- Biblioteca JavaScript potencialmente vulnerável.
- Divulgação de informações de data e hora.
- Identificação de aplicação web moderna.

Os alertas de CORS e ausência de CSP examinados estavam associados a serviços externos, não constituindo evidência de configuração insegura da API local.

O alerta de SRI foi identificado na documentação `/docs`, que carregava recursos externos do Swagger UI sem atributos de integridade.

## 4. Correções implementadas

### 4.1. Ajuste da Content Security Policy

A política CSP foi configurada para permitir o funcionamento da documentação Swagger, preservando restrições para os demais endpoints.

O script de inicialização da documentação foi autorizado por hash SHA-256 específico, evitando a liberação indiscriminada de scripts embutidos.

### 4.2. Hospedagem local do Swagger UI

Os arquivos JavaScript, CSS e favicon do Swagger foram disponibilizados na pasta `fastapi/static/swagger/`.

A documentação passou a utilizar esses arquivos locais, eliminando a dependência direta do CDN para os recursos principais do Swagger.

### 4.3. Atualização do Swagger UI

Durante uma análise intermediária, o ZAP identificou uma biblioteca JavaScript potencialmente vulnerável no arquivo `swagger-ui-bundle.js`.

O Swagger UI foi atualizado para a versão 5.35.0 e uma nova análise passiva foi realizada.

Na nova sessão, o alerta de biblioteca vulnerável não voltou a ser identificado.

## 5. Resultado da auditoria final

Na sessão final do OWASP ZAP, foram observados os seguintes resultados:

| Nível de risco | Tipos de alertas |
|---|---:|
| Alto | 0 |
| Médio | 0 |
| Baixo | 1 |
| Informativo | 1 |

### Alertas restantes

**Divulgação de Data e Hora — Unix (Systemic)**

Alerta de risco baixo relacionado à exposição de informações temporais. Deve ser avaliado conforme a resposta HTTP específica e o contexto da aplicação.

**Modern Web Application**

Alerta informativo que identifica a utilização de JavaScript na interface Swagger. Não representa, isoladamente, uma vulnerabilidade.

## 6. Validação dos testes automatizados

Após as alterações, foram executados os testes automatizados de segurança:

```powershell
python -m pytest tests/ -v
```

**Resultado:** 6 testes aprovados.

Os testes contemplam autenticação, proteção de rotas, controle de acesso a registros, validação de dados e limitação de requisições.

## 7. Evidências

- `evidencia_alertas_finais_tp3.png` — captura da aba Alertas na sessão final.
- `relatorio_zap_tp3.html` — relatório exportado pelo OWASP ZAP.

## 8. Conclusão

A auditoria passiva permitiu identificar e corrigir problemas relacionados ao carregamento de recursos externos da documentação Swagger e à utilização de uma biblioteca JavaScript sinalizada como potencialmente vulnerável.

Na sessão final analisada, não foram identificados alertas de risco alto ou médio.

Os resultados representam as requisições efetivamente observadas durante a análise passiva e não garantem a ausência de vulnerabilidades em toda a aplicação. Testes adicionais, especialmente sobre fluxos autenticados, são recomendados em avaliações futuras.
