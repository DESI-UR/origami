ORIGAMI - Sub-divide
====================

In the University of Rochester's DESI group, Dahlia Veyrat reworked the crossing number calculation done by ``origamitag.c`` into two new files: ``origamidiv.c`` and ``origamicomb.c``. In short, Veyrat's version takes in the desired sub-cube size, calculates the CN of particles in each sub-cube in parallel, and combines them into one output allowing for CN classifications on large N-body simulations (`Veyrat, Douglass & BenZvi 2023 <https://doi.org/10.3847/1538-4357/acf4f5>`_). This was implemented to allow ORIGAMI to be used on AbacusSummit simulations (`Maksimova et al. 2021, MNRAS, 508, 4017 <https://doi.org/10.1093/mnras/stab2484>`_) and similarly large simulations.

Installing
----------

The sub-divide version adds two programs to the standard ORIGAMI routines:

- ``origamidiv`` tags one sub-cube of the simulation at a time, together with
  a buffer zone of ``nbuf`` particles on each side, so that the full particle
  set never has to be held in memory.
- ``origamicomb`` stitches the sub-cube tag files back into a single
  full-box ``tag.dat`` that ``origamihalo`` and ``origamienv`` can read.

Both live in ``code/`` alongside the rest of ORIGAMI. First follow the
standard installation steps on the :doc:`origami` page (unpacking and
building Qhull, and pointing ``QLIB`` and ``QINC`` in the ``Makefile`` at it).
Qhull is only needed for the tessellation; ``origamidiv`` and
``origamicomb`` do not use it.

Then, from ``code/``:

1. Build ``origamidiv`` together with the other ORIGAMI routines::

      make origami

   This builds ``origamitag``, ``origamidiv``, ``origamihalo``,
   ``origamicen`` and ``origamienv``. Note that plain ``make`` (the ``all``
   target) does **not** build ``origamidiv``.

2. Build ``origamicomb``. It has no ``Makefile`` target and does not use
   ``readfiles.c``, so compile it directly::

      gcc -O2 -o origamicomb origamicomb.c

.. note::

   The CMake build (``CMakeLists.txt`` in the repository root) does not yet
   build ``origamidiv`` or ``origamicomb``; use the ``Makefile`` for the
   sub-divide version.

.. note::

   On macOS, ``gcc`` is Apple clang, which rejects ``-fopenmp``. Use a
   Homebrew ``gcc-NN`` (set ``CC`` in the ``Makefile``), or clang with
   ``-Xpreprocessor -fopenmp -lomp`` from ``libomp``. Recent compilers also
   reject an implicit function declaration in ``readfiles.c``; add
   ``-Wno-error=implicit-function-declaration`` to ``CFLAGS``.

The sub-divide version adds a new ``nbuf`` parameter (the buffer width, in
particles). Because ``readfiles.c`` is shared by every program, **every**
parameter file must now contain the ``nbuf`` line, in the position shown in
``code/parameters_example.txt``, even for runs that do not use
``origamidiv``.

Running
-------
