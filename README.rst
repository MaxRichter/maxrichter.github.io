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
--------------------------------------------

Add all the Pelican-generated files to the content branch of the local Git repo, commit the changes, and push the local changes to the remote repo hosted on GitHub by entering:

.. code-block:: bash

    $ git add .
    $ git commit -m 'initial pelican commit to content'
    $ git push origin content

This isn't super exciting, but it will be handy if we need to revert edits to one of these files.

Finally getting somewhere
-------------------------

OK, now you can get bloggy! All of your blog posts, photos, images, PDFs, etc., will live in the content directory, which is initially empty. To begin creating a first post and an About page with a photo, enter:

.. code-block:: bash

    $ cd content
    $ mkdir pages images
    $ cp /Users/username/SecretStash/HotPhotoOfMe.jpg images
    $ touch first-post.md
    $ touch pages/about.md

Publish
-------

Don't worry; the payoff is coming!

All that's left to do is:

- Run Pelican to generate the static HTML files in output:

.. code-block:: bash

    $ pelican content -o output -s publishconf.py

- Use ghp-import to add the contents of the output directory to the master branch:

.. code-block:: bash

    $ ghp-import -m "Generate Pelican site" --no-jekyll -b master output

- Push the local master branch to the remote repo:

.. code-block:: bash

    $ git push origin master

- Commit and push the new content to the content branch:

.. code-block:: bash

    $ git add content
    $ git commit -m 'added a first post, a photo and an about page'
    $ git push origin content

OMG, I did it!
--------------
Now the exciting part is here when you get to view what you've published for everyone to see! Open your browser and enter:

https://maxrichter.github.io