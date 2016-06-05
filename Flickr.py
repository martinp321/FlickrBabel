import json
import flickrapi
import random
from common import translate, SUPPORTED_LANGUAGES

class Flickr(object):
    """ hides nitty gritty details of dealing with flickr """
    def __init__(self, photoset_id=None, user_id=None, api_key=None, api_secret=None):
        self.photoset_id = photoset_id
        self.args = {'api_key' : api_key, 'user_id' : user_id, 'format' : 'json'}

        self.MAX_SEARCH_RESULTS = 600
        self.MAX_GROUPS_ON_PHOTO = 200
        self.MIN_GROUP_MEMBERSHIP = 2000
        self.MAX_TAGS = 53

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        if not self.flickr.token_valid(perms='write'):
            self.flickr.authenticate_via_browser(perms='write')

    def getPhotoIDs(self):
        """ returns a shuffled list of photo ids in the photoset """
        ret = self.flickr.photosets.getPhotos(photoset_id=self.photoset_id, **self.args)
        photoDicts = json.loads(ret)
        photoIDs = [photo['id'] for photo in photoDicts['photoset']['photo']]
        random.shuffle(photoIDs)
        return photoIDs

    def getSubscribedGroups(self):
        """ returns list of subscribed groups """
        groups = json.loads(self.flickr.people.getGroups(**self.args))
        return set(g['nsid'] for g in groups['groups']['group'])

    def getPhotoInfo(self, photo_id):
        """ returns photo info in form of json """
        return json.loads(self.flickr.photos.getInfo(photo_id=photo_id, **self.args))

    @staticmethod
    def getNewTags(photoinfo):
        """ returns translated photo tags + original tags """
        photoTags = [t['raw'] for t in photoinfo['photo']['tags']['tag'] if t.get('raw')]
        return set(translate(tag, language)
                   for tag in photoTags
                   for language in SUPPORTED_LANGUAGES)

    def addTagsToPhoto(self, photo_id, newTags):
        """ add new tags to photo """
        tags = ','.join(list(newTags)[:self.MAX_TAGS])
        self.flickr.photos.addTags(photo_id=photo_id, tags=tags, **self.args)

    def getGroups(self, newTags):
        """ finds groups which match interest relating to tags """
        def findGroupsForTag(tag=None):
            """ local func: given a tag, returns groups from search results """
            ret = self.flickr.groups.search(text=tag, per_page=self.MAX_SEARCH_RESULTS, **self.args)
            potentialGroups = json.loads(ret)['groups']['group']
            blockedWords = ['post', 'award', 'comment', 'invite']
            groupSet = set([])
            for group in potentialGroups:
                groupName = group['name'].lower()
                nsid = group['nsid']
                members = int(group['members'])

                largeMembership = members > self.MIN_GROUP_MEMBERSHIP
                noBlockedWords = not any([blockedWord in groupName for blockedWord in blockedWords])
                if noBlockedWords and largeMembership:
                    groupSet.add((nsid, groupName, members))
            return groupSet

        ### START ###
        return set(group
                   for newTag in newTags
                   for group in findGroupsForTag(newTag))

    def removePhotoFromQueue(self, photo_id):
        """ remove photos from show queue and set permissions to public """
        self.flickr.photos.setPerms(photo_id=photo_id,
                                    is_public=1,
                                    is_friend=1,
                                    is_family=1)
        self.flickr.photosets.removePhoto(photoset_id=self.photoset_id, photo_id=photo_id)

    def addPhotoToGroups(self, groupsForPhoto, photo_id):
        """ add photo to groups """
        subscribedGroups = self.getSubscribedGroups()
        group_count = 0
        sortedGroupsForPhoto = sorted(list(groupsForPhoto), key=lambda x: x[2], reverse=True)
        for group_id, _, _ in sortedGroupsForPhoto:
            if group_count >= self.MAX_GROUPS_ON_PHOTO:
                break

            if group_id not in subscribedGroups:
                self.flickr.groups.join(group_id=group_id, **self.args)
                subscribedGroups.add(group_id)

            ret = self.flickr.groups.pools.add(photo_id=photo_id, group_id=group_id, **self.args)
            added = json.loads(ret)['stat'] == 'ok'
            if added:
                group_count += 1
