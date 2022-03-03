def id_mapper(df, col_name):
    '''
    INPUT:
    df - DataFrame
    col_name - string, column name to be mapped

    OUTPUT:
    encoded_list - list, new numerical values for the column: [1, 2, 3, ...]
    '''

    coded_dict = dict()
    counter = 1
    encoded_list = []
    
    for val in df[col_name]:
        if val not in coded_dict:
            coded_dict[val] = counter
            counter+=1
        
        encoded_list.append(coded_dict[val])
    return encoded_list


def encode_id(df, old_col_name, new_col_name):
    '''
    INPUT:
    df - DataFrame
    old_col_name - string, column name to be mapped
    new_col_name - string, column name for new values

    OUTPUT:
    new_df - DataFrame, with added new column new_col_name and removed old_col_name
    '''

    df[new_col_name] = id_mapper(df, old_col_name)
    new_df = df.drop(columns=old_col_name)
    return new_df
