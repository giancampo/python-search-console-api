#!/usr/bin/python

import httplib2

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow


# Copy your credentials from the console
CLIENT_ID = 'ENTER-YOURS-HERE'
CLIENT_SECRET = 'ENTER-YOURS-HERE'

# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)

#Useful links:
# https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.urlcrawlerrorssamples.html#list
# http://google.github.io/google-api-python-client/docs/epy/googleapiclient.http.HttpRequest-class.html


retrieve_search_queries = webmasters_service.searchanalytics().query(
    siteUrl='ENTER-YOURS-HERE',
    body={
        "startDate": "2019-03-25",
        "endDate": "2019-03-31",
        "dimensions": ["query"],
        "dimensionFilterGroups": [
            {
                "filters": [
                    {
                        "dimension": "country",
                        "operator": "equals",
                        "expression": "ITA"
                        }
                    ]
                }
            ],
        "aggregationType": "auto",
        "rowLimit": 25000
        }
    ).execute()

for i in range(0, 25000):
    results_file = open("results.txt", "a+")
    #keys1 = retrieve_search_queries['rows'][i]['keys'][0].encode()
    #keys2 = retrieve_search_queries['rows'][i]['keys'][1].encode()
    keys = retrieve_search_queries['rows'][i]['keys']
    impressions = retrieve_search_queries['rows'][i]['impressions']
    clicks = retrieve_search_queries['rows'][i]['clicks']
    ctr = retrieve_search_queries['rows'][i]['ctr']
    position = retrieve_search_queries['rows'][i]['position']
    print ("%s|%s|%s|%s|%s\n" % (keys, impressions, clicks, ctr, position))
    results_file.write ("%s|%s|%s|%s|%s\n" % (keys, impressions, clicks, ctr, position))
    #print ("%s|%s|%s|%s|%s|%s\n" % (keys1, keys2, impressions, clicks, ctr, position))
    #results_file.write ("%s|%s|%s|%s|%s|%s\n" % (keys1, keys2, impressions, clicks, ctr, position))
    results_file.close()
