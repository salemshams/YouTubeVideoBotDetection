import re

file='comments.txt' 
commentCount = 0
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



with open(file) as input:
    for line in input:
        print(line)
        commentPattern = re.compile("comment\":.*?\[(.*?)\]", re.DOTALL)
        idPattern = re.compile("id\":.*?\"(.*?)\"", re.DOTALL)
        capIdPattern = re.compile("captid\":.*?\"(.*?)\"", re.DOTALL)
        languagePattern = re.compile("language\":.*?\"(.*?)\"", re.DOTALL)
        publishPattern =  re.compile("publishedAt\":.*?\"(.*?)\"", re.DOTALL)
        channelIdPattern =  re.compile("channelId\":.*?\"(.*?)\"", re.DOTALL)
        channelTitlePattern =  re.compile("channelTitle\":.*?\"(.*?)\"", re.DOTALL)
        categoryIdPattern = re.compile("categoryId\":.*?\"(.*?)\"", re.DOTALL)
        titlePattern = re.compile("title\":.*?\"(.*?)\"", re.DOTALL)
        descriptionPattern = re.compile("description\":.*?\"(.*?)\"", re.DOTALL)
        channelPublishPattern = re.compile("channelPublishedat\":.*?\"(.*?)\"", re.DOTALL)
        channelDescriptionPattern = re.compile("channelDescription\":.*?\"(.*?)\"", re.DOTALL)
        channelSubscriberCountPattern = re.compile("channelSubscriberCount\":.*?\"(.*?)\"", re.DOTALL)
        channelViewCountPattern = re.compile("channelViewCount\":.*?\"(.*?)\"", re.DOTALL)
        channelCommentCountPattern = re.compile("channelCommentCount\":.*?\"(.*?)\"", re.DOTALL)
        channelVideoCountPattern = re.compile("channelVideoCount\":.*?\"(.*?)\"", re.DOTALL)

    
        #if statement to check if theres more than 1 comment
        #if thereis more than one, iterate code to go through multiple comments
        
        if "comment" in line:
            output = commentPattern.search(line)
            idOutput = idPattern.search(line)
            capIdOutput = capIdPattern.search(line)
            languageOutput = languagePattern.search(line)
            publishTimeStampOutput = publishPattern.search(line)
            channelIdOutput = channelIdPattern.search(line)
            channelTitleOutput = channelTitlePattern.search(line)
            categoryOutput = categoryIdPattern.search(line)
            titleOutput = titlePattern.search(line)
            descriptionOutput  = descriptionPattern.search(line)
            channelPublishTimeStampOutput = channelPublishPattern.search(line)
            channelDescriptionOutput = channelDescriptionPattern.search(line)
            channelSubscriberCountOutput = channelSubscriberCountPattern.search(line)
            channelViewCountOutput = channelViewCountPattern.search(line)
            channelCommentCountOutput = channelCommentCountPattern.search(line)
            channelVideoCountOutput = channelVideoCountPattern.search(line)
            
            videoComments = [output.group(1)]
            
            for item in videoComments:
                if len(item) > 3:
#                    item.strip()
                    comments.append(item)
                    if "id" in line:
                        urls.append("https://www.youtube.com/watch?v=" + idOutput.group(1))
                    if "captid" in line:
                        capids.append(capIdOutput.group(1))
                    if "language" in line:
                        languages.append(languageOutput.group(1))
                    if "publishedAt" in line:
                        publishTimeStamps.append(publishTimeStampOutput.group(1)) 
                    if "channelId" in line:
                        channelIds.append(channelIdOutput.group(1))
                    if "channelTitle" in line:
                        channelTitles.append(channelTitleOutput.group(1))
                    if "categoryId" in line:
                        categories.append(categoryOutput.group(1))
                    if "title" in line:
                        titles.append(titleOutput.group(1))   
                    if "description" in line:
                        descriptions.append(descriptionOutput.group(1)) 
                    if "channelPublishedat" in line:
                        channelPublishedatTimeStamps.append(channelPublishTimeStampOutput.group(1)) 
                    if "channelDescription" in line:
                        channelDescriptions.append(channelDescriptionOutput.group(1))             
                    if "channelSubscriberCount" in line:
                        channelSubscriberCounts.append(channelSubscriberCountOutput.group(1))                                 
                    if "channelViewCount" in line:
                        channelViewCounts.append(channelViewCountOutput.group(1)) 
                    if "channelCommentCount" in line:
                        channelCommentCounts.append(channelCommentCountOutput.group(1))             
                    if "channelVideoCount" in line:
                        channelVideoCounts.append(channelVideoCountOutput.group(1))                        

#                    
print(comments[0]+"..."+urls[0]+"..."+capids[0]+"..."+languages[0]+"..."+
      publishTimeStamps[0]+"..."+channelIds[0]+"..."+channelTitles[0]+"..."+
      categories[0]+"..."+titles[0]+"..."+descriptions[0]+"..."+
      channelPublishedatTimeStamps[0]+"..."+channelDescriptions[0]+"..."+
      channelSubscriberCounts[0]+"..."+channelViewCounts[0]+"..."+
      channelCommentCounts[0]+"..."+channelVideoCounts[0])
            
