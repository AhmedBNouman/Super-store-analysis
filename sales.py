import streamlit as st
import pandas as pd
import plotly.express as px
st.image('super.png')
st.title('Super Store Analysis')
df=pd.read_csv('df_new',index_col=0)
st.sidebar.header('sidebar for sales analysis')
select=st.sidebar.selectbox('select',['univariate','Bivariate','multivariate'])
st.sidebar.subheader("Filter Options")
Region = st.sidebar.multiselect("Filter by Region", df["Region"].unique(), default=df["Region"].unique())
df['Date'] = pd.to_datetime(df['Order Date'])
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
df = df[(df["Region"].isin(Region)) & (df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]
st.dataframe(df.head())
numeric_cols = df.select_dtypes(['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include='object').columns.tolist()
if select=='univariate':
    col_type = st.radio("Select column type", ['Numeric', 'Categorical'])
    if col_type == 'Numeric':
        col = st.selectbox('Select numeric column', numeric_cols)
        chart=st.selectbox('select',['histogram','box'])
        if chart == 'histogram':
            st.plotly_chart(px.histogram(data_frame= df, x= col, title= col,text_auto=True))
        elif chart =='box':
            st.plotly_chart(px.box(data_frame= df, x= col, title= col))
    elif col_type == 'Categorical':
        col = st.selectbox('Select categorical column', categorical_cols)
        chart=st.selectbox('select',['histogram','pie'])
        if chart =='histogram':
            st.plotly_chart(px.histogram(data_frame= df, x= col, title= col,text_auto=True))
        elif chart =='pie':
            st.plotly_chart(px.pie(data_frame= df, names= col, title= col))
       
            
elif select=='Bivariate':
    st.header('Q1: What is the relationship between Discount and Profit?')
    st.plotly_chart(px.scatter(data_frame=df,y='Discount',x='Profit'))
    st.header('Q2: Does the Category affect the total Sales ?') 
    c_s=df.groupby('Category')['Sales'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=c_s, x='Category',y='Sales',text_auto=True))
    st.header('Q3: How does Ship Mode influence Profit?')
    st.plotly_chart(px.box(data_frame=df, x='Ship Mode', y='Profit', color='Ship Mode',title='Profit by Ship Mode'))
    st.header('Q4: Which regions has the highest product demand?')
    r_Q=df.groupby('Region')['Quantity'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=r_Q, x='Region', y='Quantity', color='Region',text_auto=True, title='Quantity Sold by Region'))
    st.header('Q5: Is there a difference in total Profit between customer Segments?')
    s_B=df.groupby('Segment')['Profit'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=s_B,x='Segment',y='Profit',text_auto=True))
    st.header('Q6: what the mean of ship deelay between ship mode?')
    s_S=df.groupby('Ship Mode')['Ship Delay'].mean().reset_index().round()
    st.plotly_chart(px.bar(data_frame=s_S,x='Ship Mode',y='Ship Delay',text_auto=True))
    st.header('Q7: what the top 10 customers made orders?')
    c_C=df.groupby('Customer Name')['Quantity'].count().reset_index().sort_values(by='Quantity',ascending=False).head(10)
    st.plotly_chart(px.bar(data_frame=c_C,x='Customer Name',y='Quantity',text_auto=True,labels={'Quantity':'count of orders'},title='top 10 cuctomers made ordres'))
   
    
else :
    st.header('Q1:which category is higher sales in each region?')
    c_r_s=df.groupby(['Category','Region'])['Sales'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=c_r_s, x='Category', y='Sales', color='Region', barmode='group',text_auto=True, title='Sales by Category and Region'))
    st.header('Q2: what the Profit in Sub-Category within Each Category')
    st.plotly_chart(px.box(df, x='Sub-Category', y='Profit', color='Category', title='Profit by Sub-Category within Each Category'))
    st.header('Q3: what the Monthly Sales Trend by Year ?')
    m_y_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    st.plotly_chart(px.line(m_y_sales, x='Month', y='Sales', color='Year',title='Monthly Sales Trend by Year'))
    st.header('Q4: what the Shipping Delay by Ship Mode and Category ?') 
    st.plotly_chart(px.box(df, x='Ship Mode', y='Ship Delay', color='Category',title='Shipping Delay by Ship Mode and Category'))
    st.header('Q5:what the profit for each segment in each region ?')
    s_R_p=df.groupby(['Segment','Region'])['Profit'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=s_R_p,x='Segment',y='Profit',color='Region',barmode='group',text_auto=True,title='the profit for each segment in each region'))
    
