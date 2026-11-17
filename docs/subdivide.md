# ORIGAMI - Sub-divide

In the University of Rochester's DESI group Dahlia Veyrat reworked the crossing number calculation done by `origamitag.c` into two new files: `origamidiv.c` and `origamicomb.c`. In short, this version takes in the desired sub-cube size, calculates the CNs of particles in each sub-cube in parallel, and combines them into one output allowing for CN classifications on large N-body simulations ([Veyrat, Douglass & BenZvi 2023]([https://doi.org/10.3847/1538-4357/acf4f5])). This was implemented to allow ORIGAMI to be used on AbacusSummit simulations ([Maksimova et al. 2021, MNRAS, 508, 4017](https://doi.org/10.1093/mnras/stab2484)) and similarly large simulations. 

## Installing

## Running
