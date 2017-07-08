from __future__ import division
import requests
from math import log
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np

def get_data():
    url = r"https://www.reddit.com/r/aww/hot/.json"
    r = requests.get(url,headers = {'User-agent': 'bot361308'}).json()
    return r['data']['children']

def hot_link(link):
    order = log(max(abs(link['score']),1),10)
    sign = 1 if link['score'] > 0 else -1 if link['score'] < 0 else 0
    seconds = link['created'] - 1134028003
    return round(sign * order + seconds / 45000, 7)

divs = []

class block(object):
    global divs
    def __init__(self,width,height,links,ratio=1):
        self.width = width
        self.height = height
        self.links = links
        self.split_type = 'vertical' if self.width > self.height*1.2 else 'horizontal'
        self.ratio = ratio
        self.spawn_children()

    def __str__(self):
        return "block w/ %s links" % len(self.links)

    def spawn_children(self):
        if len(self.links) == 1:
            self.children = []
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
            s1 = np.max([i.score for i in splits[0]])
            s2 = np.max([i.score for i in splits[1]])
            sum_splits = s1+s2
            # print "%s, %s" % (s1/sum_splits,s2/sum_splits)
            if self.width < 100 or self.height < 100:
                self.children = []
                self.links = [self.links[0]]
            elif self.split_type == 'vertical':
                self.children = [
                    block(self.width*s1/sum_splits,self.height,splits[0],ratio=s1/s2),
                    block(self.width*s2/sum_splits,self.height,splits[1],ratio=s2/s1),
                ]
            else:
                self.children = [
                    block(self.width,self.height*s1/sum_splits,splits[0],ratio=s1/s2),
                    block(self.width,self.height*s2/sum_splits,splits[1],ratio=s2/s1),
                ]

    def plot_all(self,x,y):
        x_pad = 0
        y_pad = 0
        if len(self.children) == 0:
            divs.append(patches.Rectangle((x,y),self.width,-self.height,facecolor='b',edgecolor='k',linewidth=1,linestyle='solid'))
        else:
            if self.split_type=='vertical':
                self.children[0].plot_all(x,y)
                self.children[1].plot_all(x + self.children[0].width + x_pad,y)
            else:
                self.children[0].plot_all(x,y)
                self.children[1].plot_all(x,y - self.children[0].height - y_pad)

    def to_dict(self):
        d = {
            'width':self.width,
            'height':self.height,
            'split_type':self.split_type,
            'ratio':"%.2f" % self.ratio,
        }
        if self.children:
            d['children'] = [i.to_dict() for i in self.children]
            d['title'] = ""
        else:
            d['children'] = []
            d['title'] = "%.2f"% self.links[0].score
        return d

    __repr__ = __str__

class link(object):
    def __init__(self,score):
        self.score = score

def serve_data(r):
    width = int(r.GET.get('width',400))
    height = int(r.GET.get('height',400))
    print "Width: %s" % width
    print "Height: %s"% height
    data = sorted(np.random.rand(50),reverse=True)
    data = [link(i) for i in data]
    b = block(width,height,data)
    # print b.to_dict()
    return b.to_dict()

if __name__ == '__main__':
    fig, axes = plt.subplots(2,2)
    for q in range(axes.shape[0]):
        for z in range(axes.shape[1]):
            divs = []
            ax = axes[q,z]
            plt.sca(ax)
            data = sorted(np.random.rand(50),reverse=True)
            data = [link(i) for i in data]
            b = block(1920,1080,data)
            print b.to_dict()
            b.plot_all(0,0)
            for idx,d in enumerate(divs):
                ax.add_patch(d)
                rx,ry = d.get_xy()
                cx = rx + d.get_width()/2
                cy = ry + d.get_height()/2
                ax.annotate("%.2f" % data[idx].score,(cx,cy),fontsize=6,color='w',ha='center',va='center')
            plt.axis('equal')
            plt.tight_layout()
    plt.show()
    raise








    data = get_data()
    for dat in data:
        print "%.2f/%.2f - %s" % (log(dat['data']['score'],10),hot_link(dat['data']),dat['data']['title'])
