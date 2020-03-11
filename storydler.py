'''
Module to download stories and highlights
'''

import json
import os
import sys
import pickle
import random
import time
import requests
from bs4 import BeautifulSoup

from login import get_id
from queryhashes import query_hash



class StoryDler():
    '''
    StoryDler: Used to download stories and highlights.
    Methods: download_stories,download_highlights,getHighlightReelId
    '''

    def __init__(self, username, session,  _filter_title=None):
        '''
        username: username of profile whose story have to save
        session: Session with login cookies
        filter_title: used to download a particular highlight reel(only for highlights)
        '''
        self.username = username
        self.session = session
        self._filter_title = _filter_title
        self.total = 0
        self.currPos = 0
        if sys.platform == 'windows':
            self.dirspace = '\\'
        else:
            self.dirspace = '/'


    def download_stories(self):
        '''
        Download story of a profile
        '''
        userid = get_id(self.username)
        if not os.path.exists(self.username+self.dirspace+'Stories'):
            os.makedirs(self.username+self.dirspace+'Stories'+self.dirspace)
        queryhash = query_hash().story
        ur = "https://www.instagram.com/graphql/query/"
        variables = {
            "reel_ids": [str(userid)],
            "tag_names": [],
            "location_ids": [],
            "highlight_reel_ids": [],
            "precomposed_overlay": False,
            "show_story_viewer_list": True,
            "story_viewer_fetch_count": 50,
            "story_viewer_cursor": "",
            "stories_video_dash_manifest": False
        }
        spacer = '*******************************************'
        variables_json = json.dumps(variables, separators=(',', ':'))
        params = {
            'query_hash': queryhash,
            'variables': variables_json
        }
        stories = self.session.get(ur, params=params)
        data = json.loads(stories.content)['data']['reels_media']
        if len(data) != 0:
            for it in data:
                self.total = len(it['items'])
                for key in it['items']:
                    self.currPos += 1
                    epoch = key['taken_at_timestamp']
                    if key['is_video']:
                        print('\n{space}\nStory Details: \nStory Type: Video\nVideo Duration: {}\nUploaded on: {} at {}\n{space}\n'.format(
                            key['video_duration'], time.strftime("%a, %d %b %Y", time.localtime(epoch)), time.strftime("%H:%M:%S", time.localtime(epoch)), space=spacer))
                        
                        url2 = key['video_resources'][-1]['src']
                        vid_path = '{}{dirspace}Stories{dirspace}{}{}.mp4'.format(self.username, 'story', time.strftime(
                            "_%d_%b_%Y_%H-%M-%S", time.localtime(epoch)),dirspace=self.dirspace)
                        if not os.path.exists(vid_path):
                            with open(vid_path, 'wb') as op:
                                op.write(requests.get(
                                    url2, stream=True).content)
                                print(
                                    '\nDownloaded!\n')
                                
                        else:
                            print(
                                '\nMedia already exists! SKIPPING....\n')
                            
                    else:
                        print('\n{space}\nStory Details: \nStory Type: Image\nUploaded on: {} at {}\n{space}\n'.format(time.strftime(
                            "%a, %d %b %Y", time.localtime(epoch)), time.strftime("%H:%M:%S", time.localtime(epoch)), space=spacer))
                        
                        url2 = key['display_resources'][-1]['src']
                        img_path = '{}{dirspace}Stories{dirspace}{}{}.jpg'.format(self.username, 'story', time.strftime(
                            "_%d_%b_%Y_%H-%M-%S", time.localtime(epoch)), dirspace=self.dirspace)
                        if not os.path.exists(img_path):
                            with open(img_path, 'wb') as op:
                                op.write(requests.get(
                                    url2, stream=True).content)
                                print(
                                    '\nDownloaded!\n')
                                
                        else:
                            print(
                                '\nMedia already exists! SKIPPING....\n')
                            
        else:
            print(
                '\nUSER HAS NO STORIES! ABORTING...\n')

    def download_highlights(self, reelId, dict_of_titles):
        '''
        Download highlights
        reelId: A list of highlight IDs
        dict_of_titles: a dictionary which contains reel IDs and their respective titles
        '''
        queryhash = query_hash().story
        ur = "https://www.instagram.com/graphql/query/"
        variables = {
            "reel_ids": [],
            "tag_names": [],
            "location_ids": [],
            "highlight_reel_ids": reelId,
            "precomposed_overlay": False,
            "show_story_viewer_list": True,
            "story_viewer_fetch_count": 50,
            "story_viewer_cursor": "",
            "stories_video_dash_manifest": False
        }
        spacer = '*******************************************'
        variables_json = json.dumps(variables, separators=(',', ':'))
        params = {
            'query_hash': queryhash,
            'variables': variables_json
        }
        self.total = len(reelId)
        stories = self.session.get(ur, params=params)
        data = json.loads(stories.content)['data']['reels_media']
        for it in data:
            self.currPos += 1
            title = dict_of_titles[it['id']]
            highlightPath = self.username + f'{self.dirspace}Highlights{self.dirspace}{title}'
            print("\n{space}\n\nHighlight Name: {title}\n".format(
                space='-'*60, title=title))
            
            if not os.path.exists(highlightPath):
                os.makedirs(highlightPath)
            else:
                pass
            for key in it['items']:
                epoch = key['taken_at_timestamp']
                if key['is_video']:
                    print('\n{space}\nStory Details:\nStory Type: Video\nVideo Duration: {}\nUploaded on: {} at {}\n{space}\n'.format(
                        key['video_duration'], time.strftime("%a, %d %b %Y", time.localtime(epoch)), time.strftime("%H:%M:%S", time.localtime(epoch)), space=spacer))
                    url2 = key['video_resources'][-1]['src']
                    vid_path = '{}{dirs}Highlights{dirs}{title}{dirs}{}{}.mp4'.format(self.username, 'story', time.strftime(
                        "_%d_%b_%Y_%H-%M-%S", time.localtime(epoch)), title=title,dirs=self.dirspace)
                    if not os.path.exists(vid_path):
                        with open(vid_path, 'wb') as op:
                            op.write(requests.get(url2, stream=True).content)
                            print(
                                '\nDownloaded!\n')
                            
                    else:
                        print(
                            '\nMedia already exists! SKIPPING....\n')
                        
                else:
                    print('\n{space}\nStory Details:\nStory Type: Image\nUploaded on: {} at {}\n{space}\n'.format(time.strftime(
                        "%a, %d %b %Y", time.localtime(epoch)), time.strftime("%H:%M:%S", time.localtime(epoch)), space=spacer))
                    
                    url2 = key['display_resources'][-1]['src']
                    img_path = '{}{dirs}Highlights{dirs}{title}{dirs}{}{}.jpg'.format(self.username, 'story', time.strftime(
                        "_%d_%b_%Y_%H-%M-%S", time.localtime(epoch)), title=title,dirs=self.dirspace)
                    if not os.path.exists(img_path):
                        with open(img_path, 'wb') as op:
                            op.write(requests.get(url2, stream=True).content)
                            print(
                                '\nDownloaded!\n')
                            
                    else:
                        print(
                            '\nMedia already exists! SKIPPING....\n')
                        

    def getHighlightId(self):
        '''
        Returns a list of reelId of a profile and dictionary of their titles
        '''
        if self._filter_title is not None:
            self._filter_title = [self._filter_title]
        else:
            self._filter_title = ['']
        userid = get_id(self.username)
        variables = {
            "user_id": str(userid),
            "include_chaining": True,
            "include_reel": False,
            "include_suggested_users": False,
            "include_logged_out_extras": False,
            "include_highlight_reels": True,
            "include_related_profiles": False
        }
        variables_json = json.dumps(variables)
        queryhash = query_hash().highlights
        params = {
            'query_hash': queryhash,
            'variables': variables_json
        }
        link = 'https://www.instagram.com/graphql/query/'
        reels = self.session.get(link, params=params)
        data = json.loads(reels.text)[
            'data']['user']['edge_highlight_reels']['edges']
        highlightReelId = []
        dict_titles = {}
        for i in self._filter_title:
            for node in data:
                if i.lower() in node['node']['title'].lower():
                    highlightReelId.append(node['node']['id'])
                    dict_titles.update(
                        {node['node']['id']: node['node']['title']})

        self.download_highlights(highlightReelId, dict_titles)
