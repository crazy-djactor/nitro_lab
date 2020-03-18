from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False

    def get_created_time(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def path(self, name):
        pass


class PublicMediaStorage(S3Boto3Storage):

    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

    def get_created_time(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def path(self, name):
        pass


class PrivateMediaStorage(S3Boto3Storage):

    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def get_created_time(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def path(self, name):
        pass
