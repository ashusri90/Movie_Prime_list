
# coding: utf-8

# # PRIME TIME

# ## Problem: 
# 
#     - We need to find the time slot which has the most tickets sold

# ## Disclaimer:
# As time slots are relative to day (date), not week, **movie_run_date** is used to create window in which we have to find the time_slot having maximum number of tickets sold.

# In[33]:

import logging

from pyspark.sql.functions import when, row_number, col, desc
from pyspark.sql.window import Window


# In[43]:

reload(logging)


# In[44]:

app_name = "PRIME_TIME"
logging.basicConfig(
    format='{} %(asctime)s %(levelname)s:%(message)s'.format(app_name),
    level=logging.DEBUG, 
    datefmt='%I:%M:%S'
)

logger = logging.getLogger(name=app_name)

logging.getLogger("py4j").setLevel(logging.ERROR)


# In[56]:

## Functions

def get_prime_time(df):
    """
    Function to tag prime time slot for a movie.
    
    Args:
        df {pyspark.sql.DataFrame}: Input dataframe
    
    Returns:
        {pyspark.sql.DataFrame}: Dataframe with prime time tagging.
    """
    df_rank =  df.withColumn(
        "rank",
        row_number().over(Window.partitionBy("movie_id", "week","movie_run_date")
                          .orderBy(desc("number_of_tkts_sold"), desc("movie_start_time")))
    )
    
    return df_rank         .withColumn("is_prime_time", when(col("rank") == 1, "TRUE").otherwise("FALSE"))         .drop("rank")


# 
# ### Creating schema of dataset 

# In[38]:

movie_schema = ('movie_id', 
                'movie_start_time',
                'movie_end_time', 
                'movie_run_date',
                'week', 
                'year',
                'theatre_name', 
                'state',
                'city',
                'country',
                'number_of_tkts_sold')


# ### Data Set with single week 

# In[39]:

data = [(1,"12:00:00","15:00:00","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (1,"12:00:00","15:00:00","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (1,"12:00:00","15:00:00","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (1,"12:00:00","15:00:00","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (1,"12:00:00","15:00:00","11/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","11/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","11/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","11/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (1,"12:00:00","15:00:00","12/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","12/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","12/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","12/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",120000)]


# In[45]:

logger.info("Reading dataset")
movie_data = sqlContext.createDataFrame(data, movie_schema)


# In[50]:

logger.debug("Ranking time based on %s" % "number_of_tkts_sold")
df_out = get_prime_time(movie_data)


# In[71]:

df_out.sort("movie_id","week").show(30)


# In[ ]:




# ## Data set 2: with multiple weeks

# In[66]:

data_2 = [(1,"12:00:00","15:00:00","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (1,"15:00:00","18:00:00","07/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (1,"18:00:00","21:00:00","07/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (1,"21:00:00","23:59:59","07/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (2,"12:00:00","15:00:00","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (2,"15:00:00","18:00:00","08/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (2,"18:00:00","21:00:00","08/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (2,"21:00:00","23:59:59","08/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (3,"12:00:00","15:00:00","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (3,"15:00:00","18:00:00","09/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (3,"18:00:00","21:00:00","09/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (3,"21:00:00","23:59:59","09/10/19",39,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (4,"12:00:00","15:00:00","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (4,"15:00:00","18:00:00","10/10/19",38,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (4,"18:00:00","21:00:00","10/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (4,"21:00:00","23:59:59","10/11/19",39,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (4,"12:00:00","15:00:00","11/09/19",37,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (4,"15:00:00","18:00:00","11/09/19",37,2019,"Inox","Maharashtra","Mumbai","India",5000),
        (4,"18:00:00","21:00:00","11/12/19",40,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (4,"21:00:00","23:59:59","11/06/19",33,2019,"Inox","Maharashtra","Mumbai","India",120000),
        (4,"12:00:00","15:00:00","12/06/19",33,2019,"Inox","Maharashtra","Mumbai","India",1000),
        (4,"15:00:00","18:00:00","12/05/19",32,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (4,"18:00:00","21:00:00","12/05/19",32,2019,"Inox","Maharashtra","Mumbai","India",10000),
        (4,"21:00:00","23:59:59","12/05/19",32,2019,"Inox","Maharashtra","Mumbai","India",10000)]


# In[67]:

logger.info("Reading dataset")
movie_data_2 = spark.createDataFrame(data_2, movie_schema)


# In[68]:

logger.debug("Ranking time based on %s" % "number_of_tkts_sold")
df_out2 = get_prime_time(movie_data_2)


# In[70]:

df_out2.sort("movie_id","week").show(30)


# In[ ]:




# In[ ]:




# In[ ]:



