================
A Spider for R18
================

This is a scrapy project for R18_ web scraping, and also as an example for Scrapy technology and CI tools from `Github Marketplace`_.

.. _R18: https://www.r18.com/
.. _`Github Marketplace`: https://github.com/marketplace

Overview
========

.. image:: https://bestpractices.coreinfrastructure.org/projects/2827/badge
    :alt: CII Best Practices
    :target: https://bestpractices.coreinfrastructure.org/projects/2827

.. image:: https://mperlet.github.io/pybadge/badges/9.5.svg
    :alt: pylint Score

.. image:: https://circleci.com/gh/scrapedia/r18/tree/master.svg?style=svg
    :target: https://circleci.com/gh/scrapedia/r18/tree/master

.. image:: https://codebeat.co/badges/7feab55f-a261-4ee9-8acd-32c7e2ca7cdb
    :target: https://codebeat.co/projects/github-com-scrapedia-r18-master

.. image:: https://api.codacy.com/project/badge/Grade/3eb532d4ac6442a5896a0cc4abef2e03
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/grammy-jiang/r18?utm_source=github.com&utm_medium=referral&utm_content=scrapedia/r18&utm_campaign=Badge_Grade_Settings

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
    :alt: License: AGPL v3

.. image:: https://depshield.sonatype.org/badges/scrapedia/r18/depshield.svg
    :target: https://depshield.github.io
    :alt: DepShield Badge

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Code style: black

Requirements
============

.. image:: https://pyup.io/repos/github/scrapedia/r18/python-3-shield.svg
   :target: https://pyup.io/repos/github/scrapedia/r18/
   :alt: Python 3

.. image:: https://pyup.io/repos/github/scrapedia/r18/shield.svg
   :target: https://pyup.io/repos/github/scrapedia/r18/
   :alt: pyup
   
.. image:: https://snyk.io/test/github/scrapedia/r18/badge.svg
    :target: https://snyk.io/test/github/scrapedia/r18
    :alt: Known Vulnerabilities

.. image:: https://img.shields.io/badge/renovate-enabled-brightgreen.svg
    :target: https://renovatebot.com
    :alt: Renovate enabled

* Python 3.6+
* Scrapy 1.6.0
* Fully tested on Linux, but it should works on Windows, Mac OSX, BSD

Usage
=====

Pipenv is adopted for the virtual environment management. Create the virtual environment and activate it:

  pipenv install && pipenv shell

Go to the project root and run the command:

  python run/run.py

Or, you can run the spider directly:

  pipenv run python run/run.py

Scrapy Technology Used In This Spider
=====================================

* SitemapSpider_
* `Stats Collection`_
* `Requests and Responses`_
* `Item Loader`_
* `Spider Contracts`_
* `Downloading and processing files and images`_

.. _SitemapSpider: https://docs.scrapy.org/en/latest/topics/spiders.html#sitemapspider
.. _`Stats Collection`: https://docs.scrapy.org/en/latest/topics/stats.html
.. _`Requests and Responses`: https://docs.scrapy.org/en/latest/topics/request-response.html
.. _`Item Loader`: https://docs.scrapy.org/en/latest/topics/loaders.html
.. _`Spider Contracts`: https://docs.scrapy.org/en/latest/topics/contracts.html
.. _`Downloading and processing files and images`: https://docs.scrapy.org/en/latest/topics/media-pipeline.html

CI Used In This Spider
======================

Spider Contracts
----------------

Tox_
----

.. _Tox: https://tox.readthedocs.io/en/latest/

CircleCI_
---------

.. _CircleCI: https://circleci.com/gh/scrapedia

TODO
====

* [X] Move zh page re-direction to en to a downloader middleware
* [ ] Docker configurations for MongoBD
