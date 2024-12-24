#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# In[2]:


data = pd.read_csv('online_retail_II.csv')


# In[3]:


st.title("Customer Segmentation and Behavioural Analysis Dashboard")


# In[4]:


data


# In[5]:


data.info()


# In[6]:


data['InvoiceDate']=pd.to_datetime(data['InvoiceDate'],errors='coerce')


# In[7]:


data.describe()


# In[8]:


data.isnull().sum()


# In[9]:


data.shape


# In[10]:


data.dropna(inplace = True)


# In[11]:


data.shape


# In[12]:


data.isnull().sum()


# In[13]:


data['Invoice'].nunique()


# In[14]:


data['Customer ID'].nunique()


# In[15]:


# Group data by date and count the number of invoices per date
daily_invoices = data.groupby(data['InvoiceDate'].dt.date)['Invoice'].count()

# Plot the number of invoices over time
plt.figure(figsize=(12, 6))
plt.plot(daily_invoices.index, daily_invoices.values, marker='o', color='b')
plt.title("Number of Invoices Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Invoices")
plt.xticks(rotation=45)
plt.show()
st.pyplot(plt.gcf())


# In[16]:


plt.figure(figsize=(12, 6))
sns.histplot(data['InvoiceDate'], bins=40, kde=True)  # Adjust bins as needed
plt.title("Distribution of Invoices by Date")
plt.xlabel("Invoice Date")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()
st.pyplot(plt.gcf())


# In[41]:


purc_count = data.groupby('Customer ID')['Invoice'].nunique()

# Sidebar options
options = ["Top 10", "Top 30", "Top 50", "Bottom 10"]
selection = st.sidebar.selectbox("Select a Customer Group:", options)

# Determine the number of customers to display based on selection
num_customers = int(selection.split(" ")[1])
order = selection.split(" ")[0].lower()

# Select top or bottom customers
if order == "top":
    selected_customers = purc_count.sort_values(ascending=False).head(num_customers)
else:
    selected_customers = purc_count.sort_values(ascending=True).head(num_customers)

# Plot the selected customers' purchase counts
plt.figure(figsize=(14, 8))
selected_customers.plot(kind='bar', color='skyblue')

plt.title(f"{selection} Customers with Purchase Counts", fontsize=16)
plt.xlabel("Customer ID", fontsize=12)
plt.ylabel("Number of Purchases", fontsize=12)
plt.xticks(rotation=90)

# Display the plot in Streamlit
st.pyplot(plt.gcf())


# In[19]:


data['T_Price']=data['Price']*data['Quantity']


# In[20]:


data.info()


# In[21]:


data.shape


# In[22]:


data.groupby('Description').agg({'Quantity':'sum'}).sort_values('Quantity',ascending=False)


# In[23]:


data.groupby('Invoice').agg({'T_Price':'sum'})


# In[24]:


data = data[~data['Invoice'].str.contains('C',na=False)]


# In[25]:


data.shape


# In[26]:


print('Farthest Time: ',data['InvoiceDate'].max())
print('Nearest Time: ',data['InvoiceDate'].min())


# In[27]:


from datetime import date

# Get today's date
today_date = pd.to_datetime(date.today())

# Perform RFM aggregation
rfm = data.groupby('Customer ID').agg({
    'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,  # Recency
    'Invoice': lambda Invoice: Invoice.nunique(),  # Frequency
    'T_Price': lambda T_Price: T_Price.sum()  # Monetary
})

# Rename the columns to recency, frequency, and monetary
rfm.columns = ["recency", "frequency", "monetary"]



# In[28]:


rfm.describe()


# In[29]:


rfm['Rs'] = pd.qcut(rfm['recency'],5,labels=[5,4,3,2,1])
rfm['Fs'] = pd.qcut(rfm['frequency'].rank(method='first'),5,labels=[1,2,3,4,5])
rfm['Ms'] = pd.qcut(rfm['monetary'].rank(method='first'),5,labels=[1,2,3,4,5])
rfm['RF_Score'] = (rfm['Rs'].astype(str) + rfm['Fs'].astype(str))



# In[30]:


Max_rf_score = rfm['RF_Score'].sort_values(ascending=False).head(50)


# In[31]:


rfm.describe()


# In[32]:


rfm['RF_Score'] = pd.to_numeric(rfm['RF_Score'], errors='coerce')


# In[33]:


top_rows = rfm.nlargest(20, 'RF_Score')

st.title("RF Score Analysis")
st.write("Top 20 rows with the maximum RF_Score:")
st.dataframe(top_rows)


# In[35]:


rfm['RF_Category'] = pd.qcut(rfm['RF_Score'], 3, labels=["Low", "Medium", "High"])


# In[36]:


rfm.info()


# In[37]:


rfm


# In[38]:


rfm_category_counts = rfm['RF_Category'].value_counts()

# Plotting the bar plot using seaborn
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

# Create a bar plot
ax=sns.barplot(x=rfm_category_counts.index, y=rfm_category_counts.values, palette='Set3')
for bars in ax.containers:
    ax.bar_label(bars)

# Adding titles and labels
plt.title('Number of Customers in Each RF Category', fontsize=16)
plt.xlabel('RF Category', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)

# Show the plot
plt.show()


# In[39]:


st.title("RF Category Analysis")
st.write("### Number of Customers in Each RF Category")

# Display the counts in a table
st.write(rfm_category_counts)

# Plotting the bar plot
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

# Create a bar plot
ax = sns.barplot(x=rfm_category_counts.index, y=rfm_category_counts.values)

# Adding bar labels
for bars in ax.containers:
    ax.bar_label(bars)

# Adding titles and labels
plt.title('Number of Customers in Each RF Category', fontsize=16)
plt.xlabel('RF Category', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)

# Streamlit chart display
st.pyplot(plt)


# In[ ]:





# In[ ]:




