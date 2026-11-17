ORIGAMI - Sub-divide
====================

In the University of Rochester's DESI group, Dahlia Veyrat reworked the crossing number calculation done by ``origamitag.c`` into two new files: ``origamidiv.c`` and ``origamicomb.c``. In short, Veyrat's version takes in the desired sub-cube size, calculates the CN of particles in each sub-cube in parallel, and combines them into one output allowing for CN classifications on large N-body simulations (`Veyrat, Douglass & BenZvi 2023 <https://doi.org/10.3847/1538-4357/acf4f5>`_). This was implemented to allow ORIGAMI to be used on AbacusSummit simulations (`Maksimova et al. 2021, MNRAS, 508, 4017 <https://doi.org/10.1093/mnras/stab2484>`_) and similarly large simulations.

Installing & Compiling
----------------------

The sub-divide version adds two programs to the standard ORIGAMI routines:

- ``origamidiv`` tags one sub-cube of the simulation at a time, together with
  a buffer zone of ``nbuf`` particles on each side, so that the full particle
  set never has to be held in memory.
- ``origamicomb`` stitches the sub-cube tag files back into a single
  full-box ``tag.dat`` that ``origamihalo`` and ``origamienv`` can read.

Both live in ``code/`` alongside the rest of ORIGAMI. Qhull is **not**
required to compute CNs: ``origamitag``, ``origamidiv`` and
``origamicomb`` do not use it, and ``make origami`` builds without it. Qhull
is only needed for the VOBOZ tessellation (``make voboz``), which
``origamihalo``, ``origamienv`` and ``origamicen`` require to group halos.
If you need those, first follow the Qhull steps on the :doc:`origami` page.

To compile the CN logic:

1. Download the code or clone the repo::

      git clone https://github.com/DESI-UR/origami.git

2. cd to ``code/`` and build ``origamidiv`` together with the other ORIGAMI routines::

      make origami

   This builds ``origamitag``, ``origamidiv``, ``origamihalo``,
   ``origamicen`` and ``origamienv``. Note that plain ``make`` (the ``all``
   target) does **not** build ``origamidiv``.

3. Build ``origamicomb``. It has no ``Makefile`` target and does not use
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

Input File Formats
------------------

Parameter File
^^^^^^^^^^^^^^

The sub-divide version reads the same parameter file as standard ORIGAMI,
with one new parameter, ``nbuf``. The format is not flexible: every parameter must be present, in the order shown in
``code/parameters_example.txt``, whether or not the routine you are running
uses it.

.. list-table::
   :header-rows: 1
   :widths: 15 60 25

   * - Parameter
     - Description
     - Used by
   * - ``posfile``
     - Full location of particle position file
     - voboz, tag, div, cen
   * - ``outdir``
     - Directory where output will be written (include the trailing ``/``)
     - voboz, tag, div, halo, env, cen
   * - ``taglabel``
     - Label NAME describing this run
     - voboz, tag, div, halo, env, cen
   * - ``boxsize``
     - Length of simulation cube in same units as positions
     - voboz, tag, div, cen
   * - ``np1d``
     - 1-D number of particles, i.e. cube root of total; **must be divisible
       by the** ``ndiv`` **given to** ``origamidiv``
     - tag, div
   * - ``nsplit``
     - Split volume into ``nsplit``\ ³ sub-volumes for OpenMP; for div,
       ``np1d``/``ndiv`` + 2 ``nbuf`` must be divisible by ``nsplit``
     - tag, div
   * - ``numfiles``
     - For Gadget input, # of particles per snapshot; 0 otherwise. **Must be
       0 for div.**
     - voboz, tag, div, cen
   * - ``nbuf``
     - **New.** 1-D number of particle buffer added to each side of sub-cube.
     - div
   * - ``buffer``
     - Buffer size around each sub-cube (defaults to 0.1). Not for CN.
     - voboz
   * - ``ndiv``
     - Number of divisions (defaults to 2, giving 8 sub-cubes). Not for CN.
     - voboz
   * - ``volcut``
     - Volume (i.e. 1/density) cut which defines a halo "core"
     - halo
   * - ``npmin``
     - Minimum number of particles per halo
     - halo
   * - ``halolabel``
     - Label HNAME describing these halos
     - halo, env, cen

``origamicomb`` does not read the parameter file; it takes its inputs on
the command line (see Running).

Particle Positions 
^^^^^^^^^^^^^^^^^^
Just like the original version of ORIGAMI, Veyrat's version only works for simulations that have grid-like initial conditions. ORIGAMI uses the particle ID to determine the particle's initial position. That is, the particle ID's must be ID = :math: `x + yN + zN^2`. The code requires the particles to be sorted by their ID. 

The particle count in the file must be 8 bytes, unlike the original ORIGAMI's 4 byte requirement. This is due to a change in the datatype `origamidiv` expects. 

Furthermore, unlike the original version of ORIGAMI `numfiles` must be 0 since Veyrat's version is not compatible with the Gadget reader. 

Running
-------
