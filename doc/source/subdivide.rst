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

   **macOS.** On macOS, ``gcc`` is Apple clang, which rejects
   ``-fopenmp``. If not installed, install GCC with ``brew install gcc``. Then, you need to edit ``CC`` and ``CFLAGS`` (lines 4–5 of
   ``code/Makefile``). 

   .. code-block:: make

      CC = gcc-16
      CFLAGS = -O2 -fopenmp -Wno-error=implicit-function-declaration

   **To do this without editing the** ``Makefile``, pass them on the command
   line, for example:

   .. code-block:: sh

      make origami CFLAGS="-O2 -fopenmp -Wno-error=implicit-function-declaration"

   ``origamicomb`` is compiled by hand (step 3 above) and doesn't need any of these flags.

Input File Formats
------------------

Parameter File
^^^^^^^^^^^^^^

The sub-divide version reads the same parameter file as standard ORIGAMI,
with one new parameter, ``nbuf``. The format is not flexible: every parameter must be present, in the order shown in
``code/parameters_example.txt``, whether or not the routine you are running
uses it.

.. warning::

   The parser (``read_parameters`` in ``code/readfiles.c``) does not
   understand comments. It skips a fixed number of lines and reads the
   values in a fixed order, so the layout of ``parameters_example.txt`` has to
   be kept exactly.

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
Just like the original version of ORIGAMI, Veyrat's version only works for simulations that have grid-like initial conditions. ORIGAMI uses the particle ID to determine the particle's initial position. That is, the particle ID's must be ID = :math:`x + yN + zN^2`. The code requires the particles to be sorted by their ID. 

The particle count in the file must be 8 bytes, unlike the original ORIGAMI's 4 byte requirement. This is due to a change in the datatype `origamidiv` expects. 

Furthermore, unlike the original version of ORIGAMI `numfiles` must be 0 since Veyrat's version is not compatible with the Gadget reader. 

Running
-------

**Particle position file downloaded**

If you have a particle position file downloaded already -- with proper ID ordering -- the first step is to adjust the parameter file. Download ``parameters_example.txt`` from the repo and adjust ``posfile`` to your file's name, ``outdir`` and ``taglabel`` to the desired output directory and filename for the CN data, ``boxsize`` to the width of your position file, and ``np1d`` to the number of particles in one dimension of your position file. Calculating CNs is then two steps: ``origamidiv`` tags each sub-cube, and ``origamicomb`` stitches the sub-cubes back together. In the directory with ``parameters_example.txt`` and the compiled ``origamidiv`` and ``origamicomb`` executables, run the two steps below.

Step 1: tag each sub-cube with ``origamidiv``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``origamidiv`` takes three arguments, the parameter file, ``ndiv`` and ``divid``:

.. code-block:: sh

   ./origamidiv parameters_example.txt <ndiv> <divid>

- ``ndiv`` is the number of divisions per side, so the box is split into
  ``ndiv``\ ³ sub-cubes. It is read from the **command line**; the ``ndiv``
  line in the parameter file is only used by VOBOZ.
- ``divid`` is the sub-cube to tag, from 0 to ``ndiv``\ ³ − 1.

Run it once for every ``divid``. For example, with ``ndiv`` = 2 there are
8 sub-cubes:

.. code-block:: sh

   export OMP_NUM_THREADS=8      # only used when nsplit > 1
   for divid in $(seq 0 7); do
       ./origamidiv parameters_example.txt 2 $divid
   done

Each run loads one sub-cube plus ``nbuf`` particles of buffer on every side,
computes the CNs, and writes only the sub-cube (not the buffer) to
``<outdir><taglabel>_tag_<divid>.dat``: (``np1d``/``ndiv``)³ bytes with no
header. The runs do not depend on each other, so on a cluster each
``divid`` can be submitted as its own job (for example as a job array).

Step 2: combine the sub-cubes with ``origamicomb``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``origamicomb`` does not read the parameter file. Pass it the same
``taglabel``, ``outdir``, ``np1d`` and ``ndiv`` used above, in this order:

.. code-block:: sh

   ./origamicomb <taglabel> <outdir> <np1d> <ndiv>

   # with the values in parameters_example.txt:
   ./origamicomb veyrat_test1_n64 ../runs/test/ 64 2

It reads every ``<taglabel>_tag_<divid>.dat`` file, puts the particles back
in ID order and writes ``<outdir><taglabel>tag.dat``. That file overwrites
any existing one and has the same format as the output of the standard
``origamitag``: an int32 particle count, then one byte per particle with
0 = void, 1 = wall, 2 = filament, 3 = halo. ``origamihalo`` and
``origamienv`` can read it directly (see :doc:`origami`).

.. note::

   ``origamicomb`` does not check its arguments. If one is missing it
   crashes instead of printing an error. As in the parameter file,
   ``outdir`` is joined directly onto the filename, so it needs the
   trailing ``/``.

Choosing ``ndiv``, ``nbuf`` and ``nsplit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``ndiv``: ``np1d`` must be divisible by ``ndiv``\ ³, not just by
  ``ndiv``. ``origamidiv`` only checks ``ndiv``, but ``origamicomb`` quits
  if ``np1d`` is not a multiple of ``ndiv``\ ³. For example, ``np1d`` = 64
  works with ``ndiv`` = 2 or 4, and ``np1d`` = 2304 works with ``ndiv`` = 4.
- ``nbuf``: besides the buffer width, ``nbuf`` is also how far along each
  row of the initial grid ``origamidiv`` searches for a crossing. The
  standard ``origamitag`` searches ``np1d``/4 particles, so
  ``nbuf`` = ``np1d``/4 should reproduce its CNs (16 for the 64³ example).
  A smaller ``nbuf`` uses less memory but can miss crossings with particles
  further away along the row.
- ``nsplit``: ``np1d``/``ndiv`` + 2 ``nbuf`` must be divisible by
  ``nsplit``. If it is not, some rows are skipped and those particles are
  tagged as void without any warning. With the example values,
  64/2 + 2 × 16 = 64.
- Very large runs: ``origamicomb`` writes the particle count in the
  header as an int32, which overflows above about 1290³ particles. The tag
  bytes are still correct, but read the file using ``np1d``\ ³ as the count
  instead of the header.

Checking the output
^^^^^^^^^^^^^^^^^^^

The fraction of particles in each CN class is a quick sanity check:

.. code-block:: python

   import numpy as np

   with open("../runs/test/veyrat_test1_n64tag.dat", "rb") as f:
       n = np.fromfile(f, np.int32, 1)[0]
       tag = np.fromfile(f, np.uint8, n)
   print(np.bincount(tag, minlength=4) / tag.size)   # [void, wall, filament, halo]

For comparison, Veyrat, Douglass & BenZvi (2023) find 30.8% / 19.4% / 18.2% /
31.6% for CN = 0 / 1 / 2 / 3 in AbacusSummit Hugebase.

**Example notebook**

:doc:`notebooks/running_veyrat_origami_RTD` walks through the same steps
from Python: it builds a 64³ test simulation with a single wall, runs
``origamidiv`` and ``origamicomb``, and reads back the CNs.
