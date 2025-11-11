# STEAM.py 使用说明

## 概述

**STEAM.py** **是一个用于根据船舶航速和运行时间估算污染物排放量的小工具。它提供命令行入口（**main()**），也可以作为模块在其他 Python 脚本中直接调用** **calculate_emissions()** **函数。**
- 计算原理及参数来源：见Principle of Ship Emission Calculation.pdf
- 使用说明见：Readme.md
- 结合之前以前团队发过的文章里面的排放因子和IMO的取值共同取得参数，也可以直接调整为IMO参数
- 作者：王苏阳，河海大学, 2025年11月11日

## 要求

* **Python 3.6+（脚本未使用外部第三方库，只依赖标准库）**

## 支持的污染物

* **NOx**
* **CO**
* **PM**
* **SO2**
* **CO2**

## 主要函数

* **calculate_emissions(u, T, va_max, P_m, P_a, LF_a, EF_m_NOx, EF_a_NOx, EF_m_CO, EF_a_CO, EF_m_PM, EF_a_PM, EF_m_SO2, EF_a_SO2, EF_m_CO2, EF_a_CO2)**

  * **输入：一组与速度、功率、负荷因子、排放因子（EF）相关的参数**
  * **输出：字典，键为污染物名称，值为相应排放量（单位由参数决定，脚本中未显式转换）**
* **LoadFactor** **类：根据当前航速** **u** **和设计航速** **va_max** **计算不同污染物的主机负荷因子（LF）。**

## 命令行用法（PowerShell）

**示例：计算在给定参数下的排放量并打印到控制台**

**code**Powershell

```
python .\Scripts\STEAM.py --speed 12 --time 3600 --speed_max 20 --power_main 5000 --power_aux 200
```

**参数说明：**

* **--speed**（必需）：船速，单位为节（knots）。脚本中用作 Va。
* **--time**（必需）：时间间隔，单位为秒（seconds）。
* **--speed_max**（必需）：设计航速或最大航速，单位为节（knots）。
* **--power_main**（必需）：主机功率，单位为 kW（脚本中用作 P_m）。
* **--power_aux**（必需）：辅机功率，单位为 kW（脚本中用作 P_a）。

**示例输出（脚本运行后，会打印如下格式）：**

**code**Code

```
Emissions:
NOx: 12345.67
CO: 123.45
PM: 12.34
SO2: 56.78
CO2: 987654.32
```

> **注：上述数值为示例格式，真实数值取决于输入参数和默认排放因子。**

## 默认参数（脚本内设定）

* **辅机平均负荷因子 LF_a = 0.13**
* **排放因子（主机/辅机，单位与脚本期待一致）**

  * **NOx: EF_m = 13.2, EF_a = 13.9**
  * **CO: EF_m = 1.1, EF_a = 1.1**
  * **PM: EF_m = 0.47, EF_a = 0.49**
  * **SO2: EF_m = 3.97, EF_a = 4.00**
  * **CO2: EF_m = 677.9, EF_a = 690.7**

**这些默认值会在脚本中** **main()** **中被使用。如果你通过命令行运行脚本，目前脚本并不提供覆盖这些 EF 的参数（除非修改脚本），但你可以在其他 Python 程序中调用** **calculate_emissions()** **并传入自定义的 EF 值。**

## 在其他 Python 脚本中使用

**你可以直接导入并调用** **calculate_emissions**：

**code**Python

```
from Scripts.STEAM import calculate_emissions

# 示例参数
u = 12.0            # 节
T = 3600            # 秒
va_max = 20.0       # 设计航速（节）
P_m = 5000.0        # 主机功率（kW）
P_a = 200.0         # 辅机功率（kW）
LF_a = 0.13
EF_m_NOx = 13.2
EF_a_NOx = 13.9
# ... 其它 EF 同上

emissions = calculate_emissions(
    u, T, va_max, P_m, P_a, LF_a,
    EF_m_NOx, EF_a_NOx,
    1.1, 1.1,      # EF CO (示例)
    0.47, 0.49,    # EF PM
    3.97, 4.00,    # EF SO2
    677.9, 690.7   # EF CO2
)
print(emissions)
```

**注意：根据你的项目结构，如果直接运行该导入示例，可能需要将项目根目录（**e:\Codes\AIS\AISwang**）添加到** **PYTHONPATH**，或将 **Scripts** **目录作为包处理（添加** **__init__.py**），或者使用相对导入。

## 假设与注意事项

* **负荷因子（LF）计算基于脚本内置的查表/插值逻辑，使用 Va/Vmax 的立方作为基础权重。**
* **脚本中** **m = (Va / Vmax) ** 3**；当 m 值处于不同区间时，会使用不同的插值或表值策略。
* **单位一致性：脚本并未对输入单位做变换，确保以说明中的单位传入参数（节、秒、kW）。**
* **若需逐项自定义 EF（排放因子）或 LF_a，应通过直接调用** **calculate_emissions()** **并传入自定义值来实现。**

---

# Ship-Emission-Calculation-Based-on-STEAM-model

