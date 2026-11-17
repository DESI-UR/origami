.. ORIGAMI documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ORIGAMI's documentation!
===================================

ORIGAMI identifies the morphology of dark matter particles in N-body
simulations. Each particle is classified as a void, wall, filament, or halo
particle by counting the number of orthogonal axes along which it has
undergone a shell-crossing
(`Falck, Neyrinck & Szalay 2012 <https://ui.adsabs.harvard.edu/abs/2012ApJ...754..126F>`_). ORIGAMI was adapted to handle N-body simulations for :math:`N > 512^3` by dividing the work of ORIGAMI into sub-cubes (`Veyrat, Douglass & BenZvi 2023 <https://doi.org/10.3847/1538-4357/acf4f5>`_). This documentation describes the installation and use of both ORIGAMI and the ORIGAMI sub-divide logic.

.. toctree::
   :maxdepth: 2
   :caption: ORIGAMI

   origami

.. toctree::
   :maxdepth: 2
   :caption: ORIGAMI - Sub-divide

   subdivide


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
