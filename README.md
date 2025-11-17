# PEM Fuel Cell Performance Model

This is a small Python model for a proton exchange membrane (PEM) fuel cell.  
The goal is to play with the basic relationships between:

- current density  
- cell voltage (polarization curve)  
- power density  
- and approximate efficiency

It’s not meant to be a high-fidelity CFD/electrochemistry model. It’s a compact, parametric model that’s easy to tweak when you’re thinking about stack sizing, performance trends, or doing quick back-of-the-envelope studies.

The model:

- takes in a set of PEM fuel cell parameters (temperature, membrane resistance, exchange current density, limiting current density, etc.),  
- computes the **activation**, **ohmic**, and **concentration** overpotentials,  
- subtracts them from an ideal Nernst voltage to get the cell voltage,  
- and sweeps over a range of current densities to produce:
  - a polarization curve (V–i),
  - power density vs current density,
  - a rough efficiency estimate.

The `scripts/run_polarization_sweep.py` script pulls it all together and generates plots.

```text
pem-fuel-cell-model/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── fuel_cell_model.py
└── scripts/
    └── run_polarization_sweep.py
