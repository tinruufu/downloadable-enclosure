from bs4 import BeautifulSoup
from lxml.etree import fromstring, tostring, Element
import requests


NS = '{{http://purl.org/rss/1.0/modules/content/}}{}'


def make_feed():
    tree = fromstring(
        requests.get('http://dlc.invincible.ink/feed/').content
    )
    for item in tree.find('channel').findall('item'):
        if item.find('enclosure') is None:
            continue

        soup = BeautifulSoup(item.find(NS.format('encoded')).text, 'lxml')
        sources = soup.select('audio source[type="audio/mpeg"]')

        for source in sources:
            mp3 = source['src']
            item.append(Element('enclosure', {
                'url': mp3,
                'type': 'audio/mpeg',
                'length': requests.head(mp3).headers['content-length'],
            }))

    return tostring(tree, pretty_print=True)


if __name__ == '__main__':
    print make_feed()
