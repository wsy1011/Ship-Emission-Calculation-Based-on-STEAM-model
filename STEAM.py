import math

class LoadFactor:
    def __init__(self, u, va_max):
        self.Va = u
        self.Vmax = va_max

    def _calculate_load_factor(self, low_load_factors):
        m = (self.Va / self.Vmax) ** 3
        x = m

        if m >= 0.2:
            return m
        elif 0.01 <= m < 0.2:
            k = int(m * 100)
            k = max(1, min(k, len(low_load_factors) - 1))
            return x * (low_load_factors[k - 1] - (m * 100 - k) * \
                         (low_load_factors[k - 1] - low_load_factors[k]))
        elif 0 < m < 0.01:
            k = int(m * 100)
            k = min(k, len(low_load_factors) - 2)
            return x * (low_load_factors[k] + abs(m * 100 - 1) * \
                         (low_load_factors[k] - low_load_factors[k + 1]))
        else:
            return x * low_load_factors[0]

    def NOx_LF(self):
        NOx_LLF = [11.47, 4.63, 2.92, 2.21, 1.83, 1.60, 1.45, 1.35, 1.27, 1.22, 
                   1.17, 1.14, 1.11, 1.08, 1.06, 1.05, 1.03, 1.02, 1.01, 1.00]
        return self._calculate_load_factor(NOx_LLF)

    def CO_LF(self):
        CO_LLF = [19.32, 9.68, 6.46, 4.86, 3.89, 3.25, 2.79, 2.45, 2.18, 1.96, 
                  1.79, 1.64, 1.52, 1.41, 1.32, 1.24, 1.17, 1.11, 1.05, 1.00]
        return self._calculate_load_factor(CO_LLF)

    def PM_LF(self):
        PM_LLF = [19.17, 7.29, 4.33, 3.09, 2.44, 2.04, 1.79, 1.61, 1.48, 1.38, 
                  1.30, 1.24, 1.19, 1.15, 1.11, 1.08, 1.06, 1.04, 1.02, 1.00]
        return self._calculate_load_factor(PM_LLF)

    def SO2_LF(self):
        SO2_LLF = [19.17, 7.29, 4.33, 3.09, 2.44, 2.04, 1.79, 1.61, 1.48, 1.38, 
                  1.30, 1.24, 1.19, 1.15, 1.11, 1.08, 1.06, 1.04, 1.02, 1.00]
        return self._calculate_load_factor(SO2_LLF)

    def CO2_LF(self):
        CO2_LLF = [5.82, 3.28, 2.44, 2.01, 1.76, 1.59, 1.47, 1.38, 1.31, 1.25, 
                   1.21, 1.17, 1.14, 1.11, 1.08, 1.06, 1.04, 1.03, 1.01, 1.00]
        return self._calculate_load_factor(CO2_LLF)

def calculate_emissions(u, T, va_max, P_m, P_a, LF_a, EF_m_NOx, EF_a_NOx, EF_m_CO, EF_a_CO, EF_m_PM, EF_a_PM, EF_m_SO2, EF_a_SO2, EF_m_CO2, EF_a_CO2):
    LF = LoadFactor(u, va_max)
    emission_NOx = P_m * LF.NOx_LF() * T * EF_m_NOx + P_a * LF_a * T * EF_a_NOx
    emission_CO = P_m * LF.CO_LF() * T * EF_m_CO + P_a * LF_a * T * EF_a_CO
    emission_PM = P_m * LF.PM_LF() * T * EF_m_PM + P_a * LF_a * T * EF_a_PM
    emission_SO2 = P_m * LF.SO2_LF() * T * EF_m_SO2 + P_a * LF_a * T * EF_a_SO2
    emission_CO2 = P_m * LF.CO2_LF() * T * EF_m_CO2 + P_a * LF_a * T * EF_a_CO2
    return {
        "NOx": emission_NOx,
        "CO": emission_CO,
        "PM": emission_PM,
        "SO2": emission_SO2,
        "CO2": emission_CO2
    }

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Calculate ship emissions based on speed and time.")
    parser.add_argument("--speed", type=float, required=True, help="Ship speed in knots.")
    parser.add_argument("--time", type=float, required=True, help="Time interval in seconds.")
    parser.add_argument("--speed_max", type=float, required=True, help="Designed Ship speed in knots.")
    parser.add_argument("--power_main", type=float, required=True, help="Main engine power in kW.")
    parser.add_argument("--power_aux", type=float, required=True, help="Auxiliary engine power in kW.")

    args = parser.parse_args()

    # Default parameters
    
    LF_a = 0.13
    EF_m_NOx = 13.2
    EF_a_NOx = 13.9
    EF_m_CO = 1.1
    EF_a_CO = 1.1
    EF_m_PM = 0.47
    EF_a_PM = 0.49
    EF_m_SO2 = 3.97
    EF_a_SO2 = 4.00
    EF_m_CO2 = 677.9
    EF_a_CO2 = 690.7

    emissions = calculate_emissions(
        args.speed, args.time, args.speed_max, args.power_main, args.power_aux, LF_a,
        EF_m_NOx, EF_a_NOx, EF_m_CO, EF_a_CO,
        EF_m_PM, EF_a_PM, EF_m_SO2, EF_a_SO2,
        EF_m_CO2, EF_a_CO2
    )

    print("Emissions:")
    for pollutant, value in emissions.items():
        print(f"{pollutant}: {value:.2f}")

if __name__ == "__main__":
    main()
