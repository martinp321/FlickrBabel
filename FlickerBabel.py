"""
FlickrBabel
-----------
Given a set of photos with tags, this module will:
- translate those tags into languages available on flickr
- add those tags to your photo
- search for any groups relevant to the photo's tags
- add your photo to those group photo pools

To use:
- Install flickrapi and microsofttranslator modules
- Get api keys for flickr and microsofttranslator
- Fill in those details below.
- On flickr:
  - Create an album called show.
  - Make all photos in show private.
  - Add english tags to those photos.
- Run this.

Word of caution - please be light on the daily runs of this to prevent annoying people.
"""

from multiprocessing import Process, current_process
import logging
from Flickr import Flickr
from common import FLICKR_CONFIG
logging.captureWarnings(True)

def printMe(msg):
    """ simpler helper to print with process id """
    print '{}: {}'.format(current_process(), msg)


def worker(photoIDs=None, flickr=None, photosToProcess=2):
    """ worker """
    photo_count = 0

    for photo_id in photoIDs:
        if photo_count >= photosToProcess:
            break

        printMe('Getting info for {}'.format(photo_id))
        photoinfo = flickr.getPhotoInfo(photo_id)

        printMe('Getting tags')
        newTags = flickr.getNewTags(photoinfo)


        flickr.addTagsToPhoto(photo_id, newTags)
        groupsForTags = flickr.getGroups(newTags)

        if groupsForTags:
            printMe('Setting photo public and removing from queue {}'.format(photo_id))
            flickr.removePhotoFromQueue(photo_id)

            printMe('Adding photo to groups {}'.format(photo_id))
            flickr.addPhotoToGroups(groupsForTags, photo_id)
            photo_count += 1


def main(workers=2):
    """ driver """
    flickr = Flickr(**FLICKR_CONFIG)
    photoIDs = flickr.getPhotoIDs()

    start, end = 0, 0
    for _ in range(workers):
        start, end = end, end + (len(photoIDs) / workers)
        kwargs = {'photoIDs': photoIDs[start:end], 'flickr': flickr}
        Process(target=worker, kwargs=kwargs).start()


if __name__ == '__main__':
    main()
