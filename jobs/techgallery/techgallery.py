""""TechGallery class."""
import requests
import re
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'


class TechGallery(object):
    """TechGallery operations."""

    def __init__(self, config):
        """Init object.

        Config object must have a TECHGALLERY_ENDPOINT like this
        https://tech-gallery.appspot.com/_ah/api/rest/v1
        """
        self.config = config
        self.endpoint = config.get('TECHGALLERY_ENDPOINT')

    def get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.resources')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'knowledgemap_service_account.json')

        return ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)

    def profile(self, login):
        """Get a profile data by login.

        If profile was not found, then return status_code 404
        """
        # get access_token and setting header params
        headers = {}
        if self.config.get('TECHGALLERY_AUTH'):
            credentials = self.get_credentials()
            headers = {'Authorization': credentials.access_token}

        url = '%s/profile?email=%s@ciandt.com' % (self.endpoint, login)
        response = requests.get(url=url, headers=headers)
        # TODO: throw exception if response.status_code <> 200
        return response.json(), response.status_code

    def technology(self, id):
        """Get details about technology.

        If profile was not found, then return status_code 404
        """
        # get access_token and setting header params
        headers = {}
        if self.config.get('TECHGALLERY_AUTH'):
            credentials = self.get_credentials()
            headers = {'Authorization': credentials.access_token}

        url = '%s/technology/%s' % (self.endpoint, id)
        response = requests.get(url=url, headers=headers)

        return response.json(), response.status_code


black_list = {
    'backbone.js': 'backbone.js',
    'calabash': 'cabalash',
    'node.js': 'node.js',
    'asp.net core': 'asp.net_core',
    'asp.net webforms': 'asp.net_webforms',
    'asp.net webapi': 'asp.net_webapi',
    'asp.net mvc': 'asp.net_mvc',
    'quartz.net': 'quartz.net'
}


def convert_name_to_id(tech_name):
    r"""Convert technology name to id.

    This method make a string replace using a bellow rules
    public String convertNameToId(String name) {
        name = Normalizer.normalize(name, Normalizer.Form.NFD);
        name = name.replaceAll("[^\\p{ASCII}]", "");
        return name.toLowerCase()
            .replaceAll(" ", "_")
            .replaceAll("#", "_")
            .replaceAll("\\/", "_")
            .replaceAll("\\.", "");
      }

    """
    if tech_name:
        if tech_name.lower() in black_list:
            tech_key = black_list[tech_name.lower()]
        else:
            tech_key = re.sub('[#/ ]', '_', re.sub(
                '[^\x00-\x7F]', '_', re.sub(
                    '[.]', '', tech_name.lower())))

        return tech_key
