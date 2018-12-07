========
cnftools
========

.. image:: https://circleci.com/gh/easyas314159/cnftools/tree/master.svg?style=svg
    :target: https://circleci.com/gh/easyas314159/cnftools/tree/master

A collection of tools for working with and generating Dimacs CNF files.

------------
Installation
------------

::

	pip install cnftools

``cnftools`` is listed in `PyPI <https://pypi.org/project/cnftools/>`_ and
can be installed with ``pip``.

-----
Usage
-----

``cnftools`` exposes the ``cnf`` command-line interface for quickly generating
Dimacs CNF files typically for use with a SAT solver.

3cnf
====

Apply the Tseytin transformation [TSEY1970]_ to a CNF file producing an output
where all clauses contain 3 or fewer literals.

::

	cnf 3cnf -i [input.cnf]

simplify
========

Simply the input CNF file.

::

	cnf simplify -i [input.cnf] -o [output.cnf]

stats
=====

Provide details about contents of a CNF file. This includes the number of literals,
the total number of clauses, as well as a histogram of clause lengths.

::

	cnf stats -i [input.cnf]

karps21
=======

This sub-command exposes utilities for generating CNF files based on
Karp's 21 NP-Complete problems [KARP1972]_. For more details on this utility
use the ``-h``/``--help`` option.

::

	cnf karps21 --help

----------
References
----------

.. [TSEY1970] Tseitin, Grigori. "On the complexity of derivation in propositional calculus." *Studies in constructive mathematics and mathematical logic* (1968): 115-125.
.. [COOK1971] Cook, Stephen A. "The complexity of theorem-proving procedures." *Proceedings of the third annual ACM symposium on Theory of computing*. ACM, 1971.
.. [KARP1972] Karp, Richard M. "Reducibility among combinatorial problems." *Complexity of computer computations*. Springer, Boston, MA, 1972. 85-103.
