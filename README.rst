Games
==========================================================

|Deployment Status| |Requirements Status| |Codecov|

| The web application on Django_ 4, Vue.js_ 3, Vuetify_ 3, `Material Design Icons`_. Create game lists like "Want to Play", "Playing", "Beaten", "On Hold".
| See more information here - https://games.samarchyan.me/about/

| Share your lists with friends.

| The website is live here - https://games.samarchyan.me.

See more documentation_.


Development
----------------------------
1. Use ubuntu-vm_ as a development VM
2. Use mysql-docker_ to bring up MySQL in Docker
3. Use redis-docker_ to bring up Redis in Docker
4. Run ``make bootstrap``
5. Run ``make createsuperuser`` to create a superadmin user
6. Edit files ``env_custom.sh`` and ``env_secrets.sh``

For development run:

```bash
make run
make dev
```

Run ``make help`` to get a list of all available commands.

| Open http://localhost:3000/ to access the web application.
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

.. |Requirements Status| image:: https://requires.io/github/desecho/games/requirements.svg?branch=master
   :target: https://requires.io/github/desecho/games/requirements/?branch=master

.. |Codecov| image:: https://codecov.io/gh/desecho/games/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/desecho/games

.. |Deployment Status| image:: https://github.com/desecho/games/actions/workflows/deployment.yaml/badge.svg
   :target: https://github.com/desecho/games/actions/workflows/deployment.yaml

.. _documentation: https://github.com/desecho/games/blob/master/doc.rst

.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _mysql-docker: https://github.com/desecho/mysql-docker
.. _redis-docker: https://github.com/desecho/redis-docker

.. _IGDB: https://www.igdb.com/

.. _Django: https://www.djangoproject.com/
.. _Vue.js: https://vuejs.org/
.. _Vuetify: https://vuetifyjs.com/
.. _Material Design Icons: https://materialdesignicons.com/
