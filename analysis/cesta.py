import pandas as pd
import numpy as np
from pulp import *
import random

pd.options.display.max_columns = None
pd.options.display.max_rows = None


random.seed(7)


def stats(
    df,
    produtores_produtor,
    produtores_produtor_verde,
    produtores_produtor_fruta,
    xij,
    yij,
):
    stats_pequena = {}
    stats_grande = {}
    # principais métricas sobre a cesta
    stats_pequena["numero_verde"] = lpSum(
        xij[(i, j)].varValue for (i, j) in produtores_produtor_verde
    )

    stats_pequena["numero_fruta"] = lpSum(
        xij[(i, j)].varValue for (i, j) in produtores_produtor_fruta
    )

    stats_pequena["peso"] = lpSum(
        xij[(i, j)].varValue * df.Peso_CP.loc[i, j] for (i, j) in produtores_produtor
    )

    stats_pequena["preco"] = lpSum(
        xij[(i, j)].varValue
        * df.preco.loc[i, j]
        * df.quantidade_cesta_pequena.loc[i, j]
        for (i, j) in produtores_produtor
    )

    stats_grande["numero_verde"] = lpSum(
        xij[(i, j)].varValue for (i, j) in produtores_produtor_verde
    ) + lpSum(yij[(i, j)].varValue for (i, j) in produtores_produtor_verde)

    stats_grande["numero_fruta"] = lpSum(
        xij[(i, j)].varValue for (i, j) in produtores_produtor_fruta
    ) + lpSum(yij[(i, j)].varValue for (i, j) in produtores_produtor_fruta)

    stats_grande["peso"] = lpSum(
        xij[(i, j)].varValue * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor
    ) + lpSum(
        yij[(i, j)].varValue * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor
    )

    stats_grande["preco"] = lpSum(
        xij[(i, j)].varValue * df.preco.loc[i, j] * df.quantidade_cesta_grande.loc[i, j]
        for (i, j) in produtores_produtor
    ) + lpSum(
        yij[(i, j)].varValue * df.preco.loc[i, j] * df.quantidade_cesta_grande.loc[i, j]
        for (i, j) in produtores_produtor
    )
    return stats_pequena, stats_grande


def format_df(df, produtores_produtor, xij, yij):
    df_output = []
    for (i, j) in produtores_produtor:
        df_output.append([i, j, (i, j), xij[(i, j)].varValue, yij[(i, j)].varValue])

    df_output = pd.DataFrame(
        df_output, columns=["ID_PRODUTO", "ID_PRODUTOR", "ID", "xij", "yij"]
    ).set_index(["ID_PRODUTO", "ID_PRODUTOR"])

    df_output = pd.merge(
        df_output,
        df,
        left_on=["ID_PRODUTO", "ID_PRODUTOR"],
        right_on=["ID_PRODUTO", "ID_PRODUTOR"],
        how="left",
    )

    return df_output[(df_output["xij"] == 1) | (df_output["yij"] == 1)].sort_values(
        "xij", ascending=False
    )


