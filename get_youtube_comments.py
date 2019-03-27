# -*- coding: utf-8 -*-
import json
import re
import csv
from apiclient.discovery import build
from apiclient.errors import HttpError
import urllib.request as ur
import xml.etree.ElementTree as ET
import pandas

#from oauth2client.tools import argparser

commentCount = -1
comments = []
videoComments = []
urls = []
capids = []
languages = []
publishTimeStamps = []
channelIds = []
channelTitles = []
categories = []
titles = []
descriptions = []
channelPublishedatTimeStamps = []
channelDescriptions = []
channelSubscriberCounts = []
channelViewCounts = []
channelCommentCounts = []
channelVideoCounts = []

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
# https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyC1WzN-xlE8nWim1opEk-NBd8gqSy9WSWs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_get_videoinfo(videoID):
  video={}
  youtube =build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  #Collect top 50 comments from a  video given the videoID
  search_response={}
  try:
    search_response = youtube.commentThreads().list(
      part="id,snippet",
      videoId=videoID,
      textFormat = "plainText",
      maxResults = 50
    ).execute()
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  comments_list = []
  for item in search_response.get("items", []):
    #print item["snippet"]["topLevelComment"]["snippet"]
    comments_list.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"].encode('ascii', 'ignore').decode('ascii'))
  #add comments to video['comment']
  video['comment']=comments_list
  #Collect information about video captions
  captions=youtube.captions().list(videoId=videoID,part="snippet").execute()
  for capts in captions.get("items",[]):
    if capts["snippet"]["language"]=='en':
      video['captid']=capts["id"]
      video['trackKind']=capts["snippet"]["trackKind"]
      video['isCC']=capts["snippet"]["isCC"]
      video['language']=capts["snippet"]["language"]
      video['isAutoSynced']=capts["snippet"]["isAutoSynced"]
      video['audioTrackType']=capts["snippet"]["audioTrackType"]
      video['captsLastUpdated']=capts["snippet"]["lastUpdated"]
  url="http://video.google.com/timedtext?lang=en&v="+videoID
  subtitle=[]
  subtitle_retrieve=ur.urlopen(url).read()
  if len(subtitle_retrieve)!=0:
    tree=ET.fromstring(subtitle_retrieve)
    subtitle_extract=ET.tostring(tree, encoding='utf-8', method='text')
    subtitle.extend([subtitle_extract.decode('utf-8', 'ignore').encode('utf-8')])
  video['subtitle']=subtitle

  search_response=youtube.videos().list(
    part="id, snippet,contentDetails,liveStreamingDetails,player,statistics,status, topicDetails",
    id=videoID
    ).execute()
  if search_response['pageInfo']['totalResults']!=1:
    print ("no result/not unique ID. ")
    return video
  else:
    for item in search_response.get("items", []):
      video['id']=item['id']
      #attributes in snippet (publishedAt, channelId, channelTitle, categoryId, videoTitle, description)
      video['publishedAt']=item['snippet']['publishedAt']
      video['channelId']=item['snippet']['channelId']
      video['channelTitle']=item['snippet']['channelTitle']
      video['categoryId']=item['snippet']['categoryId']
      video['title']=item['snippet']['title']
      video['description']=item['snippet']['description']
      channel_details=youtube.channels().list(id=video['channelId'],part="snippet,statistics").execute()
      for channel in channel_details.get("items",[]):
        try:
          video['channelPublishedat']=channel['snippet'].get('publishedAt', '')
          video['channelDescription']=channel['snippet'].get('description', '')
          video['channelSubscriberCount']=channel['statistics'].get('subscriberCount',0)
          video['channelViewCount']=channel['statistics'].get('viewCount',0)
          video['channelCommentCount']=channel['statistics'].get("commentCount",0)
          video['channelVideoCount']=channel['statistics'].get('videoCount',0)
        except HttpError as e:
          print ("An KeyError error %d occurred:\n%s" % (e.resp.status, e.content))
      #attributes in contentDetails(duration, dimension,definition,caption,licensed)
      video['contentDuration']=item['contentDetails']['duration']
      video['contentDimension']=item['contentDetails']['dimension']
      video['contentDefinition']=item['contentDetails']['definition']
      video['contentCaption']=item['contentDetails']['caption']
      video['contentLicensed']=item['contentDetails']['licensedContent']
      video['contentRating']=item['contentDetails'].get('contentRating',{})
      #attributes in status(uploadStatus,privacyStatus, license, embeddable,publicStatsViewable)
      video['uploadStatus']=item['status']['uploadStatus']
      video['privacyStatus']=item['status']['privacyStatus']
      video['license']=item['status']['license']
      video['embeddable']=item['status']['embeddable']
      video['publicStatsViewable']=item['status']['publicStatsViewable']
      #attributes in statistics(viewCount, likeCount, dislikeCount,favoriteCount,commentCount)
      video['viewCount']=item['statistics'].get('viewCount',0)
      video['likeCount']=item['statistics'].get('likeCount',0)
      video['dislikeCount']=item['statistics'].get('dislikeCount',0)
      video['favoriteCount']=item['statistics'].get('favoriteCount',0)
      video['commentCount']=item['statistics'].get('commentCount',0)
      #attributes from topicDetails (topicIds, relevantTopicIds)
      video['topicIds']=item.get('topicDetails',{}).get('topicIds','')
      video['relevantTopicIds']=item.get('topicDetails',{}).get('relevantTopicIds','')
  return video

def youtube_search(query,max_result=50):
  videoIdlist=[]
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    channelId=query,
    part="id,snippet",
    maxResults=max_result
  ).execute()

