Customs Filters Steps Pipelines
===============================

The purpose of these pipelines is to use the filters that are structured in `openedx-filters`_ and
implemented in `edx-platform`_. From the creation of a custom filter pipeline in this space, we can
overwrite the one of the structure in ``openedx-filter`` so that it executes the action that we want, where
the filter is implemented in ``edx-platform``.

 .. _openedx-filters: https://github.com/openedx/openedx-filters
 .. _edx-platform: https://github.com/openedx/edx-platform

Filters steps list:
-------------------

* `FilterUserCourseEnrollmentsByTenant`_: Filters the course enrollments of a user from the tenant site where the request is made.

.. _FilterUserCourseEnrollmentsByTenant: ./pipeline.py#L9

How to add a new Filter Step:
-----------------------------

Add a new Filter Step in `pipeline.py`_ file, note that this must exist in ``openedx-filters`` in order to be
called. Find a `list of filters`_ that exist so far and `how to implement`_ it.

.. _pipeline.py: ./pipeline.py
.. _list of filters: https://github.com/openedx/openedx-filters/blob/main/openedx_filters/learning/filters.py
.. _how to implement: https://github.com/openedx/openedx-filters/tree/main/docs/decisions
