====================
maxrichter.github.io
====================

This is the Tech Blog from Max.

Manage
------

.. code-block:: bash

    1. Create venv: python -m venv venv
    2. Install requirements.txt
    3. Run: pelican-quickstart
    4. Try it out: make devserver --> http://localhost:8000/
    5. Add content:
        - Add .rst into content page
    6. Change the theme:
        - git clone --recursive https://github.com/getpelican/pelicanthemes
        - Copy the theme into maxrichter.github.io project folder
        - Adapt pelicanconf.py:
            - Add: THEME = './attila/'
    7. Publish to GitHub pages:
        - pelican content -o output -s pelicanconf.py
        - ghp-import output -b gh-pages
        - git push https://github.com/MaxRichter/maxrichter.github.io.git gh-pages:master