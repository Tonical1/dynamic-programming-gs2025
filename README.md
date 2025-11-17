Pedro Gaspar - RM: 554887

Enrico Ricarte - RM: 558571

# README — dynamic_ferrari.py

Este README explica, passo a passo, cada função presente no arquivo `dynamic_ferrari.py`. O objetivo do script é selecionar um conjunto ótimo de "habilidades" (problema Knapsack 0/1) usando recursão e memoização, com relatórios por funcionário e por categoria. Também há uma implementação recursiva de ordenação (merge sort) usada antes de construir o DataFrame.

Observação: o script depende de `pandas` para manipulação de tabelas; instale com `pip install pandas` se necessário.

## Sistema Integrado de Desenvolvimento Futuro — Visão Conceitual

Este repositório apresenta parte da implementação conceitual de uma solução voltada ao desenvolvimento contínuo de habilidades dentro de organizações.
A proposta geral da plataforma é funcionar como um hub de evolução profissional, onde colaboradores podem registrar competências que desejam aprimorar, acompanhar metas, criar solicitações internas e monitorar seu progresso ao longo do tempo.

A visão da solução está alinhada com temas contemporâneos como:
- Transformação digital
- Aprendizado contínuo
- Upskilling e reskilling
- Gestão do conhecimento
- Organização e priorização de desenvolvimento

A ideia central é oferecer uma base estruturada para que equipes tenham clareza sobre:
- Habilidades desejadas ou necessárias
- Metas individuais e coletivas
- Demandas internas relacionadas ao crescimento profissional
- Evolução das competências ao longo do tempo

## Papel deste Arquivo (dynamic_ferrari.py)

Dentro desse contexto mais amplo, o arquivo dynamic_ferrari.py representa um módulo técnico demonstrativo da solução.
Ele implementa, em Python, um conjunto de funcionalidades que simulam como o sistema poderia:

- Organizar registros de habilidades
- Ordenar dados de maneira customizável
- Priorizar investimentos de desenvolvimento usando um algoritmo de otimização (Knapsack 0/1)
- Gerar relatórios estruturados por funcionário e categoria

Em outras palavras, este módulo funciona como um protótipo do núcleo lógico da plataforma:
capaz de analisar habilidades, aplicar critérios de impacto e horas, e sugerir uma seleção otimizada de desenvolvimento — algo diretamente aplicável a sistemas reais de gestão de pessoas.

A seguir está o conteúdo completo do README técnico original, preservado integralmente.

---

Sumário das funções/documentos a seguir:
- `HabilidadeRegistro` (dataclass)
- `gerar_base_dados()`
- `merge(left, right, key)`
- `merge_sort(data, key)`
- `to_dataframe(registros)`
- `preparar_itens(df)`
- `knapsack_solver(itens, capacidade)` (internamente usa `@lru_cache` para dp)
- `relatorio_selecao(itens_sel)`
- `relatorio_por_funcionario(df_sel)`
- `relatorio_por_categoria(df_sel)`
- `pipeline(capacidade_horas, ordenar_por, crescente)`
- Bloco `if __name__ == "__main__"`

Cada função tem: o que faz, entradas, saídas, passos internos (recursão/memoização), e exemplo de uso.

---

## `HabilidadeRegistro` (dataclass)

O que faz:
- Define a estrutura imutável (frozen) para um registro de habilidade.

Campos / significado:
- `id_andamento` (int): identificador do registro
- `funcionario` (str): nome do colaborador
- `habilidade` (str): nome da habilidade
- `categoria` (str): categoria da habilidade (ex.: Tecnologia, Soft Skill)
- `status` (str): status do acompanhamento
- `nivel` (str): nível (Iniciante/Intermediário/Avançado)
- `horas_estimadas` (int): peso usado no knapsack (horas necessárias)
- `valor_impacto` (int): valor usado no knapsack (impacto estimado)
- `ultima_alteracao` (datetime): timestamp da última alteração

Uso:
- Instanciada por `gerar_base_dados()` para criar a base de registros.

---

## `gerar_base_dados()`

O que faz:
- Gera uma lista de instâncias `HabilidadeRegistro` com pelo menos 20 registros simulados.

Entrada:
- Nenhuma.

Saída:
- `List[HabilidadeRegistro]` com registros de exemplo.

Passo a passo:
1. Cria uma lista `base` com `HabilidadeRegistro(...)` preenchidos manualmente.
2. Retorna `base`.

Exemplo:
- `registros = gerar_base_dados()`

