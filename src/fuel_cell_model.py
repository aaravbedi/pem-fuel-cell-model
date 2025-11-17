import numpy as np

class PEMFuelCellModel:
    def __init__(
        self,
        temperature_K: float = 353.15,
        nernst_voltage_V: float = 1.18,   
        membrane_resistance_ohm_cm2: float = 0.2,
        exchange_current_density_A_cm2: float = 1e-3,
        limiting_current_density_A_cm2: float = 2.0,
        alpha: float = 0.5,                 
        R: float = 8.314,                  
        F: float = 96485.0,             
        num_cells: int = 50,
        active_area_cm2: float = 50.0,
    ):
        self.T = temperature_K
        self.E_nernst = nernst_voltage_V
        self.R = R
        self.F = F

        self.R_m = membrane_resistance_ohm_cm2
        self.i0 = exchange_current_density_A_cm2
        self.i_lim = limiting_current_density_A_cm2
        self.alpha = alpha

        self.num_cells = num_cells
        self.active_area_cm2 = active_area_cm2

    def activation_overpotential(self, i_A_cm2: np.ndarray) -> np.ndarray:
        i = np.maximum(i_A_cm2, 1e-8)
        return (self.R * self.T / (self.alpha * self.F)) * np.log(i / self.i0)

    def ohmic_overpotential(self, i_A_cm2: np.ndarray) -> np.ndarray:
        return i_A_cm2 * self.R_m

    def concentration_overpotential(self, i_A_cm2: np.ndarray) -> np.ndarray:
        i_ratio = np.clip(i_A_cm2 / self.i_lim, 0.0, 0.999999)
        return -(self.R * self.T / self.F) * np.log(1.0 - i_ratio)

    def cell_voltage(self, i_A_cm2: np.ndarray) -> np.ndarray:
        V_act = self.activation_overpotential(i_A_cm2)
        V_ohm = self.ohmic_overpotential(i_A_cm2)
        V_conc = self.concentration_overpotential(i_A_cm2)

        V = self.E_nernst - V_act - V_ohm - V_conc
        V = np.maximum(V, 0.0)
        return V

    def stack_voltage(self, i_A_cm2: np.ndarray) -> np.ndarray:
        return self.cell_voltage(i_A_cm2) * self.num_cells

    def power_density_W_cm2(self, i_A_cm2: np.ndarray) -> np.ndarray:
        V = self.cell_voltage(i_A_cm2)
        return i_A_cm2 * V

    def efficiency(self, i_A_cm2: np.ndarray) -> np.ndarray:
        V = self.cell_voltage(i_A_cm2)
        return np.where(self.E_nernst > 0, V / self.E_nernst, 0.0)