def cesta_feia(df):

    # Criar conjuntos para os vários tipos de produtos - facilita a construção das restrições
    produtores_produtor = list(df.index.values)

    produtores_produtor_verde = list(df[df.tipo == "verde"].index.values)
    produtores_produtor_fruta = list(df[df.tipo == "fruta"].index.values)
    # produtores_produtor_uni = list(df[df.medida=='Unidade'].index.values)
    # produtores_produtor_kg = list(df[df.medida=='Kg'].index.values)

    # Produtos obrigatórios - produtos marcados pela Fruta Feia como urgentes
    produtor_obrigatorio = list(df[df.urgente].index.values)

    # Definição das variáveis de decisão
    # Produtos das cestas pequenas
    xij = LpVariable.dicts("x", [tuple(c) for c in produtores_produtor], 0, 1, LpBinary)
    # Produto diferenciador das cestas grandes - produto extra apenas utilizados nas cestas grandes
    yij = LpVariable.dicts("y", [tuple(c) for c in produtores_produtor], 0, 1, LpBinary)

    # Incialização do problema a optimizar
    n = 0
    prob = LpProblem("Cesta_Feia_Produtos_Produtores", LpMaximize)

    # Função Objectivo: optimizar rank produto produtor (para já está a minimizar)
    prob += lpSum(
        df.ranking.loc[i, j] * xij[(i, j)] for (i, j) in produtores_produtor
    ) + lpSum(df.ranking.loc[i, j] * yij[(i, j)] for (i, j) in produtores_produtor)

    # Restrição: Número de produtos
    prob += (
        lpSum(xij[(i, j)] for (i, j) in produtores_produtor) == 7,
        "R_numero de produtos 7",
    )
    prob += (
        lpSum(yij[(i, j)] for (i, j) in produtores_produtor) == 1,
        "R_numero de produtos 1",
    )

    # Restrição: produto obrigatório
    if len(produtor_obrigatorio) > 0:
        for (i, j) in produtor_obrigatorio:
            prob += xij[(i, j)] + yij[(i, j)] == 1

    # Restrição: produto diferenciador tem de ser diferente dos outros
    for (i, j) in produtores_produtor:
        prob += xij[(i, j)] + yij[(i, j)] <= 1

    prob.solve()
    if prob.solve() != 1:
        error_msg = "A lista de disponibilidade não tem número suficiente de produtos - 7 cesta pequena e 8 cesta grande"
        return False, error_msg

    else:
        print(LpStatus[prob.status], prob.objective.value())
        n = n + 1
        print("A cesta está a: ", "{0:.0%}".format(n / 5))

    # Restrição: Número mínimo de verdes na cesta pequena > 1
    prob += (
        lpSum(xij[(i, j)] for (i, j) in produtores_produtor_verde) >= 1,
        "R_pelo menos 1 verde",
    )

    prob.solve()
    if prob.solve() != 1:
        error_msg = (
            "A lista de disponibiliade não cumpre o critério - pelo menos 1 verde"
        )
        return False, error_msg

    else:
        print(LpStatus[prob.status], prob.objective.value())
        n = n + 1
        print("A cesta está a : ", "{0:.0%}".format(n / 5))

    # Restrição soft - deal são 3 verdes + 4 frutas
    prob += (
        lpSum(xij[(i, j)] for (i, j) in produtores_produtor_verde)
        >= min(3, len(df[df.tipo == "verde"])),
        "R_n_minimo_verdes",
    )
    prob += (
        lpSum(xij[(i, j)] for (i, j) in produtores_produtor_fruta)
        >= min(4, len(df[df.tipo == "fruta"])),
        "R_n_minimo_frutas",
    )

    prob.solve()
    if prob.solve() != 1:
        error_msg = "Erro na construção ideal de cestas - 3 verdes e 4 frutas"
        return False, error_msg
    else:
        print(LpStatus[prob.status], prob.objective.value())
        n = n + 1
        print("A cesta está a : ", "{0:.0%}".format(n / 5))

    # Restrição Peso: 3-4 kg cestas pequenas
    # estes valores podem ser input da google sheet, porque no verão este valores podem ser inferiores
    peso_cp_min = 3
    peso_cp_max = 4

    prob += (
        lpSum(xij[(i, j)] * df.Peso_CP.loc[i, j] for (i, j) in produtores_produtor)
        >= peso_cp_min
    )
    prob += (
        lpSum(xij[(i, j)] * df.Peso_CP.loc[i, j] for (i, j) in produtores_produtor)
        <= peso_cp_max
    )

    prob.solve()
    if prob.solve() != 1:
        error_msg = "A lista de disponibiliade não cumpre o critério - 3-4 kg para cestas pequenas"
        return False, error_msg

    else:
        print(LpStatus[prob.status], prob.objective.value())
        n = n + 1
        print("A cesta está a : ", "{0:.0%}".format(n / 5))

    # Restrição Peso: 6-8 kg cestas grandes
    # estes valores podem ser input da google sheet, porque no verão este valores podem ser inferiores
    peso_cg_min = 6
    peso_cg_max = 8

    prob += (
        lpSum(xij[(i, j)] * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor)
        + lpSum(yij[(i, j)] * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor)
        >= peso_cg_min
    )

    prob += (
        lpSum(xij[(i, j)] * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor)
        + lpSum(yij[(i, j)] * df.Peso_CG.loc[i, j] for (i, j) in produtores_produtor)
        <= peso_cg_max
    )

    prob.solve()
    if prob.solve() != 1:
        error_msg = "A lista de disponibiliade não cumpre o critério - 6-8 kg para cestas pequenas"
        return False, error_msg
    else:
        print(LpStatus[prob.status], prob.objective.value())
        n = n + 1
        print("A cesta está a : ", "{0:.0%}".format(n / 5))

    stats_pequena_1, stats_grande_1 = stats(
        df,
        produtores_produtor,
        produtores_produtor_verde,
        produtores_produtor_fruta,
        xij,
        yij,
    )
    df_cesta_1 = format_df(df, produtores_produtor, xij, yij)

    # remover um dos produtos anteriormente considerados e construir nova cesta
    prob += (
        lpSum(xij[(i, j)] * xij[(i, j)].varValue for (i, j) in produtores_produtor)
        + lpSum(yij[(i, j)] * xij[(i, j)].varValue for (i, j) in produtores_produtor)
        <= 6
    )

    prob.solve()
    if prob.solve() != 1:
        print(
            "Solução Alternativa - lamentamos mas não foi possível encontrar uma cesta alternativa"
        )
    else:
        print(LpStatus[prob.status], prob.objective.value())

    stats_pequena_2, stats_grande_2 = stats(
        df,
        produtores_produtor,
        produtores_produtor_verde,
        produtores_produtor_fruta,
        xij,
        yij,
    )
    df_cesta_2 = format_df(df, produtores_produtor, xij, yij)

    return [
        {
            "df": df_cesta_1,
            "stats": {"pequena": stats_pequena_1, "grande": stats_grande_1},
        },
        {
            "df": df_cesta_2,
            "stats": {"pequena": stats_pequena_2, "grande": stats_grande_2},
        },
    ]


