"""pixabay_scraper.py
Get a bunch of image urls from a search result url

Usage:
    pixabay_scraper.py -h
    pixabay_scraper.py -n=<number> [options]

Options
    -h                  Show this page
    -n=<number>         Number of results to get
    --search=<str>      Search pixabay
    --img_type=<str>    Search with type
"""

import pixabay
from docopt import docopt
from random import randint

def scrape(n, search=None, img_type=None):
    """ Scrape images and filter """
    api_key = None
    with open('api_key.txt', 'r') as key_file:
        api_key = key_file.read().strip()

    if search is None:
        search = ''
    if img_type is None:
        img_type = 'illustration'
    # load api key
    image_searcher = pixabay.Image(api_key)

    ims = image_searcher.search(orientation='vertical',
                                safesearch='false',
                                order='latest',
                                page=1,#randint(1, int(200/int(n))),
                                editors_choice='false',
                                per_page=int(n),
                                q=search,
                                image_type=img_type)
    # Get hits
    hits = ims['hits']

    image_urls = []
    for hit in hits:
        image_urls.append(hit['largeImageURL'])

    return image_urls

def main(args):
    """ Entry point """
    urls = scrape(int(args['-n']), search=args['--search'], img_type=args['--img_type'])
    print(urls)

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    main(ARGS)