#  videos = []
#  channels = []
#  playlists = []
  
  #https://www.googleapis.com/youtube/v3/search?key={AIzaSyC1WzN-xlE8nWim1opEk-NBd8gqSy9WSWs}&channelId={UCLfPQRsJtGvdQN2IfXyy0ow}&part=snippet,id&order=date&maxResults=50


  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
#  print(search_response)
  for search_result in search_response.get("items", []):
#      print(search_result)
      if(search_result["id"]["kind"] == "youtube#video"):
         videoIdlist.append(search_result["id"]["videoId"])
#    if search_result["id"]["kind"] == "youtube#video":
#      
#      videos.append("%s (%s)" % (search_result["snippet"]["title"],
#                                 search_result["id"]["videoId"]))
#      videoIdlist.append(search_result["id"]["videoId"])
#    elif search_result["id"]["kind"] == "youtube#channel":
#      channels.append("%s (%s)" % (search_result["snippet"]["title"],
#                                   search_result["id"]["channelId"]))
#    elif search_result["id"]["kind"] == "youtube#playlist":
#      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#                                    search_result["id"]["playlistId"]))

#  print ("Videos:\n", "\n".join(videos), "\n")
#  print ("Channels:\n", "\n".join(channels), "\n")
#  print ("Playlists:\n", "\n".join(playlists), "\n")
  return videoIdlist

def get_videos(channelId, max_result):
  try:
    videoIdlist=youtube_search(channelId,max_result)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(channelId+":")
    print(videoIdlist)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#    f=open('comments.txt','a')
    for idx,value in enumerate(videoIdlist):
      video=youtube_get_videoinfo(value)
      video['keyword']=keyword
      video['rank']=idx
      parse(video)
#      f.write(json.dumps(video))
#      f.write('\n')
#    f.close() 
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    
def parse(video):
# parsing: one comment per line; ignored videos with empty comment
#    print(video)
    if (video['comment'] != ""):      
        line = video
        videoComments = line['comment']
#        print(videoComments)
        for item in videoComments:
            if len(item) > 0:
                comments.append(item)
                if "id" in line:
                    urls.append("https://www.youtube.com/watch?v=" + video['id'])
                else:
                    urls.append("")
                if "captid" in line:
                    capids.append(line['captid'])
                else:
                    capids.append("")
                if "language" in line:
                    languages.append(line['language'])
                else:
                    languages.append("")
                if "publishedAt" in line:
                    publishTimeStamps.append(line['publishedAt']) 
                else:
                    publishTimeStamps.append("")
                if "channelId" in line:
                    channelIds.append(line['channelId'])
                else:
                    channelIds.append("")
                if "channelTitle" in line:
                    channelTitles.append(line['channelTitle'])
                else:
                    channelTitles.append("")
                if "categoryId" in line:
                    categories.append(line['categoryId'])
                else:
                    categories.append("")
                if "title" in line:
                    titles.append(line['title'])  
                else:
                    titles.append("")
                if "description" in line:
                    descriptions.append(line['description']) 
                else:
                    descriptions.append("")
                if "channelPublishedat" in line:
                    channelPublishedatTimeStamps.append(line['channelPublishedat']) 
                else:
                    channelPublishedatTimeStamps.append("")
                if "channelDescription" in line:
                    channelDescriptions.append(line['channelDescription'])  
                else:
                    channelDescriptions.append("")
                if "channelSubscriberCount" in line:
                    channelSubscriberCounts.append(line['channelSubscriberCount'])
                else:
                    channelSubscriberCounts.append("")                                 
                if "channelViewCount" in line:
                    channelViewCounts.append(line['channelViewCount']) 
                else:
                    channelViewCounts.append("")
                if "channelCommentCount" in line:
                    channelCommentCounts.append(line['channelCommentCount']) 
                else:
                    channelCommentCounts.append("")
                if "channelVideoCount" in line:
                    channelVideoCounts.append(line['channelVideoCount']) 
                else:
                    channelVideoCounts.append("")
                global commentCount
                commentCount += 1
                i = commentCount
                print ('comment#:'+ str(i)+'*****************************')
                print(comments[i]
                +"..."+urls[i]+"..."+capids[i]+"..."+languages[i]+"..."+
                      publishTimeStamps[i]+"..."+channelIds[i]+"..."+channelTitles[i]+"..."+
                      categories[i]+"..."+titles[i]+"..."+descriptions[i]+"..."+
                      channelPublishedatTimeStamps[i]+"..."+channelDescriptions[i]+"..."+
                      channelSubscriberCounts[i]+"..."+channelViewCounts[i]+"..."+
                      channelCommentCounts[i]+"..."+channelVideoCounts[i]
                      )
                with open('comments.csv', mode='a', encoding = 'utf-8') as commentFile:
                    commentWriter = csv.writer(commentFile)
                    row = [comments[i], urls[i], capids[i],languages[i], 
                                         publishTimeStamps[i], channelIds[i], channelTitles[i], 
                                         categories[i], titles[i], descriptions[i],
                                         channelPublishedatTimeStamps[i], channelDescriptions[i], 
                                         channelSubscriberCounts[i], channelViewCounts[i], 
                                         channelCommentCounts[i], channelVideoCounts[i]]
                    commentWriter.writerow(row)
                commentFile.close()
  
keywords=pandas.read_excel('channels.xlsx')
L1=keywords['Channels'].values.tolist()
try:
    for keyword in L1:
        get_videos(keyword,50)
except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
