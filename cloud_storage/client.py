from googleapiclient.discovery import build, DISCOVERY_URI
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from httplib2 import Http
import json

GCS_SCOPE = [
    'https://www.googleapis.com/auth/devstorage.read_write'
]

DEFAULT_MIMETYPE = 'application/octet-stream'

def get_client(json_key=None, json_key_file=None, project_id=None, service_url=None):

    with open(json_key_file, 'r') as key_file:
        json_key = json.load(key_file)

    scope = GCS_SCOPE

    if json_key:
        credentials = _credentials().from_json_keyfile_dict(json_key,
                                                            scopes=scope)
        if not project_id:
            project_id = json_key['project_id']

    if service_url is None:
        service_url = DISCOVERY_URI

    gcs_service = _get_gcs_service(credentials=credentials,
                                   service_url=service_url)

    return GCSClient(gcs_service, project_id)


def _get_gcs_service(credentials=None, service_url=None):
    assert credentials, 'Must provide ServiceAccountCredentials'
    
    http = credentials.authorize(Http())

    service = build('storage', 'v1', http=http,
                    discoveryServiceUrl=service_url)
    return service

def _credentials():
    """Import and return SignedJwtAssertionCredentials class"""
    from oauth2client.service_account import ServiceAccountCredentials

    return ServiceAccountCredentials


class GCSClient(object):

    def __init__(self, gcs_service, project_id):
        self.gcs = gcs_service
        self.project_id = project_id

    def upload_from_filename(self, filename=None, bucket_id=None, blob_location=None):
        media = MediaFileUpload(filename)
        if not media.mimetype():
            media = MediaFileUpload(filename, DEFAULT_MIMETYPE)
        self.gcs.objects().insert(bucket=bucket_id, name=blob_location, media_body=media).execute()
