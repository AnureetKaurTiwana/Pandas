#!/usr/bin/env python
# coding: utf-8

# # Test Attendance Analysis
# There are two Datasets: 
# 1. Attendance Data
# 2. Test Data
# 
# From Attendance Data - find the active users
# From Test Data find the number of users who appeared for tests and find the count at board,grade and subject level.
# 
# <b>  Agenda: Find the test attendance percentage at board and grade level </b>
# 
# Functions Used: read_csv, to_csv, df.drop(), df.merge(),groupby(),subplot(), bar(),
# sns.displot(), lambda, apply()

# In[37]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


file=pd.read_csv(r"C:\Users\Tnluser\Downloads\AttendanceAnalysis.csv")


# In[3]:


file2=file.drop_duplicates(subset=['PREMIUM_ACCOUNT_ID'],keep="last")
file2['PREMIUM_ACCOUNT_ID'].value_counts()


# In[4]:


file2


# In[5]:


file2


# In[5]:


file2['PREMIUM_ACCOUNT_ID']


# In[7]:


file2['ATTENDANCE %'].dtype


# In[8]:


def convert(data):
    return float(data[:len(data)-1])

file2['ATTENDANCE %']=file2['ATTENDANCE %'].apply(convert) 
    


# In[9]:


file2['ATTENDANCE %'].dtype


# In[9]:



df2 = file2[file2['ATTENDANCE %']>0]
df2.head()


# In[10]:


file2['ATTENDANCE %'].count()


# In[11]:


file2.to_csv(r"attendance.csv")


# In[11]:


test=pd.read_csv(r"C:\Users\Tnluser\Downloads\20Aug.csv")
test.head()


# ## Analysing test data

# In[12]:



#Number of  students who took test board, grade and subject level
df2=test.groupby(['board','grade','subject'])['rollNo'].count().reset_index()
df2.head()


# In[15]:


#Attendace data analysis- How many active students are there in each board an 
df3=file2.groupby(['SYLLABUS','GRADE'])['PREMIUM_ACCOUNT_ID'].count().reset_index()
df3.head()


# In[21]:


#renaming columns to match with test column names
df3.columns=['board','grade','PID']
df3.head()


# ### Joining two dataframes 
# Creating foreign key to join these two dataframes.

# In[22]:


df2['helper']=df2['board']+'Standard '+df2['grade']
df2.head(2)


# In[23]:


df3['helper']=df3['board']+df3['grade']
df3.head(2)


# In[24]:


df4=df2.merge(df3, on='helper', how='left')
df4.head(2)


# ### Droping the not required columns

# In[25]:


df4.drop(columns=['helper','board_y','grade_y'],inplace=True)


# In[27]:


df4.head(2)


# In[28]:


df4.rename(columns={'board_x':'board','grade_x':'grade','rollNo':'Test_Taker_Count','PID':'ActiveUsers'},inplace=True)


# ## What percent of active users have  taken the test?

# In[33]:


df4['Test_Attendance']=(df4['Test_Taker_Count']/df4['ActiveUsers'])*100
df4['Test_Attendance']=df4['Test_Attendance'].apply(lambda x: round(x,2))


# In[34]:


df4.head()


# ### Plot Test Attendance vs Board

# In[32]:


fig, ax = plt.subplots()
ax.bar(df4['board'],df4['Test_Attendance'],width=0.4)
ax.set_ylabel('Test_Attendance %')
ax.set_xlabel('Board')


# ## Plot Test Attendance Vs Grade

# In[28]:


fig, ax = plt.subplots()
ax.bar(df4['grade'],df4['Test_Attendance'],width=0.4)
ax.set_ylabel('Test_Attendance %')
ax.set_xlabel('grade')


# In[36]:


df4['Test_Attendance']=df4['Test_Attendance'].apply(float)
df4['Test_Attendance'].quantile([0.25, 0.5, 0.75])


# In[60]:



sns.displot(df4['Test_Attendance'], kind='kde')

plt.axvline(x = df4['Test_Attendance'].median(),# Line on x = 2
        
           ymin = 0, # Bottom of the plot
           ymax = 1)
plt.xlim(0,df4['Test_Attendance'].max()+20)


# In[68]:


test.head(5)


# In[75]:


df5=test.groupby('rollNo')['assessment[0].tllmsAssessmentId'].count().reset_index()
df5.rename(columns={'rollNo':'rollNo','assessment[0].tllmsAssessmentId':'assessmentID'},inplace=True)


# In[108]:


type(df5)


# In[84]:


df6=df5[df5['assessmentID']==2].reset_index()
df6.head()


# In[86]:


df6.drop(columns={'index'},inplace=True)


# In[88]:


df6.head()


# In[90]:


test.rename(columns={'assessment[0].tllmsAssessmentId':'assessmentID'},inplace=True)


# In[91]:


test.head(2)


# In[123]:


df7=test[['assessmentID','board','grade','subject']]
df7.head(2)


# In[124]:


df8=df7.groupby(['board','grade','subject'])['assessmentID'].count().reset_index()


# In[125]:


df8.rename(columns={'assessmentID':'count_assessment_ID'},inplace=True)


# In[126]:


df8.head(2)


# In[131]:


df8.pivot(index=['board','grade'],columns='subject',values='count_assessment_ID').fillna(0)


# In[ ]:




