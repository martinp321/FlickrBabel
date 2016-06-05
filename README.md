FlickrBabel
-----------
Given a set of photos with tags, this module will:
- translate those tags into languages available on flickr
- add those tags to your photo
- search for any groups relevant to the photo's tags
- add your photo to those group photo pools

To use:
- Install flickrapi and microsofttranslator modules
  - pip install flickrapi
  - pip install microsofttranslator
- Get api keys for flickr and microsofttranslator
  - flickr - https://www.flickr.com/services/apps/create/apply
  - ms - https://blogs.msdn.microsoft.com/translation/gettingstarted1/
- Fill those details in the common.py module

- On flickr:
  - Create an album called show.
  - Make all photos in show private.
  - Add english tags to those photos.
- Run via 'python FlickerBabel.py'

Word of caution - please be light on the daily runs of this to prevent annoying people.

