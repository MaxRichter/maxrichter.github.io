====================
maxrichter.github.io
====================

This is the Tech Blog from Max.

Manage
------

.. code-block:: bash

    https://opensource.com/article/19/5/run-your-blog-github-pages-python

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
        Run Pelican to generate the static HTML files in output:
            - pelican content -o output -s pelicanconf.py
        Use ghp-import to add the contents of the output directory to the master branch:
            - ghp-import -m "Generate Pelican site" --no-jekyll -b master output
        Push the local master branch to the remote repo:
            - git push origin master
        Commit and push the new content to the content branch:
            $ git add content
            $ git commit -m 'added a first post, a photo and an about page'
            $ git push origin content

Seperation of content and publishing content

.. code-block:: bash

    $ git add .
    $ git commit -m 'initial pelican commit to content'
    $ git push origin content