import os
import numpy as np
import matplotlib.pyplot as plt
from src.fuel_cell_model import PEMFuelCellModel

def run_polarization_sweep():
    model = PEMFuelCellModel(
        temperature_K=353.15,
        nernst_voltage_V=1.18,
        membrane_resistance_ohm_cm2=0.2,
        exchange_current_density_A_cm2=1e-3,
        limiting_current_density_A_cm2=2.0,
        num_cells=50,
        active_area_cm2=50.0,
    )

    i_values = np.linspace(0.01, 1.8, 200)

    V_cell = model.cell_voltage(i_values)
    P_density = model.power_density_W_cm2(i_values)
    eta = model.efficiency(i_values)
    stack_power_W = P_density * model.active_area_cm2 * model.num_cells

    os.makedirs("outputs", exist_ok=True)

    plt.figure(figsize=(6, 4))
    plt.plot(i_values, V_cell, linewidth=2)
    plt.xlabel("Current density [A/cm²]")
    plt.ylabel("Cell voltage [V]")
    plt.title("PEM Fuel Cell Polarization Curve")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/polarization_curve.png", dpi=200)
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.plot(i_values, P_density, linewidth=2)
    plt.xlabel("Current density [A/cm²]")
    plt.ylabel("Power density [W/cm²]")
    plt.title("Power Density vs Current Density")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/power_density.png", dpi=200)
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.plot(i_values, eta, linewidth=2)
    plt.xlabel("Current density [A/cm²]")
    plt.ylabel("Efficiency [-]")
    plt.title("Approximate Efficiency vs Current Density")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/efficiency.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    run_polarization_sweep()