def clean_data(df):

    # Existem produtos não classificados, para já vou remover, depois devemos completar
    df = df[df["quantidade_cesta_pequena"].notna()]
    df = df[df["quantidade_cesta_grande"].notna()]
    df = df[df["medida"].notna()]

    df["Peso_CP"] = np.where(
        df["medida"] == "Unidade", 0.4, df["quantidade_cesta_pequena"]
    )
    df["Peso_CG"] = np.where(
        df["medida"] == "Unidade", 0.4, df["quantidade_cesta_grande"]
    )

    df = df.set_index(["ID_PRODUTO", "ID_PRODUTOR"])

    return df


def main(df):
    df = clean_data(df)
    return cesta_feia(df)


if __name__ == "__main__":
    df = pd.read_csv("data.csv", index_col=0)
    result = main(df)
"""---------------------------------------------------------------------------------------

# ## Extra
# Preço das cestas deixou de ser restrição na sequência da reunião de 02-06-2021
# estes valores podem ser input da google sheet

delta_preco_cp = 0.05
print(1.5/delta_preco_cp)
print('preco minimo: ', 1.5 - delta_preco_cp)
print('preco minimo: ', 1.5 + delta_preco_cp)

# Restrição Preço: 1,5€ cestas pequenas (igualdade é muito forte!)

prob += lpSum(xij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Pequena'].loc[i,j] \
              for (i,j) in produtores_produtor) >= 1.5 - delta_preco_cp

prob += lpSum(xij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Pequena'].loc[i,j] \
              for (i,j) in produtores_produtor) <= 1.5 + delta_preco_cp


prob.solve()
if prob.solve() != 1:
    print('A lista de disponibiliade não cumpre o critério - preço cestas pequenas')
else:
    print(LpStatus[prob.status], prob.objective.value())

# estes valores podem ser input da google sheet

delta_preco_cg = 0.15
print(3/delta_preco_cg)
print('preco minimo: ', 3 - delta_preco_cg)
print('preco minimo: ', 3 + delta_preco_cg)

# Restrição Preço: 3€ cestas grandes (igualdade é muito forte!)

prob += lpSum(xij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Grande'].loc[i,j] \
              for (i,j) in produtores_produtor) \
      + lpSum(yij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Grande'].loc[i,j] \
              for (i,j) in produtores_produtor) >= 3 - delta_preco_cg

prob += lpSum(xij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Grande'].loc[i,j] \
              for (i,j) in produtores_produtor) \
      + lpSum(yij[(i,j)]*df_disponibilidade['Preço'].loc[i,j]*df_disponibilidade['Quantidade Cesta Grande'].loc[i,j] \
              for (i,j) in produtores_produtor) <= 3 + delta_preco_cg

prob.solve()
if prob.solve() != 1:
    print('A lista de disponibiliade não cumpre o critério - preço €3 para cestas grandes')
else:
    print(LpStatus[prob.status], prob.objective.value())
    
---------------------------------------------------------------------------------------"""
