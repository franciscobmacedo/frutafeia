# Import Libraries
import pandas as pd
import numpy as np


# Function to obtain the Adjusted Ranking from the original Ranking
def adjusted_ranking(ranking):
    """The purpose of this function is to re-organize the ranking and present it with a new order
    
    Input:
    ranking - A list corresponding to the ranking that was computed in the function 'ranking'
    
    Output:
    ranking_ajustado - A list containing dictionaries. This list corresponds to the adjusted ranking
    """
    
    # Begin by converting the list with the ranking into a DataFrame so that we can use pandas' libraries
    df_ranking = pd.DataFrame(ranking)
    
    
    # Creation of a list containing the Produtor, ordered by the maximum of Pontuacao that the Produtor gets in any
    # of its pairs
    
    # Transform the structure and contents of the Ranking DataFrame into something that can be useful
    df_ranking_usable = df_ranking.groupby(['Produtor']).max()
    df_ranking_usable = df_ranking_usable.reset_index()
    
    df_ranking_usable = df_ranking_usable[{'Produtor', 'Pontuacao'}]
    df_ranking_usable = df_ranking_usable.sort_values('Pontuacao', ascending = False)
    
    # Create the list
    lista_prod = df_ranking_usable['Produtor'].tolist()
    
    
    # Create a DataFrame that has the ranking sorted by the name of the Produtor and that
    # for each Produtor, is sorted by the Pontuacao each of its Produtos has
    
    sorted_ranking = df_ranking.sort_values(by = ['Produtor', 'Pontuacao'], ascending = False)
    
    
    # Create the final Adjusted Ranking
    
    ranking_ajustado = []
    
    for produtor in lista_prod:
        auxiliary_dict = {}
        auxiliary_dict['Produtor'] = produtor
        auxiliary_dict['Produtos'] = (sorted_ranking.loc[sorted_ranking['Produtor'] == produtor]
                                      [{'Produto', 'Pontuacao'}]).to_dict('records')
        ranking_ajustado.append(auxiliary_dict)
    
    return ranking_ajustado