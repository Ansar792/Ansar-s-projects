# Ansar-s-projects
# project 1 - YouTube Data Harvesting and Warehousing using SQL and Streamlit
# coding description listed below
Line #3 : youtube API key declarion
Line #7-10 : required Libraries import such as Google API client, Pandas, PPrint and streamlit
Line #14-16 : Youtube API extract setup
Line #22-38 : defining function for creating "Channal" table using pandas dataframe
Line #42-80 : defining function for creating "Video" table using pandas datafram
Line #84 - 122 : defining function for creating "comment" table. Used Try - Except block in order to avoid errors as there were few youtube channels are disabled for comment
Line #127-128 : streamlit title and header declaration
Line #131 : getting channel ID input from user through streamlit text input function
Line # 136-154 : construction of DataFrames for Channal, Video and comment details using the input and calling above defined functions
Line #158-165 : displaying dataframe details in web application using streamlit Write function
Line #170-178 : inserting dataframes of channal, video and comment tables into MYSQL using sqlalchemy connector
Line #182-211 : getting data extract using MYSQL in python by pandas "read_sql_query" function
