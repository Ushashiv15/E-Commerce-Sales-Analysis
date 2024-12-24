#!/usr/bin/env python
# coding: utf-8

# In[98]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display
import plotly.express as px
import streamlit as st


# In[99]:


data = pd.read_csv("Amazon Sale Report (1).csv",low_memory = False)


# In[100]:


st.title("Amazon Data Analysis Dashboard")


# In[101]:


data


# In[102]:


data.shape


# In[103]:


data.isnull().sum()


# In[104]:


data.drop(['New','PendingS'], axis=1, inplace=True)


# In[105]:


data.describe()


# In[106]:


pd.isnull(data).sum()


# In[107]:


data = data.dropna(subset=['currency'])


# In[108]:


data.info()


# In[109]:


pd.isnull(data).sum()


# In[110]:


data = data.dropna(subset=['ship-postal-code'])


# In[111]:


data['Date'] = pd.to_datetime(data['Date'],dayfirst = True)
data = data.set_index('Date')
data['year'] = data.index.year
data['month'] = data.index.month
data['day'] = data.index.day


# In[112]:


data['ship-postal-code']=data['ship-postal-code'].astype('int')


# In[113]:


data.info()


# In[130]:


ax=sns.countplot(x='Size' ,data=data)
ax.set_title('Size Analysis')

for bars in ax.containers:
    ax.bar_label(bars)
plt.show()
st.pyplot(plt.gcf())


# In[115]:


st.sidebar.header("Filter Options")
selected_category = st.sidebar.selectbox(
    "Select a Category:", 
    options=data['Category'].unique(), 
    key="unique_category_select"
)


# In[116]:


# Function to display sizes by category
def display_sizes_by_category(category):
    category_data = data[data['Category'] == category]
    category_sizes = category_data.groupby('Size')['Qty'].sum()

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(category_sizes.index.astype(str), category_sizes.values, marker='o', color='purple')
    plt.title(f'Sizes for each Category: {category}')
    plt.xlabel('Size')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

# Call the function with the selected category
display_sizes_by_category(selected_category)


# In[132]:


ax=sns.countplot(x='Category' ,data=data)
ax.set_title('Category Analysis')

for bars in ax.containers:
    ax.bar_label(bars)
plt.show()
st.pyplot(plt.gcf())


# In[118]:


# Function to display sizes by category
def display_sales_by_category(category):
    category_data = data[data['Category'] == category]
    category_sales = category_data.groupby('month')['Amount'].sum()

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(category_sales.index.astype(str), category_sales.values, marker='o', color='purple')
    plt.title(f'Sales Trend for Category: {category}')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

# Call the function with the selected category
display_sales_by_category(selected_category)


# In[119]:


data['Courier Status'].unique()


# In[134]:


plt.figure(figsize=(12,7))
ax = sns.countplot(data = data, x='Courier Status',hue='Status')
plt.show()
st.pyplot(plt.gcf()) 


# In[139]:


B2B_Check = data['B2B'].value_counts()
plt.title('Business to Business Analysis')

plt.pie(B2B_Check, labels=B2B_Check, autopct='%1.1f%%')
plt.axis('equal')
plt.show()


# In[137]:


# Plot the pie chart
fig, ax1 = plt.subplots()
ax1.pie(B2B_Check, labels=B2B_Check.index, autopct='%1.1f%%', startangle=90)
ax1.set_title('Business to Business Analysis')
ax1.axis('equal')  # Ensure the pie chart is circular

# Display the plot in Streamlit
st.pyplot(fig)


# In[140]:


fb = data['Fulfilment'].value_counts()
plt.title('Fulfillment Analysis')
plt.pie(fb, labels=fb.index, autopct='%1.1f%%')
plt.axis('equal')
plt.show()


# In[141]:


# Plot the pie chart
fig1, ax2 = plt.subplots()
ax2.pie(fb, labels=fb.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('Fulfillment Analysis')
ax2.axis('equal')  # Ensure the pie chart is circular

# Display the plot in Streamlit
st.pyplot(fig1)


# In[123]:


plt.figure(figsize=(12,6))
sns.countplot(data = data, x='ship-state')
plt.xlabel('States')
plt.ylabel('Count')
plt.title('Shipment of product in each state')
plt.xticks(rotation=90)
plt.show()
st.pyplot(plt.gcf())


# In[135]:


selected_state = st.sidebar.selectbox("Select a State:", options=data['ship-state'].unique())
#selected_category = st.sidebar.selectbox("Select a Category:", options=data['Category'])

# Filter data
filtered_data = data[(data['ship-state'] == selected_state) & (data['Category'] == selected_category)]

# Aggregate quantity by Size
aggregated_data = filtered_data.groupby(['Size']).agg({'Qty': 'sum'}).reset_index()

st.write(f"### Shipment Quantities in {selected_state} for {selected_category}")

# Check if there's data to display
if not aggregated_data.empty:
    # Create bar plot
    fig = px.bar(
        aggregated_data,
        x='Size',
        y='Qty',
        color='Size',
        title=f"Shipment Quantities by Product Size in {selected_state} for {selected_category}",
        labels={'Qty': 'Quantity', 'Size': 'Product Size'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for the selected filters.")

# Additional Insights
st.sidebar.markdown("### Additional Insights")
if st.sidebar.checkbox("Show Data Summary"):
    st.write("#### Data Summary")
    st.write(aggregated_data.describe())


# In[ ]:




