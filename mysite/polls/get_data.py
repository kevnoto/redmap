from __future__ import division
import requests
from math import log
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np
from colorsys import hsv_to_rgb, rgb_to_hsv
from datetime import datetime,timedelta
import pytz
import time

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def get_data():
    url = r"https://www.reddit.com/r/all/hot/.json"
    r = requests.get(url,headers = {'User-agent': 'bot361308'}).json()
    return r['data']['children']

def get_subreddit_data(r):
    reddits = r.GET.getlist('reddits[]')
    reddit_data = []
    for subreddit in reddits:
        url = r"https://www.reddit.com/r/%s/hot/.json" % subreddit
        r = requests.get(url,headers = {'User-agent': 'bot361308'}).json()
        reddit_data += r['data']['children']
    return {'data':reddit_data}

def hot_link(link):
    order = log(max(abs(link['score']),1),10)
    sign = 1 if link['score'] > 0 else -1 if link['score'] < 0 else 0
    seconds = link['created'] - 1134028003
    return round(sign * order + seconds / 45000, 7)

divs = []

def hex_to_rgb(hx):
    hx = hx.split("#")[1]
    rgb = tuple(int(hx[i:i+2], 16)for i in (0,2,4))
    return rgb

class block(object):
    global divs
    def __init__(self,width,height,links,ratio=1):
        self.width = width
        self.height = height
        self.links = links
        self.split_type = 'vertical' if self.width > self.height*1.2 else 'horizontal'
        self.ratio = ratio
        self.spawn_children()
        self.set_font_size()
        self.set_color()

    def set_font_size(self):
        if len(self.links) == 1:
            self.font_size = "%spx" % int(np.sqrt((self.width * self.height) / (len(self.links[0].title)*1.8)))
        else:
            self.font_size = "1em"

    def __str__(self):
        return "block w/ %s links" % len(self.links)

    def spawn_children(self):
        if len(self.links) == 1:
            self.children = []
            self.title = self.links[0].title
        else:
            if len(self.links) == 2:
                splits = [[self.links[0]],[self.links[1]]]
            else:
                dif1 = self.links[0].score-self.links[1].score
                dif2 = self.links[1].score-self.links[2].score
                if dif1/dif2 > 1:
                    # DO ONLY 1
                    splits = [[self.links[0]],self.links[1:]]
                else:
                    # DO 2
                    splits = [self.links[0:2],self.links[2:]]
            s1 = np.max([i.score for i in splits[0]]) - splits[0][0].pos*.05
            s2 = np.max([i.score for i in splits[1]]) - splits[1][0].pos*.05
            sum_splits = s1+s2
            # print "%s, %s" % (s1/sum_splits,s2/sum_splits)
            if self.width < 100 or self.height < 100:
                self.children = []
                self.links = [self.links[0]]
                self.title = self.links[0].title

            elif self.split_type == 'vertical':
                self.children = [
                    block(self.width*s1/sum_splits,self.height,splits[0],ratio=s1/s2),
                    block(self.width*s2/sum_splits,self.height,splits[1]),
                ]
            else:
                self.children = [
                    block(self.width,self.height*s1/sum_splits,splits[0],ratio=s1/s2),
                    block(self.width,self.height*s2/sum_splits,splits[1]),
                ]

    def set_color(self):
        old_rgb = hex_to_rgb(self.links[0].color)
        hsv = list(rgb_to_hsv(old_rgb[0]/255,old_rgb[1]/255,old_rgb[2]/255))
        now = time.time()
        created = int(self.links[0].time)
        adjustment = (now - created) / timedelta(hours=12).total_seconds()
        hsv[2] = hsv[2] * (0 if adjustment > 1 else (1-adjustment))
        new_rgb = list(hsv_to_rgb(hsv[0],hsv[1],hsv[2]))
        new_rgb = [i*255 for i in new_rgb]
        self.color = '#%02x%02x%02x' % (new_rgb[0],new_rgb[1],new_rgb[2])

    def to_dict(self):
        d = {
            'width':self.width,
            'height':self.height,
            'split_type':self.split_type,
            'ratio':"%.2f" % self.ratio,
            'font_size':self.font_size,
        }
        if self.children:
            d['children'] = [i.to_dict() for i in self.children]
            d['title'] = ""
        else:
            d['children'] = []
            d['title'] = self.title
            d['url'] = self.links[0].url
            d['color'] = self.color
        return d

    __repr__ = __str__

class reddit_link(object):
    def __init__(self,reddit_d,pos):
        self.score = reddit_d['score']
        self.title = html_decode(reddit_d['title'])
        self.time = reddit_d['created_utc']
        self.url = reddit_d['url']
        self.pos = pos
        self.score = hot_link(reddit_d)
        self.font_size = "2px"
        self.color = '#4281ff'

def serve_data(r):
    width = int(r.GET.get('width',400))
    height = int(r.GET.get('height',400))
    data = get_data()
    data = [reddit_link(i['data'],idx) for idx,i in enumerate(data)]
    b = block(width,height,data)
    return b.to_dict()

