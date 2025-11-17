# -*- coding: utf-8 -*-
"""
Seleção ótima de habilidades (knapsack 0/1) com:
- Recursão + memoização
- Ordenação recursiva (merge sort) dos dados em DataFrame
- Relatórios por funcionário e categoria
- Pelo menos 20 informações na base
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
from functools import lru_cache
from datetime import datetime
import pandas as pd

# ---------------------------
# Definição dos dados
# ---------------------------

@dataclass(frozen=True)
class HabilidadeRegistro:
    id_andamento: int
    funcionario: str
    habilidade: str
    categoria: str
    status: str
    nivel: str
    horas_estimadas: int       # "peso" da mochila
    valor_impacto: int         # "valor" da mochila
    ultima_alteracao: datetime

def gerar_base_dados() -> List[HabilidadeRegistro]:
    """Gera pelo menos 20 registros simulando a tabela andamento_habilidade."""
    base = [
        HabilidadeRegistro(1, "Ana Souza", "Machine Learning", "Tecnologia", "Aprendendo", "Iniciante", 40, 85, datetime(2025, 11, 1)),
        HabilidadeRegistro(2, "Carlos Lima", "Inteligência Emocional", "Soft Skill", "Concluído", "Intermediário", 20, 60, datetime(2025, 11, 2)),
        HabilidadeRegistro(3, "Mariana Alves", "Gestão de Projetos Ágeis", "Gestão", "Iniciando", "Iniciante", 30, 70, datetime(2025, 11, 3)),
        HabilidadeRegistro(4, "João Pereira", "Design Thinking", "Inovação", "Aprendendo", "Intermediário", 25, 65, datetime(2025, 11, 4)),
        HabilidadeRegistro(5, "Fernanda Costa", "Comunicação Assertiva", "Soft Skill", "Concluído", "Avançado", 15, 55, datetime(2025, 11, 5)),
        HabilidadeRegistro(6, "Ana Souza", "Data Visualization", "Tecnologia", "Aprendendo", "Intermediário", 22, 58, datetime(2025, 11, 6)),
        HabilidadeRegistro(7, "Carlos Lima", "Negociação", "Soft Skill", "Aprendendo", "Intermediário", 18, 50, datetime(2025, 11, 6)),
        HabilidadeRegistro(8, "Mariana Alves", "Arquitetura de Software", "Tecnologia", "Iniciando", "Iniciante", 35, 80, datetime(2025, 11, 7)),
        HabilidadeRegistro(9, "João Pereira", "UX Research", "Inovação", "Aprendendo", "Intermediário", 28, 62, datetime(2025, 11, 7)),
        HabilidadeRegistro(10, "Fernanda Costa", "People Analytics", "Gestão", "Aprendendo", "Intermediário", 26, 66, datetime(2025, 11, 8)),
        HabilidadeRegistro(11, "Ana Souza", "Estatística Aplicada", "Tecnologia", "Aprendendo", "Iniciante", 24, 59, datetime(2025, 11, 9)),
        HabilidadeRegistro(12, "Carlos Lima", "OKRs", "Gestão", "Aprendendo", "Intermediário", 16, 48, datetime(2025, 11, 9)),
        HabilidadeRegistro(13, "Mariana Alves", "Cloud Fundamentals", "Tecnologia", "Aprendendo", "Iniciante", 32, 74, datetime(2025, 11, 9)),
        HabilidadeRegistro(14, "João Pereira", "Prototipação Rápida", "Inovação", "Aprendendo", "Intermediário", 20, 57, datetime(2025, 11, 9)),
        HabilidadeRegistro(15, "Fernanda Costa", "Mediação de Conflitos", "Soft Skill", "Iniciando", "Intermediário", 18, 52, datetime(2025, 11, 9)),
        HabilidadeRegistro(16, "Ana Souza", "SQL Avançado", "Tecnologia", "Aprendendo", "Intermediário", 27, 68, datetime(2025, 11, 10)),
        HabilidadeRegistro(17, "Carlos Lima", "Storytelling", "Soft Skill", "Aprendendo", "Intermediário", 14, 46, datetime(2025, 11, 10)),
        HabilidadeRegistro(18, "Mariana Alves", "Segurança da Informação", "Tecnologia", "Aprendendo", "Iniciante", 33, 76, datetime(2025, 11, 10)),
        HabilidadeRegistro(19, "João Pereira", "Acessibilidade Digital", "Inovação", "Aprendendo", "Intermediário", 21, 56, datetime(2025, 11, 10)),
        HabilidadeRegistro(20, "Fernanda Costa", "Feedback Eficaz", "Soft Skill", "Concluído", "Avançado", 12, 44, datetime(2025, 11, 10)),
        HabilidadeRegistro(21, "Ana Souza", "MLOps Básico", "Tecnologia", "Iniciando", "Iniciante", 29, 69, datetime(2025, 11, 10)),
        HabilidadeRegistro(22, "Carlos Lima", "Facilitação de Workshops", "Gestão", "Aprendendo", "Intermediário", 23, 61, datetime(2025, 11, 10)),
        HabilidadeRegistro(23, "Mariana Alves", "Testes Automatizados", "Tecnologia", "Aprendendo", "Intermediário", 31, 72, datetime(2025, 11, 10)),
        HabilidadeRegistro(24, "João Pereira", "Design de Serviço", "Inovação", "Aprendendo", "Intermediário", 26, 64, datetime(2025, 11, 10)),
        HabilidadeRegistro(25, "Fernanda Costa", "Entrevistas Estruturadas", "Soft Skill", "Aprendendo", "Intermediário", 17, 49, datetime(2025, 11, 10)),
    ]
    return base

# ---------------------------
# Ordenação recursiva: merge sort
# ---------------------------

def merge(left: List[Any], right: List[Any], key):
    """Intercala duas listas ordenadas."""
    if not left:
        return right
    if not right:
        return left
    if key(left[0]) <= key(right[0]):
        return [left[0]] + merge(left[1:], right, key)
    else:
        return [right[0]] + merge(left, right[1:], key)

def merge_sort(data: List[Any], key):
    """Ordena recursivamente usando merge sort."""
    n = len(data)
    if n <= 1:
        return data
    mid = n // 2
    left_sorted = merge_sort(data[:mid], key)
    right_sorted = merge_sort(data[mid:], key)
    return merge(left_sorted, right_sorted, key)

# ---------------------------
# Conversão para DataFrame (pandas)
# ---------------------------

def to_dataframe(registros: List[HabilidadeRegistro]) -> pd.DataFrame:
    """Converte lista de registros em DataFrame."""
    df = pd.DataFrame([{
        "id_andamento": r.id_andamento,
        "funcionario": r.funcionario,
        "habilidade": r.habilidade,
        "categoria": r.categoria,
        "status": r.status,
        "nivel": r.nivel,
        "horas_estimadas": r.horas_estimadas,
        "valor_impacto": r.valor_impacto,
        "ultima_alteracao": r.ultima_alteracao
    } for r in registros])
    return df

# ---------------------------
# Knapsack 0/1 com recursão + memoização
# ---------------------------

def preparar_itens(df: pd.DataFrame) -> List[Tuple[int, int, Dict[str, Any]]]:
    """
    Prepara itens no formato (peso, valor, metadados).
    peso = horas_estimadas
    valor = valor_impacto
    metadados = linha completa para relatório
    """
    itens = []
    for _, row in df.iterrows():
        itens.append((int(row["horas_estimadas"]), int(row["valor_impacto"]), row.to_dict()))
    return itens

def knapsack_solver(itens: List[Tuple[int, int, Dict[str, Any]]], capacidade: int):
    """
    Resolve o knapsack 0/1 usando recursão e memoização.
    Retorna (valor_maximo, itens_selecionados, horas_totais).
    """

    @lru_cache(maxsize=None)
    def dp(i: int, cap: int) -> Tuple[int, Tuple[int, ...]]:
        # i: índice do item atual, cap: capacidade restante
        if i == len(itens) or cap <= 0:
            return 0, tuple()
        peso, valor, _meta = itens[i]

        # Caso 1: pular item
        val_skip, sel_skip = dp(i + 1, cap)

        # Caso 2: incluir item (se couber)
        if peso <= cap:
            val_take, sel_take = dp(i + 1, cap - peso)
            val_take += valor
            if val_take > val_skip:
                return val_take, sel_take + (i,)
        # Caso 3: melhor é pular
        return val_skip, sel_skip

    valor_max, indices = dp(0, capacidade)
    itens_sel = [itens[i] for i in indices]
    horas_totais = sum(p for p, _v, _m in itens_sel)
    return valor_max, itens_sel, horas_totais

# ---------------------------
# Relatórios
# ---------------------------

def relatorio_selecao(itens_sel: List[Tuple[int, int, Dict[str, Any]]]) -> pd.DataFrame:
    """Gera DataFrame com itens selecionados e campos relevantes."""
    linhas = []
    for peso, valor, meta in itens_sel:
        linhas.append({
            "funcionario": meta["funcionario"],
            "habilidade": meta["habilidade"],
            "categoria": meta["categoria"],
            "status": meta["status"],
            "nivel": meta["nivel"],
            "horas": peso,
            "valor": valor,
            "ultima_alteracao": meta["ultima_alteracao"]
        })
    df = pd.DataFrame(linhas)
    return df

def relatorio_por_funcionario(df_sel: pd.DataFrame) -> pd.DataFrame:
    """Resumo por funcionário: total de horas e valor."""
    if df_sel.empty:
        return pd.DataFrame(columns=["funcionario", "horas_total", "valor_total"])
    resumo = (
        df_sel.groupby("funcionario")[["horas", "valor"]]
        .sum()
        .reset_index()
        .rename(columns={"horas": "horas_total", "valor": "valor_total"})
    )
    return resumo

def relatorio_por_categoria(df_sel: pd.DataFrame) -> pd.DataFrame:
    """Resumo por categoria: total de horas e valor."""
    if df_sel.empty:
        return pd.DataFrame(columns=["categoria", "horas_total", "valor_total"])
    resumo = (
        df_sel.groupby("categoria")[["horas", "valor"]]
        .sum()
        .reset_index()
        .rename(columns={"horas": "horas_total", "valor": "valor_total"})
    )
    return resumo

# ---------------------------
# Pipeline principal
# ---------------------------

def pipeline(capacidade_horas: int, ordenar_por: str = "valor_impacto", crescente: bool = False) -> Dict[str, Any]:
    """
    1) Gera base (>= 20 itens)
    2) Ordena recursivamente pelo campo escolhido (merge sort)
    3) Converte para DataFrame
    4) Prepara itens e resolve knapsack (recursão + memo)
    5) Gera relatórios
    """
    registros = gerar_base_dados()

    # Ordenação recursiva com merge sort
    keyfunc = (lambda r: getattr(r, ordenar_por)) if hasattr(registros[0], ordenar_por) else (
        lambda r: {
            "horas_estimadas": r.horas_estimadas,
            "valor_impacto": r.valor_impacto,
            "ultima_alteracao": r.ultima_alteracao
        }[ordenar_por]
    )
    ordenados = merge_sort(registros, keyfunc)
    if not crescente:
        ordenados = list(reversed(ordenados))

    df = to_dataframe(ordenados)
    itens = preparar_itens(df)
    valor_max, itens_sel, horas_totais = knapsack_solver(itens, capacidade_horas)
    df_sel = relatorio_selecao(itens_sel)
    resumo_func = relatorio_por_funcionario(df_sel)
    resumo_cat = relatorio_por_categoria(df_sel)

    resultados = {
        "capacidade": capacidade_horas,
        "valor_max": valor_max,
        "horas_totais": horas_totais,
        "selecionados": df_sel.sort_values(by="valor", ascending=False).reset_index(drop=True),
        "resumo_funcionario": resumo_func.sort_values(by="valor_total", ascending=False).reset_index(drop=True),
        "resumo_categoria": resumo_cat.sort_values(by="valor_total", ascending=False).reset_index(drop=True),
        "dados_ordenados": df
    }
    return resultados

# ---------------------------
# Execução de exemplo (não teste mínimo; base tem 25 itens)
# ---------------------------

if __name__ == "__main__":
    # Capacidade de horas disponível (ex.: 200 horas)
    resultados = pipeline(capacidade_horas=200, ordenar_por="valor_impacto", crescente=False)

    print("\n=== Configuração ===")
    print(f"Capacidade (horas): {resultados['capacidade']}")
    print(f"Valor máximo obtido: {resultados['valor_max']}")
    print(f"Horas totais selecionadas: {resultados['horas_totais']}")

    print("\n=== Seleção ótima (top 10 por valor) ===")
    print(resultados["selecionados"].head(10).to_string(index=False))

    print("\n=== Resumo por funcionário ===")
    print(resultados["resumo_funcionario"].to_string(index=False))

    print("\n=== Resumo por categoria ===")
    print(resultados["resumo_categoria"].to_string(index=False))

    print("\n=== Dados ordenados (primeiras 10 linhas) ===")
    print(resultados["dados_ordenados"].head(10).to_string(index=False))
