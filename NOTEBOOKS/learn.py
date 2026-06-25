#---------------------- learn pandas with me ------------------------------

import pandas as pd 


#------series in pandas-------------

a = {"name" : "nency", "age" : 20, "city" : "new york"}
myvar = pd.Series(a)
print(myvar[1])

#-----------------------series with index------------------------------
b = [10,20,30,40,50]
myvar2 = pd.Series(b,index = ["a","b","c","d","e"])
print(myvar2["c"])


#-----------------------dataframe in pandas------------------------------

data = {
    "calories" : [420,380,390,400,410],
    "duration" : [50,40,45,55,60]
}

df = pd.DataFrame(data)
print(df)

#------------------- name the index(each row)------------------------------
import pandas as pd 

data = {
    "calories" : [420,380,390,400,410],
    "duration" : [50,40,45,55,60]
}

df = pd.DataFrame(data, index = ["D-1","D-2","D-3","D-4","D-5"])
print(df)
print(df.loc["D-2"])                         #loc is used to access a group of rows and columns by label(s) or a boolean array.




#------------------------------------------------------------------- read csv file in pandas-----------------------------------------------------------------------------------------

import pandas as pd

df = pd.read_csv("C:\\Users\\vrutupatel\\OneDrive\\Desktop\\python\\practice data.csv")


# print(df)  # this will return the first 5 rows of the dataframe by default, if you want to see all the rows then you can use to_string() method.

# print(df.to_string())  

# # if u dont want to use to_string() method then you can change the max_rows option in pandas to display all the rows.

# pd.options.display.max_rows = 1000
# print(df)  # this will return all the rows of the dataframe.


print(df.info())  # this will return information about the dataframe, including the number of rows and columns, data types, and memory usage.








#--------------------cleaning data in pandas------------------------------

import pandas as pd

df = pd.read_csv("C:\\Users\\vrutupatel\\OneDrive\\Desktop\\python\\practice data.csv")
# print(df.to_string())

# new_df = df.dropna()
# print(new_df.to_string())  # this will return a new dataframe with all the rows that contain missing values removed.
  
df.fillna(130, inplace = True) # this will fill all the missing values with 130 in the original dataframe.
print(df.to_string())





#----------------------replace with mean value---------------------------------

import pandas as pd

df = pd.read_csv("C:\\Users\\vrutupatel\\OneDrive\\Desktop\\python\\practice data.csv")
# print(df.to_string())

