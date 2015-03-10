# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014 Anler Hernández <hello@anler.me>
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

import pytest

from unittest.mock import patch, Mock
from taiga_contrib_google_auth import connector as google


def test_url_builder():
    assert (google._build_url("login", "authorize") ==
            "https://accounts.google.com/o/oauth2/auth")
    assert (google._build_url("login","access-token") ==
            "https://www.googleapis.com/oauth2/v3/token")
    assert (google._build_url("user", "profile") ==
            "https://api.google.com/user")
    assert (google._build_url("user", "emails") ==
            "https://api.google.com/user/emails")


def test_login_without_settings_params():
    with pytest.raises(google.GoogleApiError) as e, \
            patch("taiga_contrib_google_auth.connector.requests") as m_requests:
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"access_token": "xxxxxxxx"}

        auth_info = google.login("*access-code*", "**client-id**", "*ient-secret*", google.HEADERS)
    assert e.value.status_code == 400
    assert "error_message" in e.value.detail


def test_login_success():
    with patch("taiga_contrib_google_auth.connector.requests") as m_requests, \
            patch("taiga_contrib_google_auth.connector.CLIENT_ID") as CLIENT_ID, \
            patch("taiga_contrib_google_auth.connector.CLIENT_SECRET") as CLIENT_SECRET:
        CLIENT_ID = "*CLIENT_ID*"
        CLIENT_SECRET = "*CLIENT_SECRET*"
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"access_token": "xxxxxxxx"}

        auth_info = google.login("*access-code*", "**client-id**", "*client-secret*", google.HEADERS)

        assert auth_info.access_token == "xxxxxxxx"
        m_requests.post.assert_called_once_with("https://google.com/login/oauth/access_token",
                                                headers=google.HEADERS,
                                                params={'code': '*access-code*',
                                                        'scope': 'user:emails',
                                                        'client_id': '**client-id**',
                                                        'client_secret': '*client-secret*'})


def test_login_whit_errors():
    with pytest.raises(google.GoogleApiError) as e, \
            patch("taiga_contrib_google_auth.connector.requests") as m_requests, \
            patch("taiga_contrib_google_auth.connector.CLIENT_ID") as CLIENT_ID, \
            patch("taiga_contrib_google_auth.connector.CLIENT_SECRET") as CLIENT_SECRET:
        CLIENT_ID = "*CLIENT_ID*"
        CLIENT_SECRET = "*CLIENT_SECRET*"
        m_requests.post.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"error": "Invalid credentials"}

        auth_info = google.login("*access-code*", "**client-id**", "*ient-secret*", google.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 200
    assert e.value.detail["error"] == "Invalid credentials"


def test_get_user_profile_success():
    with patch("taiga_contrib_google_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = {"id": 1955,
                                        "login": "mmcfly",
                                        "name": "martin seamus mcfly",
                                        "bio": "time traveler"}

        user_profile = google.get_user_profile(google.HEADERS)

        assert user_profile.id == 1955
        assert user_profile.username == "mmcfly"
        assert user_profile.full_name == "martin seamus mcfly"
        assert user_profile.bio == "time traveler"
        m_requests.get.assert_called_once_with("https://api.google.com/user",
                                               headers=google.HEADERS)


def test_get_user_profile_whit_errors():
    with pytest.raises(google.GoogleApiError) as e, \
            patch("taiga_contrib_google_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 401
        m_response.json.return_value = {"error": "Invalid credentials"}

        auth_info = google.get_user_profile(google.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 401
    assert e.value.detail["error"] == "Invalid credentials"


def test_get_user_emails_success():
    with patch("taiga_contrib_google_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 200
        m_response.json.return_value = [{"email": "darth-vader@bttf.com", "primary": False},
                                        {"email": "mmcfly@bttf.com", "primary": True}]

        emails = google.get_user_emails(google.HEADERS)

        assert len(emails) == 2
        assert emails[0].email == "darth-vader@bttf.com"
        assert not emails[0].is_primary
        assert emails[1].email == "mmcfly@bttf.com"
        assert emails[1].is_primary
        m_requests.get.assert_called_once_with("https://api.google.com/user/emails",
                                               headers=google.HEADERS)


def test_get_user_emails_whit_errors():
    with pytest.raises(google.GoogleApiError) as e, \
            patch("taiga_contrib_google_auth.connector.requests") as m_requests:
        m_requests.get.return_value = m_response = Mock()
        m_response.status_code = 401
        m_response.json.return_value = {"error": "Invalid credentials"}

        emails = google.get_user_emails(google.HEADERS)
    assert e.value.status_code == 400
    assert e.value.detail["status_code"] == 401
    assert e.value.detail["error"] == "Invalid credentials"


def test_me():
    with patch("taiga_contrib_google_auth.connector.login") as m_login, \
            patch("taiga_contrib_google_auth.connector.get_user_profile") as m_get_user_profile, \
            patch("taiga_contrib_google_auth.connector.get_user_emails") as m_get_user_emails:
        m_login.return_value = google.AuthInfo(access_token="xxxxxxxx")
        m_get_user_profile.return_value = google.User(id=1955,
                                                      username="mmcfly",
                                                      full_name="martin seamus mcfly",
                                                      bio="time traveler")
        m_get_user_emails.return_value = [google.Email(email="darth-vader@bttf.com", is_primary=False),
                                          google.Email(email="mmcfly@bttf.com", is_primary=True)]

        email, user = google.me("**access-code**")

        assert email == "mmcfly@bttf.com"
        assert user.id == 1955
        assert user.username == "mmcfly"
        assert user.full_name == "martin seamus mcfly"
        assert user.bio == "time traveler"

        headers = google.HEADERS.copy()
        headers["Authorization"] = "token xxxxxxxx"
        m_get_user_profile.assert_called_once_with(headers=headers)
        m_get_user_emails.assert_called_once_with(headers=headers)
