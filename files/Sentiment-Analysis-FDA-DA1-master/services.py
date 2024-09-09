import warnings
import requests
import constants
from textblob import TextBlob
import regex as re
import requests
from gingerit.gingerit import GingerIt

import rpy2.robjects as robjects
import pandas as pd
import matplotlib.pyplot as plt
from rpy2.robjects import pandas2ri
from rpy2.rinterface_lib.embedded import RRuntimeError
from rpy2.robjects.packages import importr


utils = importr('utils')
pandas2ri.activate()
warnings.filterwarnings("ignore")


def extract_youtube_video_title(url):
    data = requests.get(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={extract_youtube_video_id(url)}&key={constants.API_KEY}")
    data = data.json()
    return data['items'][0]['snippet']['title']


def extract_youtube_video_id(url):
    pattern = r"(?<=v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|\&v=|\?v=)([^#\&\?]*)(?=\?|\&|\#|$|\z)"
    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


def get_comments(vid_id, comments, nextPageToken):
    # https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyC92Np9S-r_ZB-qbz_4cMoA1FtGaniuiH0&textFormat=plainText&part=snippet&videoId=kffacxfA7G4&maxResults=100&pageToken=
    # https://www.youtube.com/watch?v=RVLNBVK8auM
    data = requests.get(
        f"https://www.googleapis.com/youtube/v3/commentThreads?key={constants.API_KEY}&textFormat=plainText&part=snippet&videoId={vid_id}&maxResults={comments}&pageToken={nextPageToken}")

    data = data.json()
    try:
        nextPageToken = data['nextPageToken']
    except:
        nextPageToken = ''
    comments = []
    for item in data['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment: str = comment.encode("ascii", "ignore").decode().strip()
        if comment != "":
            # corrected = spell_checker(comment)
            # print(corrected)
            # comments.append(corrected)
            comments.append(comment)

    return nextPageToken, comments


def get_sentiment(comment):
    # comment = spell_checker(comment)
    analysis = TextBlob(comment)

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# def importr_tryhard(packname):
#     try:
#         rpack = importr(packname)
#     except RRuntimeError:
#         utils.install_packages(packname)
#         rpack = importr(packname)
#     return rpack

# def get_sentiment(comments):

#     text_df1 = pd.DataFrame(comments, columns=['comment'])
#     text_df1['comment'] = text_df1['comment'].astype(str).str.replace('[^\w\s]', '').str.replace('\d+', '').str.replace('\n', '').str.replace('\t', '').str.replace('\r', '').str.replace(' +', ' ').str.lower()

#     review = text_df1['comment'].tolist()
#     review = robjects.vectors.StrVector(review)
#     review = [i for i in review]
#     review = robjects.vectors.StrVector(review)
#     print(review)

#     syuzhet = importr_tryhard("syuzhet")
#     s1 = syuzhet.get_nrc_sentiment(review)
#     s1 = pd.DataFrame(s1).T

#     review_sentiment = pd.concat(
#         [text_df1['comment'], pd.DataFrame(s1)], axis=1)
#     sentiments = "anger anticipation disgust fear joy sadness surprise trust negative positive".split()[::-1]
#     review_sentiment.columns = ['comment'] + sentiments
#     review_sentiment['sentiment'] = review_sentiment[sentiments].idxmax(axis=1)
#     print(review_sentiment)
#     return review_sentiment


def spell_checker(text: str) -> str:
    corrected_text = GingerIt().parse(text)
    return corrected_text['result']

def main(link, comments):
    vid_id = extract_youtube_video_id(link)
    nextPageToken, comments_list = get_comments(vid_id, comments, '')
    while (len(comments_list) < comments):
        if nextPageToken != '':
            nextPageToken, comments_list_temp = get_comments(
                vid_id, comments, nextPageToken)
            comments_list += comments_list_temp
        else:
            break
    parsed_comment = {'comment': [], 'sentiment': []}
    for comment in comments_list:
        parsed_comment['comment'].append(comment)
        parsed_comment['sentiment'].append(get_sentiment(comment))
    # parsed_comment = get_sentiment(comments_list)
    pList = []
    nList = []
    neList = []
    for i in range(len(parsed_comment['sentiment'])):
        if parsed_comment['sentiment'][i] == 'positive':
            pList.append(parsed_comment['comment'][i])
        elif parsed_comment['sentiment'][i] == 'negative':
            nList.append(parsed_comment['comment'][i])
        else:
            neList.append(parsed_comment['comment'][i])
    parsed_comment['positive'] = pList
    parsed_comment['negative'] = nList
    parsed_comment['neutral'] = neList
    parsed_comment['title'] = extract_youtube_video_title(link)
    parsed_comment[
        'thumbnail'] = f"http://img.youtube.com/vi/{extract_youtube_video_id(link)}/maxresdefault.jpg"
    return parsed_comment
