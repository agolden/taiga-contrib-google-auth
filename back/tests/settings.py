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

from settings.development import *

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
CELERY_ALWAYS_EAGER = True
CELERY_ENABLED = False

MEDIA_ROOT = "/tmp"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
INSTALLED_APPS = INSTALLED_APPS + [
    "taiga_contrib_github_auth",
]
INSTALLED_APPS = set(INSTALLED_APPS) - set(["taiga.hooks.github", "taiga.hooks.gitlab", "taiga.hooks.bitbucket"])

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": None,
    "user": None,
    "import-mode": None,
    "import-dump-mode": None,
}