Observações:
- Ideal para testes e demonstrações; pode ser substituída por uma função que carregue dados reais.

---

## `merge(left, right, key)`

O que faz:
- Intercala (`merge`) duas listas já ordenadas de acordo com a função `key`.

Entradas:
- `left` (List[Any]): primeira lista ordenada
- `right` (List[Any]): segunda lista ordenada
- `key` (callable): função que extrai a chave de comparação de cada item

Saída:
- Lista com todos os elementos de `left` e `right` intercalados, ordenada por `key`.

Passo a passo (recursivo):
1. Se `left` estiver vazio, retorna `right` (caso base).
2. Se `right` estiver vazio, retorna `left` (caso base).
3. Compara `key(left[0])` com `key(right[0])`:
   - Se `key(left[0]) <= key(right[0])`, coloca `left[0]` na frente e chama `merge(left[1:], right, key)`.
   - Caso contrário, coloca `right[0]` e chama `merge(left, right[1:], key)`.
4. A recursão termina quando uma das listas ficar vazia.

Observações:
- Função recursiva tradicional de merge de merge sort.

---

## `merge_sort(data, key)`

O que faz:
- Ordena `data` recursivamente usando merge sort com a função `key`.

Entradas:
- `data` (List[Any]): lista a ordenar
- `key` (callable): função para extrair a chave de cada elemento

Saída:
- Nova lista ordenada por `key`.

Passo a passo (recursivo):
1. Se `len(data) <= 1`, retorna `data` (caso base).
2. Divide `data` em duas metades: `left` e `right`.
3. Chama `merge_sort(left, key)` recursivamente para ordenar a metade esquerda.
4. Chama `merge_sort(right, key)` recursivamente para ordenar a metade direita.
5. Usa `merge(left_sorted, right_sorted, key)` para unir e retorna o resultado.

Observações:
- A função `key` permite ordenar por qualquer campo (por exemplo `valor_impacto` ou `horas_estimadas`).

---

## `to_dataframe(registros)`

O que faz:
- Converte a lista de `HabilidadeRegistro` em um `pandas.DataFrame` com colunas legíveis.

Entrada:
- `registros` (List[HabilidadeRegistro])

Saída:
- `pd.DataFrame` com colunas: `id_andamento`, `funcionario`, `habilidade`, `categoria`, `status`, `nivel`, `horas_estimadas`, `valor_impacto`, `ultima_alteracao`.

Passo a passo:
1. Itera sobre `registros` e monta uma lista de dicionários com os campos desejados.
2. Chama `pd.DataFrame(...)` e retorna.

Observações:
- Útil para gerar relatórios tabulares com `pandas` e usar `groupby`.

---

## `preparar_itens(df)`

O que faz:
- Converte o DataFrame em uma lista de tuplas `(peso, valor, metadados)` para o solver da mochila.

Entrada:
- `df` (`pd.DataFrame`): DataFrame com colunas `horas_estimadas` e `valor_impacto`.

Saída:
- `List[Tuple[int, int, Dict[str, Any]]]` onde cada tupla contém:
  - `peso` (int) = `horas_estimadas`
  - `valor` (int) = `valor_impacto`
  - `metadados` (dict) = dicionário da linha (para relatórios)

Passo a passo:
1. Itera sobre `df.iterrows()`.
2. Para cada linha, adiciona `(int(horas_estimadas), int(valor_impacto), row.to_dict())` à lista `itens`.
3. Retorna `itens`.

---

## `knapsack_solver(itens, capacidade)`

O que faz:
- Resolve o problema knapsack 0/1 (selecionar itens sem fracionamento) usando recursão com memoização via `functools.lru_cache`.

Entradas:
- `itens` (List[Tuple[peso, valor, metadados]]): lista com peso e valor por item
- `capacidade` (int): capacidade total (horas disponíveis)

Saída:
- Tupla `(valor_maximo, itens_selecionados, horas_totais)` onde:
  - `valor_maximo` é a soma máxima de valores alcançada
  - `itens_selecionados` é a lista dos itens (tuplas) escolhidos
  - `horas_totais` é a soma dos pesos dos itens escolhidos

