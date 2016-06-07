# Write on 2016/06/07 by SunChuan

import feedparser
import re
import os


def getWordCounts(url):
    d = feedparser.parse(url)
    wc = {}

    # for key in d.entries():


apcount = {}
wordCounts = {}

with open('D:/machinelearninginaction/PCI_Code Folder/chapter3/feedlist2.txt') as file:
    fileLen = len(file.readlines())
    for feedurl in file:
        title, wc = getWordCounts(feedurl)
        wordCounts[title] = wc
        for key, value in wordCounts.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[key] = apcount[key] + 1

        wordList = []
        for key, value in apcount.items():
            frac = float(value) / len(fileLen)
            if frac < 0.5 or frac > 0.1: wordList.append(key)

def wordCounts(url):
    d = feedparser.parse(url)
    wc = {}
    print(d.entries)
    for key in d.entries:
        if 'summry' in key: summary = key.summary
        else: summary = key.description


def getWords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)

    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return ([word.lower() for word in words])

getWords('http://www.sina.com.cn/')



# wordCounts('http://www.sina.com.cn/')

# import feedparser
# import re
#
#
# # Returns title and dictionary of word counts for an RSS feed
# def getwordcounts(url):
#     # Parse the feed
#     d = feedparser.parse(url)
#     wc = {}
#     # Loop over all the entries
#     for e in d.entries:
#         if 'summary' in e:
#             summary = e.summary
#         else:
#             summary = e.description
#         # Extract a list of words
#         words = getwords(e.title + ' ' + summary)
#         for word in words:
#             wc.setdefault(word, 0)
#             wc[word] += 1
#     return d.feed.title, wc
#
#
# def getwords(html):
#     # Remove all the HTML tags
#     txt = re.compile(r'<[^>]+>').sub('', html)
#     # Split words by all non-alpha character
#     words = re.compile(r'[^A-Z^a-z]+').split(txt)
#     # Convert to lowercase
#     return [word.lower() for word in words if word != '']
#
#
# apcount = {}
# wordcounts = {}
# feedlist = [line for line in open('D:/machinelearninginaction/PCI_Code Folder/chapter3/feedlist2.txt')]
# for feedurl in feedlist:
#     try:
#         title, wc = getwordcounts(feedurl)
#         wordcounts[title] = wc
#         for word, count in wc.items():
#             apcount.setdefault(word, 0)
#             if count > 1:
#                 apcount[word] += 1
#     except:
#         print('Failed to parse feed %s' % feedurl)
#
# wordlist = []
# for w, bc in apcount.items():
#     frac = float(bc) / len(feedlist)
#     if frac > 0.1 and frac < 0.5:
#         wordlist.append(w)
#
# out = open('D:/machinelearninginaction/PCI_Code Folder/chapter3/blogdata2.txt', 'w')
# out.write('Blog')
# for word in wordlist: out.write('\t%s' % word)
# out.write('\n')
# for blog, wc in wordcounts.items():
#     print(blog)
#     out.write(blog)
#     for word in wordlist:
#         if word in wc:
#             out.write('\t%d' % wc[word])
#         else:
#             out.write('\t0')
#     out.write('\n')
