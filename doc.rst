Documentation
==============

Search
-------------
| Search is limited to 100 results.
| Search results only include categories: main game, dlc, expansion, standalone expansion, episode, remake and remaster.
| Full list is available here: https://api-docs.igdb.com/#game-enums.

Npm module dependencies
------------------------
* ``roboto-fontface``, ``@mdi/font``, ``webfontloader`` are ``vuetify`` dependencies

Dev

* ``@typescript-eslint/parser`` is ``@typescript-eslint/eslint-plugin`` dependency
* ``sass`` is required for processing ``sass`` files

These warnings are to be ignored as webpack is not used.

* ``null-loader@npm:4.0.1 [1a5b9]            → ^4.0.0 || ^5.0.0 ✘``
* ``vue-cli-plugin-vuetify@npm:2.5.1 [51c7d] → ^4.0.0 || ^5.0.0 ✘``

Cache
--------
Redis is used for caching.

Assets used
--------------
* `Image Not Found icon`_

Cron jobs
------------
Cron jobs are run with `GitHub Actions`_. Time zone is UTC.

- ``Remove unused games`` runs at 07:00 UTC (03:00 EDT) on the first day of the month
- ``DB backup`` runs at 09:00 UTC (05:00 EDT) daily


CI/CD
----------
`GitHub Actions`_  are used for CI/CD.

Tests are automatically run on pull requests and in master or dev branches.

Deployment is automatically done in master branch.

The following GitHub Actions are used:

* Checkout_
* `Setup Python`_
* `Setup Node.js environment`_
* Codecov_
* `Docker Login`_
* `Build and push Docker images`_
* `GitHub Action for DigitalOcean - doctl`_
* `Kubectl tool installer`_
* `DigitalOcean Spaces Upload Action`_
* Cache_
* `Docker Setup Buildx`_
* `Set Timezone`_

.. _Image Not Found icon: https://uxwing.com/image-not-found-icon/

.. _GitHub Actions: https://github.com/features/actions

.. _Checkout: https://github.com/marketplace/actions/checkout
.. _Setup Python: https://github.com/marketplace/actions/setup-python
.. _Setup Node.js environment: https://github.com/marketplace/actions/setup-node-js-environment
.. _Codecov: https://github.com/marketplace/actions/codecov
.. _Docker Login: https://github.com/marketplace/actions/docker-login
.. _Build and push Docker images: https://github.com/marketplace/actions/build-and-push-docker-images
.. _GitHub Action for DigitalOcean - doctl: https://github.com/marketplace/actions/github-action-for-digitalocean-doctl
.. _Kubectl tool installer: https://github.com/marketplace/actions/kubectl-tool-installer
.. _DigitalOcean Spaces Upload Action: https://github.com/marketplace/actions/digitalocean-spaces-upload-action
.. _Cache: https://github.com/marketplace/actions/cache
.. _Docker Setup Buildx: https://github.com/marketplace/actions/docker-setup-buildx
.. _Set Timezone: https://github.com/marketplace/actions/set-timezone
