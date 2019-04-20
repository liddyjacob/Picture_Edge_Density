"""dixit_lib
A library for dixit clone

"""
from PIL import Image
import requests
from io import BytesIO
import sys
import numpy
from matplotlib import pyplot
import cv2 as cv

DIAMETER_RATIO = 30.0 / (1859.0 * 2596.0)
SIGMA_RATIO = 75.0 / (1859.0 * 2596.0)

def url_to_image(url):
    response = requests.get(url)
    if response is None:
        raise IOError("Unsuccessful response.\nurl: " + url)

    img = Image.open(BytesIO(response.content));
    return img

def find_edges(cv_img):
    """ Find the edges of a cv_image """
    (h, w)   = cv_img.shape[:2]

    cv_blur  = cv.bilateralFilter(cv_img, int(DIAMETER_RATIO * h * w),
                                  SIGMA_RATIO * float(h * w),
                                  SIGMA_RATIO * float(h * w / 2))
    cv_gray  = cv.cvtColor(cv_blur, cv.COLOR_BGR2GRAY)
    cv_edge  = cv.Canny(cv_gray, 50, 200)
    return cv_edge

def __test__():
    """ Test the functions in this library """
    try:
        url_to_image("www.asd.q")
        sys.exit("URL was not valid! Test failed")
    except IOError as err:
        print("URL test 1 succeeded")


    try:
        url_to_image("https://images.unsplash.com/photo-1555083892-97490c72c90c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1859&q=80")
        print("URL test 2 succeeded")
    except IOError as err:
        print("URL test 2 failed")

    img = url_to_image("https://images.unsplash.com/photo-1555083892-97490c72c90c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1859&q=80")
    cv_img   = numpy.array(img)
    cv_edges  = find_edges(cv_img)
    cv.imwrite("edges.png", cv_edges)

    url = 'https://cdn.pixabay.com/photo/2017/07/03/20/17/abstract-2468874_960_720.jpg'
    img = url_to_image(url)
    cv_img   = numpy.array(img)
    cv_edges  = find_edges(cv_img)
    cv.imwrite(url.split('/')[-1], cv_edges)


    img = url_to_image("https://images.unsplash.com/photo-1555083892-97490c72c90c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1859&q=80")
    cv_img   = numpy.array(img)
    cv_edges  = find_edges(cv_img)
    cv.imwrite("edges.png", cv_edges)

if __name__ == "__main__":
    __test__()