# STEAM.py Usage Instructions

## Overview

**STEAM.py** **is a small utility for estimating pollutant emissions based on ship speed and operating time. It provides a command-line entry point (**main()**) and can also be used as a module by directly calling the** **calculate_emissions()** **function in other Python scripts.**

- Ship Emission Calculation Based on the STEAM Model
- For calculation principles and parameter sources, see "Principle of Ship Emission Calculation.pdf"
- For usage instructions, see Readme.md
- Parameters are derived from a combination of emission factors from previous team publications and IMO values, and can be directly adjusted to use IMO parameters.
- Author: Wangsuyang, Hohai University, November 11, 2025

## Requirements

* **Python 3.6+ (The script does not use any external third-party libraries and relies only on the standard library)**

## Supported Pollutants

* **NOx**
* **CO**
* **PM**
* **SO2**
* **CO2**

## Main Functions

* **calculate_emissions(u, T, va_max, P_m, P_a, LF_a, EF_m_NOx, EF_a_NOx, EF_m_CO, EF_a_CO, EF_m_PM, EF_a_PM, EF_m_SO2, EF_a_SO2, EF_m_CO2, EF_a_CO2)**

  * **Input**: A set of parameters related to speed, power, load factor, and emission factor (EF).
  * **Output**: A dictionary where keys are pollutant names and values are the corresponding emission amounts (the unit is determined by the input parameters, as the script does not perform explicit unit conversions).
* **LoadFactor** **class: Calculates the main engine load factor (LF) for different pollutants based on the current speed** **u** **and the design speed** **va_max**.

## Command Line Usage (PowerShell)

**Example: Calculate emissions with given parameters and print to the console.**

**code**Powershell

```
python .\Scripts\STEAM.py --speed 12 --time 3600 --speed_max 20 --power_main 5000 --power_aux 200
```

**Argument Descriptions:**

* **--speed** **(required): Ship speed in knots. Used as** **Va** **in the script.**
* **--time** **(required): Time interval in seconds.**
* **--speed_max** **(required): Design speed or maximum speed in knots.**
* **--power_main** **(required): Main engine power in kW. Used as** **P_m** **in the script.**
* **--power_aux** **(required): Auxiliary engine power in kW. Used as** **P_a** **in the script.**

**Example Output (after running the script, output will be printed in this format):**

**code**Code

```
Emissions:
NOx: 12345.67
CO: 123.45
PM: 12.34
SO2: 56.78
CO2: 987654.32
```

> **Note: The values above are for demonstration purposes. The actual results depend on the input parameters and default emission factors.**

## Default Parameters (Hardcoded in the script)

* **Average auxiliary engine load factor** **LF_a** **= 0.13**
* **Emission Factors (main engine / auxiliary engine, units should be consistent with the script's expectations)**

  * **NOx: EF_m = 13.2, EF_a = 13.9**
  * **CO: EF_m = 1.1, EF_a = 1.1**
  * **PM: EF_m = 0.47, EF_a = 0.49**
  * **SO2: EF_m = 3.97, EF_a = 4.00**
  * **CO2: EF_m = 677.9, EF_a = 690.7**

**These default values are used in the** **main()** **function of the script. If you run the script from the command line, there is currently no option to override these EFs via arguments (unless you modify the script). However, you can call** **calculate_emissions()** **from another Python program and pass in custom EF values.**

## Usage in Other Python Scripts

**You can directly import and call** **calculate_emissions**:

**code**Python

```
from Scripts.STEAM import calculate_emissions

# Example parameters
u = 12.0            # knots
T = 3600            # seconds
va_max = 20.0       # Design speed (knots)
P_m = 5000.0        # Main engine power (kW)
P_a = 200.0         # Auxiliary engine power (kW)
LF_a = 0.13
EF_m_NOx = 13.2
EF_a_NOx = 13.9
# ... other EFs as above

emissions = calculate_emissions(
    u, T, va_max, P_m, P_a, LF_a,
    EF_m_NOx, EF_a_NOx,
    1.1, 1.1,      # EF CO (example)
    0.47, 0.49,    # EF PM
    3.97, 4.00,    # EF SO2
    677.9, 690.7   # EF CO2
)
print(emissions)
```

**Note: Depending on your project structure, to run this import example directly, you might need to add the project root directory (e.g.,** **e:\Codes\AIS\AISwang**) to your **PYTHONPATH**, treat the **Scripts** **directory as a package (by adding an** **__init__.py** **file), or use relative imports.**

## Assumptions and Notes

* **The Load Factor (LF) calculation is based on the script's built-in lookup** table/interpolation **logic, using the cube of** **Va/Vmax** **as the base weight.**
* **In the script,** **m = (Va / Vmax) ** 3**. Different interpolation or table-lookup strategies are used when **m** **falls into different ranges.**
* **Unit Consistency**: The script does not perform unit conversions. Ensure that parameters are passed in the units specified in the instructions (knots, seconds, kW).
* **To customize individual EFs (Emission Factors) or** **LF_a**, you should call the **calculate_emissions()** **function directly and pass in your custom values.**
