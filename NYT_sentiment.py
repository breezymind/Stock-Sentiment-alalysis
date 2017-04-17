import re
from textblob import TextBlob

from nytimesarticle import articleAPI
APIKey = "67ffae10edaf42e5ad0564962e888f79"
api = articleAPI(APIKey)

def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    try:
        for i in articles['response']['docs']:
            dic = {}
            dic['headline'] = i['headline']['main'].encode("utf8")
            dic['date'] = i['pub_date'][0:10] # cutting time of day.
            if i['snippet'] is not None:
                dic['snippet'] = i['snippet'].encode("utf8")
            dic['source'] = i['source']
            dic['type'] = i['type_of_material']
            dic['word_count'] = i['word_count']
            
            #dic['id'] = i['_id']
            #if i['abstract'] is not None:
            #    dic['abstract'] = i['abstract'].encode("utf8")
            #dic['desk'] = i['news_desk']
            #dic['section'] = i['section_name']
            #dic['url'] = i['web_url']
            
            #locations
            #locations = []
            #for x in range(0,len(i['keywords'])):
            #    if 'glocations' in i['keywords'][x]['name']:
            #        locations.append(i['keywords'][x]['value'])
            #dic['locations'] = locations
            # subject
            #subjects = []
            #for x in range(0,len(i['keywords'])):
            #    if 'subject' in i['keywords'][x]['name']:
            #        subjects.append(i['keywords'][x]['value'])
            #dic['subjects'] = subjects   
            
            news.append(dic)
        return(news)
    except KeyError:
        return []
    
def get_articles(date_range, query):
    '''
    This function accepts a date range in string format (e.g.'2016-03-01 to 2017-03-01')
    and a query (e.g.'Amnesty International') and it will 
    return a list of parsed articles (in dictionaries).
    '''
    matchObj = re.match( r'(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', date_range)
    start_date = matchObj.group(1)
    end_date = matchObj.group(2)
    all_articles = []
    for i in range(0,100): #NYT limits pager to first 100 pages. But rarely will you find over 100 pages of results anyway.
        articles = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = start_date.replace('-', ''),
               end_date = end_date.replace('-', ''),
               sort='oldest',
               page = str(i))
        articles = parse_articles(articles)
        all_articles = all_articles + articles
    return(all_articles)

keywords = raw_input('Please input the keywords: ')
date_range = raw_input('Please input the time range: ')
news = get_articles(date_range, keywords)

headline_sentiment_pos = []
headline_sentiment_neutral = []
headline_sentiment_neg = []
snippet_sentiment_pos = []
snippet_sentiment_neutral = []
snippet_sentiment_neg = []

for i in news:
    try:
        headline_sentiment_list = []
        headline_sentiment = TextBlob(i['headline']).sentiment
        headline_sentiment_list.append(headline_sentiment)

        if headline_sentiment.polarity == 0:
            headline_sentiment_neutral.append((i['headline'], 'neutral'))
        elif headline_sentiment.polarity > 0:
            headline_sentiment_pos.append((i['headline'],'positive'))
        else:
            headline_sentiment_neg.append((i['headline'],'negative'))


        snippet_sentiment_list = []
        snippet_sentiment = TextBlob(i['snippet']).sentiment
        snippet_sentiment_list.append(snippet_sentiment)
        if snippet_sentiment.polarity == 0:
            snippet_sentiment_neutral.append((i['headline'], 'neutral'))
        elif snippet_sentiment.polarity > 0:
            snippet_sentiment_pos.append((i['headline'],'positive'))
        else:
            snippet_sentiment_neg.append((i['headline'],'negative'))
            
    except UnicodeDecodeError:
        pass
        
print len(news)
for i in headline_sentiment:
    print headline_sentiment_pos
    print '\n'
    print headline_sentiment_neutral
    print '\n'
    print headline_sentiment_neg
    print '\n'
    
