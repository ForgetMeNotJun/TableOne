import streamlit as st
import pandas as pd

def load_data(uploaded_file, file_type):
    if file_type == 'csv':
        df = pd.read_csv(uploaded_file, encoding = 'utf-8')
        
    elif file_type == 'xlsx (xls)':
        df = pd.read_excel(uploaded_file)  
    
    else: st.error(
        'Only files in csv or xlsx (or xls) format can be uploaded!'
    )
    
    return df

#table split by exposure
def splitTable(dataframe, exposure):
    dataframe[exposure] = dataframe[exposure].map(lambda x:1 if x==True else 0 if x==False else x)
    df_ex = dataframe[dataframe[exposure]== 1]
    df_non = dataframe[dataframe[exposure]== 0]
    return df_ex, df_non

# continuous variables
def makeContinuous(dataframe, continous_col_list):
    df_continuous = pd.DataFrame(columns=continous_col_list, index=['value'])
    for column in continous_col_list:
        #calculate each qx
        dataframe[column] = dataframe[column].astype(float)
        q1 = dataframe[column].quantile(0.25).astype(float)
        q2 = dataframe[column].quantile(0.50).astype(float)
        q3 = dataframe[column].quantile(0.75).astype(float)
        #input value
        df_continuous[column].loc['value'] = f'{round(q2,1)} [{round(q1,1)}-{round(q3,1)}]'
    return df_continuous

def makeCategorical(dataframe, categorical_col_list):
    df_categorical = pd.DataFrame(columns=categorical_col_list, index=['value'])
    for column in categorical_col_list:
        n = dataframe[column].sum()
        rate = n/len(dataframe) *100
        #input value
        df_categorical[column].loc['value'] = f'{int(n)} ({round(rate,1)}%)'
    return df_categorical

def tableOne(dataframe,continous_col_list,categorical_col_list,column_order,label):
    df_continous = makeContinuous(dataframe, continous_col_list)
    df_categorical = makeCategorical(dataframe, categorical_col_list)
    table_one = pd.concat([df_continous,df_categorical], axis=1)
    table_one = table_one[column_order]
    table_one = table_one.T.rename(columns={'value':label})
    return table_one

@st.cache
def convert_df(dataframe):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv()
 
st.title('TableOne')

st.header('''
# 
Upload the preprocessed file with which you'd like to create Table 1.
''')

file_type = st.selectbox(
      			"Which file type would you like to upload: csv or xlsx (xls) ?",
     			('csv', 'xlsx (xls)'),)

uploaded_file = st.file_uploader("", type="csv", key='file_uploader')

if uploaded_file is not None:
    df = load_data(uploaded_file,file_type) 
    st.write(df.head())
    columns_list = list(df.columns)
        
    # select continuous variables
    exposure = st.selectbox(
        "On the basis of which column (exposure) would you like to divide Table 1?",
        columns_list,
    )

    continous_col_list = st.multiselect(
        "Choose all continous variables that you'd like to include in Table 1.",
        columns_list,
        []
    )

    categorical_col_list = st.multiselect(
        "Choose all categorical variables that you'd like to include in Table 1.",
        columns_list,
        []
    )
    
    column_order = st.multiselect(
        "Select the columns in the order in which you'd like to order vertically.",
        continous_col_list + categorical_col_list,
        []
    )
            
    if len(continous_col_list +categorical_col_list)==0:
        st.error('Select at least one column!')
    
    else:
        df_ex, df_non = splitTable(df, exposure)  
        overall_table = tableOne(df,continous_col_list,categorical_col_list, column_order,"overall")
        ex_table = tableOne(df_ex,continous_col_list,categorical_col_list, column_order, "exposure")
        non_table = tableOne(df_non,continous_col_list,categorical_col_list, column_order,"non-exposure")
        
        table_one = pd.concat([overall_table,ex_table], axis=1)
        table_one = pd.concat([table_one,non_table], axis=1)
        download = convert_df(table_one)
        
        if st.button('Make Table 1'):
            st.dataframe(table_one)
            st.download_button(
                label="Download data as csv",
                data=download,
                file_name='Table1.csv',
                #mime='text/csv',
            )