Passo a passo (dp recursivo memoizado):
1. Define `dp(i, cap)` decorada com `@lru_cache(maxsize=None)` onde `i` é o índice atual e `cap` a capacidade restante.
2. Caso base: se `i == len(itens)` ou `cap <= 0`, retorna `(0, tuple())`.
3. Lê `peso, valor, _meta = itens[i]`.
4. Calcula `val_skip, sel_skip = dp(i+1, cap)` (pular o item).
5. Se `peso <= cap`, calcula `val_take, sel_take = dp(i+1, cap - peso)` e soma `valor` a `val_take`. Se `val_take > val_skip`, retorna `(val_take, sel_take + (i,))`.
6. Caso contrário, retorna `(val_skip, sel_skip)`.
7. Fora de `dp`, chama `dp(0, capacidade)` para obter `(valor_max, indices)`; converte `indices` em `itens_sel` e calcula `horas_totais`.

Observações:
- A memoização via `lru_cache` evita recomputar muitos subproblemas e garante que o algoritmo seja eficiente para a faixa de dados do script.
- `dp` retorna índices como uma `tuple` para que seja hashable e compatível com `lru_cache`.

Exemplo de uso:
```python
valor_max, itens_sel, horas = knapsack_solver(itens, capacidade=200)
```

---

## `relatorio_selecao(itens_sel)`

O que faz:
- Constrói um `DataFrame` resumido com os itens selecionados para fins de relatório.

Entrada:
- `itens_sel`: lista de tuplas `(peso, valor, meta)` retornada por `knapsack_solver`.

Saída:
- `pd.DataFrame` com colunas: `funcionario`, `habilidade`, `categoria`, `status`, `nivel`, `horas`, `valor`, `ultima_alteracao`.

Passo a passo:
1. Itera `itens_sel` e para cada item monta um dicionário com os campos relevantes usando `meta`.
2. Converte lista de dicionários em `pd.DataFrame` e retorna.

---

## `relatorio_por_funcionario(df_sel)`

O que faz:
- Agrupa `df_sel` por `funcionario` e soma `horas` e `valor` para produzir um resumo por funcionário.

Entrada:
- `df_sel` (`pd.DataFrame`) resultante de `relatorio_selecao`.

Saída:
- `pd.DataFrame` com colunas `funcionario`, `horas_total`, `valor_total`.

Passo a passo:
1. Se `df_sel` estiver vazio, retorna `DataFrame` vazio com colunas apropriadas.
2. Caso contrário, usa `groupby` + `sum()` e renomeia colunas.
3. Retorna `resumo`.

---

## `relatorio_por_categoria(df_sel)`

O que faz:
- Idêntico a `relatorio_por_funcionario`, mas agrupa por `categoria`.

---

## `pipeline(capacidade_horas, ordenar_por='valor_impacto', crescente=False)`

O que faz (fluxo completo):
1. Gera a base de dados chamando `gerar_base_dados()`.
2. Define `keyfunc` para ordenar os registros pelo campo escolhido (`ordenar_por`).
3. Ordena recursivamente com `merge_sort(registros, keyfunc)`.
4. Se `crescente` for `False`, inverte a lista para ordem decrescente.
5. Converte para DataFrame (`to_dataframe`).
6. Prepara `itens` com `preparar_itens(df)`.
7. Resolve o knapsack: `valor_max, itens_sel, horas_totais = knapsack_solver(itens, capacidade_horas)`.
8. Gera `df_sel = relatorio_selecao(itens_sel)` e resumos por funcionário e categoria.
9. Retorna um dicionário `resultados` com todos os componentes (incl. `dados_ordenados`).

Entradas:
- `capacidade_horas` (int): limite de horas para seleção
- `ordenar_por` (str): nome do campo por onde ordenar (ex.: `valor_impacto`)
- `crescente` (bool): se `True`, ordena crescente; se `False`, ordena decrescente

Saída:
- `Dict[str, Any]` contendo: `capacidade`, `valor_max`, `horas_totais`, `selecionados` (DataFrame), `resumo_funcionario`, `resumo_categoria`, `dados_ordenados`.

Exemplo de uso:
```python
resultados = pipeline(capacidade_horas=200, ordenar_por='valor_impacto', crescente=False)
print(resultados['valor_max'])
print(resultados['selecionados'].head())
```

---

## Bloco principal (`if __name__ == '__main__'`)

O que faz:
- Executa um exemplo completo usando `pipeline` com `capacidade_horas=200`. Imprime:
  - Configurações básicas
  - Seleção ótima (top 10 por valor)
  - Resumo por funcionário
  - Resumo por categoria
  - Primeiras linhas dos dados ordenados

Como executar:
```powershell
python dynamic_ferrari.py
```

---

## Dependências

- Python 3.8+
- pandas (para DataFrame e agrupamentos)

Instalação rápida:
```powershell
pip install pandas
```

---
