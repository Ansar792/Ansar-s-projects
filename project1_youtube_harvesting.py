#API key declaraion

api_key = 'AIzaSyBdt7DAQkBBZWsVMvrQkRtytiXg3Gb61dQ'

#required Libraries import

import googleapiclient.discovery
import pandas as pd
from pprint import pprint
import streamlit as st

#Youtube API extract setup

api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)



# Channel Function defination

def channel(ch_ID):
  request = youtube.channels().list(part="snippet,contentDetails,statistics",id=ch_ID)
  response = request.execute()
  channel_ID = response['items'][0]['id']
  channel_name = response['items'][0]['snippet']['title']
  channel_type = response['kind']
  channel_views = response['items'][0]['statistics']['viewCount']
  channel_description = response['items'][0]['snippet']['description']
  channel_status = 'Active'

  ch_df = pd.DataFrame({'channel_ID':[channel_ID],
                      'channel_name':[channel_name],
                      'channel_type':[channel_type],
                      'channel_views':[channel_views],
                      'channel_description':[channel_description],
                      'channel_status':[channel_status]})
  return ch_df

#Taking Video IDs for Video table / video data Function defination

def video(ch_ID):
  video_ids = []
  response = youtube.channels().list(part="snippet,contentDetails,statistics",id=ch_ID).execute()
  playlist_ID = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
  responce_2 = youtube.playlistItems().list(part='snippet',playlistId=playlist_ID,maxResults=25).execute()

  for i in range(len(responce_2['items'])):
    video_ids.append(responce_2['items'][i]['snippet']['resourceId']['videoId'])

  vid_data = pd.DataFrame()
  for i in video_ids:
    response_3 = youtube.videos().list(part="snippet,contentDetails,statistics",id=i).execute()
    video_name = response_3['items'][0]['snippet']['title']
    video_descrition = response_3['items'][0]['snippet']['description']
    video_published_date = response_3['items'][0]['snippet']['publishedAt']
    vid_view_count = response_3['items'][0]['statistics']['viewCount']
    vid_like_count = response_3['items'][0]['statistics']['likeCount']
    vid_fav_count = response_3['items'][0]['statistics']['favoriteCount']
    vid_comment_count = response_3['items'][0]['statistics']['commentCount']
    vid_caption_status = response_3['items'][0]['contentDetails']['caption']
    vid_duration = response_3['items'][0]['contentDetails']['duration']

    vid_df = pd.DataFrame ({'channel_ID' : [ch_ID],
                            'playlist_ID' : [playlist_ID],
                            'video_ID': [i],
                            'video_name' : [video_name],
                            'video_descrition' : [video_descrition],
                            'video_published_date' : [video_published_date],
                            'vid_view_count' : [vid_view_count],
                            'vid_like_count' : [vid_like_count],
                            'vid_dislike_count' : "disabled",
                            'vid_fav_count' : [vid_fav_count],
                            'vid_comment_count':[vid_comment_count],
                            'vid_caption_status':[vid_caption_status],
                            'vid_duration': [vid_duration]})

    vid_data = pd.concat([vid_data,vid_df])

  return vid_data

#Comment Data function Definition

def comment(vid_ID):

  comment_data = pd.DataFrame()
  try:
    request = youtube.commentThreads().list(part = "snippet", videoId=vid_ID,maxResults = 25)
    response = request.execute()

    for i in range(len(response['items'])):
      video_id = response['items'][i]['snippet']['videoId']
      comment_id = response['items'][i]['snippet']['topLevelComment']['id']
      comment_text = response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay']
      author_name = response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
      comm_pub_date = response['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt']

      comment_df = pd.DataFrame({'video_id' : [video_id],
                              'comment_id' : [comment_id],
                              'comment_text' : [comment_text],
                              'Author_name' : [author_name],
                              'comment_published_date' : [comm_pub_date]})

      comment_data = pd.concat([comment_data, comment_df])

  except:
    video_id = vid_ID
    comment_id = "comment_disabled"
    comment_text = "comment_disabled"
    author_name = "comment_disabled"
    comm_pub_date = "comment_disabled"


  comment_df = pd.DataFrame({'video_id' : [video_id],
                              'comment_id' : [comment_id],
                              'comment_text' : [comment_text],
                              'Author_name' : [author_name],
                              'comment_published_date' : [comm_pub_date]})

  comment_data = pd.concat([comment_data, comment_df])

  return comment_data


# streamlit title declarion

st.title ("YOUTUBE DATA ANALYSER")
st.header("Analyse your youtube channels various detail with the help of youtube analyser by entering your channel ID")

