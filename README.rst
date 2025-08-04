Games
==========================================================

|Deployment Status| |Codecov|

| The web application on Django_ 5, Vue.js_ 3, Vuetify_ 3, `Material Design Icons`_ 7.
| Create game lists like "Want to Play", "Playing", "Beaten", "On Hold".
| See more information here - https://games.samarchyan.me/about/
| The website is live here - https://games.samarchyan.me.

See more documentation_.

Development
----------------------------
| You can use ubuntu-vm_ as a development VM if needed.
| Also you can use macos-setup_ if you are on Mac.

1. Use mysql-docker_ to bring up MySQL in Docker
2. Use redis-docker_ to bring up Redis in Docker
3. Run ``make install-deps`` if necessary (only on Ubuntu)
4. Run ``make bootstrap``
5. Run ``make createsuperuser`` to create a superadmin user
6. Edit files ``env_custom.sh`` and ``env_secrets.sh``

For development run:

.. code-block:: bash

    make run
    make dev


Run ``make help`` to get a list of all available commands.

| Open http://localhost:5173/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.

Run in Docker:

1. Run ``make docker-build-dev``
2. Edit file ``docker_secrets.env``
3. Run ``make docker-run``

Production
------------
To use production commands:

1. Edit file ``db_env_prod.sh``
2. Activate the kubectl context

Used API
-----------
* IGDB_

.. |Codecov| image:: https://codecov.io/gh/desecho/games/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/desecho/games

.. |Deployment Status| image:: https://github.com/desecho/games/actions/workflows/deployment.yaml/badge.svg
   :target: https://github.com/desecho/games/actions/workflows/deployment.yaml

.. _documentation: https://github.com/desecho/games/blob/main/doc.rst

.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _macos-setup: https://github.com/desecho/macos-setup
.. _mysql-docker: https://github.com/desecho/mysql-docker
.. _redis-docker: https://github.com/desecho/redis-docker

.. _IGDB: https://www.igdb.com/

.. _Django: https://www.djangoproject.com/
.. _Vue.js: https://vuejs.org/
.. _Vuetify: https://vuetifyjs.com/
.. _Material Design Icons: https://materialdesignicons.com/
