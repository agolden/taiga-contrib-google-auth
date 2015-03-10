Taiga contrib google auth
=========================

![Kaleidos Project](http://kaleidos.net/static/img/badge.png "Kaleidos Project")
[![Managed with Taiga.io](https://taiga.io/media/support/attachments/article-22/banner-gh.png)](https://taiga.io "Managed with Taiga.io")

The Taiga plugin for google authentication.

Installation
------------

### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-google-auth` with:

```bash
  pip install taiga-contrib-google-auth
```

Modify your settings/local.py and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_google_auth"]
```

### Taiga Front

Download in your `dist/js/` directory of Taiga front the `taiga-contrib-google-auth` compiled code:

```bash
  cd dist/js
  wget "https://raw.googleusercontent.com/taigaio/taiga-contrib-google-auth/stable/front/dist/google_auth.js"
```

Download in your `dist/images/contrib` directory of Taiga front the `taiga-contrib-google-auth` google icon:

```bash
  cd dist/images/contrib
  wget "https://raw.googleusercontent.com/taigaio/taiga-contrib-google-auth/stable/front/images/contrib/google-logo.png"
```

Include in your dist/js/conf.json in the contribPlugins list the value `"/js/google_auth.js"`:

```json
...
    "contribPlugins": ["/js/google_auth.js"]
...
```

Running tests
-------------

3/10/15: PLEASE NOTE: These tests were just copied from the github plugin and are not yet operational.  They will be updated shortly.

We only have backend tests, you have to add your taiga-back directory to the
PYTHONPATH environment variable, and run py.test, for example:

```bash
  cd back
  add2virtualenv /home/taiga/taiga-back/
  py.test
```