# getting Channel ID as input
channel_ID = [st.text_input("Enter your channel ID:",placeholder="channel ID")]


# Taking DataFrames before execute

channel_data = pd.DataFrame()
for i in channel_ID:
  channel_data = pd.concat([channel_data,channel(i)])

all_vid_data = pd.DataFrame()
for i in channel_ID:
  all_vid_data = pd.concat([all_vid_data,video(i)])
  all_vid_data.vid_duration.replace({"PT" : ""},\
                                    regex=True, inplace=True)
  all_vid_data.vid_duration.replace({"H":":"},\
                                    regex=True, inplace=True)
  all_vid_data.vid_duration.replace({"M":":"},\
                                      regex=True, inplace=True)
  all_vid_data.vid_duration.replace({"S":""},\
                                    regex=True, inplace=True)

all_comm_data = pd.DataFrame()
for i in all_vid_data['video_ID']:
  all_comm_data = pd.concat([all_comm_data,comment(i)])


# Getting details based on the input
input = st.radio("select below option to get your channel detail",["channel detail","video detail","comment detail"])
if st.button("please enter to get details"):
  if input == "channel detail":
   st.write(channel_data)
  elif input == "video detail":
   st.write(all_vid_data)
  elif input == "comment detail":
   st.write(all_comm_data)


#SQL insert

import sqlalchemy as db
engine = db.create_engine('mysql://root:Ansar792@127.0.0.1:3306')
conn = engine.connect()

if st.button("Insert data to SQL"):
  channel_data.to_sql('channel', schema = 'youtube',if_exists='append',index=False, con=conn)
  all_vid_data.to_sql('video', schema = 'youtube',if_exists='append',index=False, con=conn)
  all_comm_data.to_sql('comment', schema = 'youtube',if_exists='append', index = False, con = conn)
  st.success("Data successfully inserted into SQL Database")

#SQL Q&A query

if st.button("Q&A"):
  st.text ('Q1 : What are the names of all the videos and their corresponding channels?')
  st.write(pd.read_sql_query('select channel_name,video_name from youtube.channel inner join youtube.video on channel.channel_ID=video.channel_ID', conn))

  st.text ('Q2 : Which channels have the most number of videos, and how many videos do they have?')
  st.write(pd.read_sql_query('select channel_name,count(video_name) from youtube.channel inner join youtube.video on channel.channel_ID=video.channel_ID group by(channel_name) order by(count(video_name))',conn))

  st.text ('Q3 : What are the top 10 most viewed videos and their respective channels?')
  st.write(pd.read_sql_query('select channel_name,video_name,vid_view_count from youtube.channel inner join youtube.video on channel.channel_ID = video.channel_ID order by vid_view_count desc limit 10', conn))

  st.text('Q4 : How many comments were made on each video, and what are their corresponding video names?')
  st.write(pd.read_sql_query('select video_name, vid_comment_count from youtube.video order by vid_comment_count asc',conn))

  st.text('Q5 : Which videos have the highest number of likes, and what are their corresponding channel names?')
  st.write(pd.read_sql_query('select video_name,vid_like_count,channel_name from youtube.video join youtube.channel on channel.channel_ID = video.channel_ID order by vid_like_count desc limit 1',conn))        
                
  st.text('Q6 : What is the total number of likes and dislikes for each video, and what are their corresponding video names?')
  st.write(pd.read_sql_query('select video_name,vid_like_count,vid_dislike_count from youtube.video',conn))

  st.text('Q7 : What is the total number of views for each channel, and what are their corresponding channel names?')
  st.write(pd.read_sql_query('select channel_name, channel_views from youtube.channel',conn))

  st.text('Q8 : What are the names of all the channels that have published videos in the year 2024?')
  st.write(pd.read_sql_query('select channel_name, video_name, left(video_published_date,4) from youtube.channel join youtube.video on channel.channel_ID = video.channel_ID where left(video_published_date,4) = "2022"',conn))

  st.text('Q9 : What is the average duration of all videos in each channel, and what are their corresponding channel names?')
  st.write(pd.read_sql_query('select channel_name, avg(vid_duration) from youtube.channel join youtube.video on channel.channel_ID=video.channel_ID group by channel_name',conn))

  st.text('Q10 : Which videos have the highest number of comments, and what are their corresponding channel names?')
  st.write(pd.read_sql_query('select channel_name, video_name, vid_comment_count from youtube.channel join youtube.video on channel.channel_ID = video.channel_ID order by vid_comment_count desc limit 1',conn))

#END of coding