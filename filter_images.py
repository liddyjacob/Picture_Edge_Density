"""filter_images.py
Get a bunch of image urls from a search result url

Usage:
    filter_images.py -h
    filter_images.py -n=<number> [options]
    filter_images.py --url=<url> [options]

Options
    -h                  Show this page
    -n=<number>         Number of results to get
    --search=<str>      Search pixabay
    --img_type=<str>    Search with type
    --url=<url>         Filter a single image
"""

import pixabay
from docopt import docopt
from pixabay_scraper import scrape
from dixit_lib import url_to_image
from dixit_lib import find_edges
import cv2 as cv
import numpy
import os

LOWER_LIMIT = .025
UPPER_LIMIT = .16
DESIRED_RATIO = 4.0 / 3.0
ERROR = .1

def main(args):
    """ Entry point """
    urls = [args['--url']]
    if args['--url'] is None:
        urls = scrape(int(args['-n']), search=args['--search'], img_type=args['--img_type'])
    i = 0;
    for fname in os.listdir('image_database'):
        name = fname.split('.')[0]
        if i <= int(name):
            i = int(name) + 1



    for url in urls:
        # GET IMAGES:
        image = url_to_image(url)
        image_cv = numpy.array(image)

        # FILTER IMAGES:
        # Image must be RGB.
        if image_cv.shape[2] is not 3:
            continue

        # Image must have desired ratio +- error
        (h, w) = image_cv.shape[:2]
        ratio = float(h) / float(w)
        if ratio < DESIRED_RATIO * (1.0 - ERROR):
            continue
        if ratio > DESIRED_RATIO * (1.0 + ERROR):
            continue

        # Image cannot be too complex, but also must not be too simple
        edges_cv = find_edges(image_cv)
        nonzero = numpy.count_nonzero(edges_cv)
        percentage = float(nonzero) / float(h * w)

        print(percentage)
        if percentage > UPPER_LIMIT or percentage < LOWER_LIMIT:
            continue
        #-------------------
        # If image passes, write:

        cv.imwrite('image_database/' + str(i) + '.png', image_cv)
        i += 1;
        #-------------------


if __name__ == '__main__':
    ARGS = docopt(__doc__)
    main(ARGS)
