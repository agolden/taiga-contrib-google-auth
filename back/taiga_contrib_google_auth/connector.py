# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json

from collections import namedtuple
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taiga.base.connectors.exceptions import ConnectorBaseException


class GoogleApiError(ConnectorBaseException):
    pass


######################################################
## Data
######################################################

CLIENT_ID = getattr(settings, "GOOGLE_API_CLIENT_ID", None)
CLIENT_SECRET = getattr(settings, "GOOGLE_API_CLIENT_SECRET", None)
REDIRECT_URI = getattr(settings, "GOOGLE_API_REDIRECT_URI", None)

URL = getattr(settings, "GOOGLE_URL", "https://accounts.google.com/")
API_URL = getattr(settings, "GOOGLE_API_URL",  "https://www.googleapis.com/")
API_RESOURCES_URLS = {
    "login": {
        "authorize": "o/oauth2/auth",
        "access-token": "oauth2/v3/token"
    },
    "user": {
        "profile": "plus/v1/people/me",
        "emails": "user/emails"
    }
}


HEADERS = {"Accept": "application/json",}

AuthInfo = namedtuple("AuthInfo", ["access_token"])
User = namedtuple("User", ["id", "username", "full_name", "email", "bio"])
Email = namedtuple("Email", ["email", "is_primary"])


######################################################
## utils
######################################################

def _build_url(*args, **kwargs) -> str:
    """
    Return a valid url.
    """
    resource_url = API_RESOURCES_URLS
    for key in args:
        resource_url = resource_url[key]

    if kwargs:
        resource_url = resource_url.format(**kwargs)

    return urljoin(API_URL, resource_url)


def _get(url:str, headers:dict) -> dict:
    """
    Make a GET call.
    """
    response = requests.get(url, headers=headers)

    data = response.json()
    if response.status_code != 200:
        raise GoogleApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


def _post(url:str, params:dict, headers:dict) -> dict:
    """
    Make a POST call.
    """
    response = requests.post(url, params=params, headers=headers)
    data = response.json()
    if response.status_code != 200 or "error" in data:
        raise GoogleApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


######################################################
## Simple calls
######################################################

def login(access_code:str, client_id:str=CLIENT_ID, client_secret:str=CLIENT_SECRET,
          headers:dict=HEADERS, redirect_uri:str=REDIRECT_URI):
    """
    Get access_token fron an user authorized code, the client id and the client secret key.
    (See https://developer.google.com/v3/oauth/#web-application-flow).
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise GoogleApiError({"error_message": _("Login with google account is disabled. Contact "
                                                     "with the sysadmins. Maybe they're snoozing in a "
                                                     "secret hideout of the data center.")})

    url = _build_url("login", "access-token")
    params={"code": access_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri}
    data = _post(url, params=params, headers=headers)
    return AuthInfo(access_token=data.get("access_token", None))


def get_user_profile(headers:dict=HEADERS):
    """
    Get authenticated user info.
    (See https://developer.google.com/v3/users/#get-the-authenticated-user).
    """
    url = _build_url("user", "profile")
    data = _get(url, headers=headers)
    return User(id=data.get("id", None),
                username=data.get("name", None).get("givenName", None) + data.get("name", None).get("familyName", None),
                full_name=(data.get("displayName", None) or ""),
                email=(data.get("emails", None)[0].get("value", None) or ""),
		bio=(data.get("bio", None) or ""))


def get_user_emails(headers:dict=HEADERS) -> list:
    """
    Get a list with all emails of the authenticated user.
    (See https://developer.google.com/v3/users/emails/#list-email-addresses-for-a-user).
    """
    url = _build_url("user", "emails")
    data = _get(url, headers=headers)
    return [Email(email=e.get("email", None), is_primary=e.get("primary", False))
                    for e in data]


######################################################
## Convined calls
######################################################

def me(access_code:str) -> tuple:
    """
    Connect to a google account and get all personal info (profile and the primary email).
    """
    auth_info = login(access_code)
    
    headers = HEADERS.copy()
    headers["Authorization"] = "Bearer {}".format(auth_info.access_token)

    user = get_user_profile(headers=headers)
    # emails = get_user_emails(headers=headers)

    # primary_email = next(filter(lambda x: x.is_primary, emails))
    # return primary_email.email, user
    return user

