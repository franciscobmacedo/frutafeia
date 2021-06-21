# Import Libraries
import pandas as pd
import numpy as np


# Function to obtain the Adjusted Ranking from the original Ranking
def adjusted_ranking(df_ranking):
    """The purpose of this function is to re-organize the ranking and present it with a new order

    Input:
    ranking - A list corresponding to the ranking that was computed in the function 'ranking'

    Output:
    ranking_ajustado - A list containing dictionaries. This list corresponds to the adjusted ranking
    """

    # Creation of a list containing the Produtor, ordered by the maximum of Pontuacao that the Produtor gets in any
    # of its pairs

    # Transform the structure and contents of the Ranking DataFrame into something that can be useful
    df_ranking_usable = df_ranking.groupby(["produtor"]).max()
    df_ranking_usable = df_ranking_usable.reset_index()

    df_ranking_usable = df_ranking_usable[{"produtor", "pontuacao"}]
    df_ranking_usable = df_ranking_usable.sort_values("pontuacao", ascending=False)

    # Create the list
    lista_prod = df_ranking_usable["produtor"].tolist()

    # Create a DataFrame that has the ranking sorted by the name of the Produtor and that
    # for each Produtor, is sorted by the Pontuacao each of its Produtos has

    sorted_ranking = df_ranking.sort_values(
        by=["produtor", "pontuacao"], ascending=False
    )

    # Create the final Adjusted Ranking

    ranking_ajustado = []

    for produtor in lista_prod:
        auxiliary_dict = {}
        auxiliary_dict["produtor"] = produtor
        auxiliary_dict["produtos"] = (
            sorted_ranking.loc[sorted_ranking["produtor"] == produtor][
                {"produto", "pontuacao"}
            ]
        ).to_dict("records")
        ranking_ajustado.append(auxiliary_dict)

    return ranking_ajustado
