# Prompt da dashboard e o que mudou até a versão final

A dashboard foi gerada por um **agente de IA (Claude Code)** trabalhando com duas "skills" deste repositório:

1. **Tratar o dado:** [`agents/sanitize_porsche.py`](../agents/sanitize_porsche.py), seguindo as regras de [`agents/schema.md`](../agents/schema.md).
2. **Desenhar a dashboard:** o prompt abaixo, com [`agents/prepare_base.py`](../agents/prepare_base.py) e [`agents/build_html.py`](../agents/build_html.py) para embutir a base no HTML.

Não usei o ChatGPT com Canvas: o caminho foi o do agente com skill.

## Prompt inicial

```text
Você é um agente que monta dashboards em HTML.

Base: data/porsche_dashboard_base.json — 100 vendas Porsche nos EUA, já tratadas pelo agente
sanitize_porsche.py. Campos: id, data (ISO ou nulo quando INVALID), modelo, familia, ano,
preco (US$), milhas, pagamento, cidade, estado, entrega.

Gere UM arquivo index.html, sem dependências além de uma fonte do Google Fonts, com a base
embutida, que abra no GitHub Pages.

Responda três perguntas de negócio, cada uma com um gráfico e uma frase de resposta que
se atualize com os filtros:
  1. Quais famílias de modelo (911, 718, Cayenne, Macan, Panamera, Taycan) sustentam o faturamento?
  2. Quanto da receita depende de crédito (Financing, Lease, Credit Card) e quanto é pago à vista?
  3. Quanto da receita ainda não chegou ao cliente (a caminho, parado em aprovação, cancelado)?

Indicadores de topo: receita total, nº de vendas, ticket médio, % da receita via crédito,
% da receita entregue e milhagem média.

Filtros: família, modelo (dependente da família), estado, ano-modelo e método de pagamento,
mais um botão de limpar.

Visual: fundo grafite escuro, vermelho como única cor de destaque, prata e cinzas para o resto,
tipografia Barlow Condensed nos títulos e Barlow no texto. Textos em português, valores em US$.
Tem que funcionar no celular.
```

## O que mudou até a versão final

| # | Mudança | Por quê |
|---|---|---|
| 1 | **Nomes de cliente e vendedor saíram da base** embutida no HTML | A base vai pública dentro da página, e esses campos não respondem nenhuma pergunta |
| 2 | **Filtro de cidade trocado por estado** (a cidade continua na tabela) | São 79 cidades para 100 vendas: quase uma por venda, o filtro não recortava nada. Estado agrupa melhor |
| 3 | **Cada gráfico ignora o próprio filtro** (o de família não some quando se filtra uma família, só esmaece as outras barras) | Sem isso, filtrar "911" deixava o gráfico com uma barra só e a comparação se perdia |
| 4 | **Clique nos gráficos filtra** (barras, fatias e legenda) | Deixa a exploração mais rápida que abrir lista |
| 5 | Pergunta 3 com **status agrupados** em 4 situações (Entregue, A caminho, Parado em aprovação, Cancelado) | Os 10 status do agente eram finos demais para uma resposta direta |
| 6 | Painel **Qualidade do dado** | Mostrar o que o agente resolveu e o que ficou INVALID (24 datas impossíveis) e sinalizar datas futuras (19 em 29/10/2026; a página recalcula pela data de hoje) |
| 7 | **Tabela de detalhe** ordenável | Permite conferir qualquer número dos gráficos |
| 8 | **Parâmetros na URL** (`?familia=911&estado=CA`) | Compartilhar um recorte pronto e gerar os prints de filtro |
| 9 | Correções no teste: frase da pergunta 2 que imprimia texto quebrado, concordância ("o da família 911") e plurais ("1 venda", "1 estado") | Achados ao conferir a página no navegador |

## Como conferi

- Página aberta no navegador sem nenhum erro no console.
- Indicadores comparados com um cálculo independente em Python sobre o mesmo JSON:
  receita US$ 12.827.800,50 · crédito 36,4% · entregue 39,6% · cancelado 4,9% · milhagem média 11.422.
- Filtro 911 + CA: 3 vendas, US$ 553.400, igual ao Python.
- Recorte sem vendas (2020 + Cripto): os painéis mostram "Sem vendas" em vez de quebrar.
