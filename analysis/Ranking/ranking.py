# Import Libraries
import pandas as pd
import numpy as np


# Function to compute the Statistics for a given field
def compute_statistics(df_mapas_campo, field):
    """The purpose of this function is to compute the Statistics: Inverse of the Frequency and Antiquity 
    for a given Field
    
    Input:
    df_mapas_de_campo - A DataFrame containing all the Mapas de Campo that are being considered
    field - A string with the field for which we are computing the Inverse of the Frequency. This will be either 
    produtos or produtor
    
    Output:
    output_dict - A dictionary that contains: keys - each element in field
                                              values - a dictionary containin the inv_frequency and antiquity for that
                                              corresponding element of field
    """
    
    # Computation of the column with Inverse of Frequency for each product: 'inv_frequency'
    
    # The first step consists in the computation of the number of occurrences for each element in 'field'
    df_aux = df_mapas_campo.groupby([field]).agg({'data': [pd.Series.nunique, np.max]}).reset_index()
    df_aux.columns = [field, 'n_occurrences', 'ultima_data']
    
    # Adjust the number of currences so that the minimum value that appears in this column is 1
    df_aux['occurrences_adjusted'] = df_aux['n_occurrences'] - (df_aux['n_occurrences'].min() - 1)
    
    # The Inverse Frequency column is the inverse of the number of occurrences
    df_aux['inv_frequency'] = 1 / df_aux['occurrences_adjusted']
    
    
    # Computation of the column with Antiquity for each product: 'antiquity'
    
    # The first step consists in the computation of the number of days since each element in field was used
    lastweek_date = df_mapas_campo['data'].max()
    df_aux['dias_ultima_cesta'] = (lastweek_date - df_aux['ultima_data']).dt.days
    
    # Antiquity is defined as the normalization of the column 'dias_ultima_cesta'
    oldest_day = df_aux['dias_ultima_cesta'].max()
    df_aux['antiquity'] = df_aux['dias_ultima_cesta'] / oldest_day
    
    
    # Output dictionary
    
    # The first step consists in re-indexing df_aux and choosing only the columns corresponding to the statistics
    df_aux = df_aux.set_index(field)
    df_aux_reduced = df_aux[{'inv_frequency', 'antiquity'}]
    
    # Convert df_aux_reduced into an output and return it
    output_dict = df_aux_reduced.to_dict('index')
    
    return output_dict


# Function to compute the Ranking from the Mapas de Campo
def ranking(df_mapas_campo):
    """The purpose of this function is to use the Mapas de Campo to compute the Ranking.
    
    Input: 
    df_mapas_de_campo - A DataFrame containing all the Mapas de Campo that are being considered in the computation of a
    given week's ranking
    
    Output:
    ranking - A list containing dictionaries. Each dictionary has a pair produtor, produto and the ponctuation given 
    to this pair, thereby resulting in the ranking. The elements of this list are not ordered in any way
    """
    
    # Call the function compute_statistics to obtain the dictionaries with inv_frequency and antiquity for both
    # produtos and produtores/agricultores
    produto_dict = compute_statistics(df_mapas_campo, 'produto')
    agricultor_dict = compute_statistics(df_mapas_campo, 'produtor')
    
    # Create a dictionary with all the unique pairs (Agricultor, Produto)
    df_agric_prod = df_mapas_campo[{'produtor', 'produto'}]
    df_pairs = df_agric_prod.drop_duplicates()
    dict_of_pairs = df_pairs.to_dict('records')
    
    # Compute the Ranking
    ranking = []
    
    for pair in dict_of_pairs:
        pontuacao = (10 / 4) * (agricultor_dict[pair['produtor']]['inv_frequency'] + 
                                agricultor_dict[pair['produtor']]['antiquity'] + 
                                produto_dict[pair['produto']]['inv_frequency'] +
                                produto_dict[pair['produto']]['antiquity'])
        ranked_dict = {'produtor': pair['produtor'], 'produto': pair['produto'], 'pontuacao': pontuacao}
        ranking.append(ranked_dict)
    
    return ranking