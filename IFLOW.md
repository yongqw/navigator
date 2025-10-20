# iFlow 上下文信息 (IFLOW.md)

## 项目概览

此目录 (`C:\Users\yowan\Local\navigator`) 是一个 Python 虚拟环境 (venv) 的根目录。虚拟环境用于隔离 Python 项目的依赖包，确保项目之间的依赖不会相互干扰。

主要组成部分:
- `venv/`: 包含虚拟环境的所有文件。
  - `Scripts/`: 包含 Python 解释器和脚本的可执行文件 (如 `python.exe`, `pip.exe`)。
  - `Lib/site-packages/`: 包含安装在此虚拟环境中的所有第三方库和包。
- `IFLOW.md`: 此文件，提供给 iFlow CLI 作为上下文信息。

## 关键技术和架构

- **Python 版本**: 根据 `venv\pyvenv.cfg` 文件，此虚拟环境是基于 Python 3.11.9 创建的。
- **包管理**: 使用 `pip` 作为包管理器。
- **已安装的核心库**: 
  - `numpy` (2.3.4): 用于科学计算的基础库。
  - `scipy` (1.16.2): 用于科学和技术计算的库。
  - `matplotlib` (3.10.7): 用于创建静态、动画和交互式可视化。
  - `Pillow` (12.0.0): Python 图像处理库。
  - `fontTools` (4.60.1): 用于处理字体文件的库。

## 构建和运行

由于这是一个 Python 虚拟环境而非一个可直接运行的应用程序项目，因此没有传统的“构建”步骤。使用方法如下：

1.  **激活虚拟环境**:
    *   Windows (命令提示符): `C:\Users\yowan\Local\navigator\venv\Scripts\activate.bat`
    *   Windows (PowerShell): `C:\Users\yowan\Local\navigator\venv\Scripts\Activate.ps1`
2.  **使用 Python 和 pip**:
    *   激活后，可以使用 `python` 命令运行 Python 脚本。
    *   使用 `pip install <package_name>` 安装新的包。
    *   使用 `pip list` 查看已安装的包。
3.  **停用虚拟环境**:
    *   运行 `deactivate` 命令。

## 开发约定

此目录本身不包含源代码或特定的开发约定。它是一个环境容器。任何在此环境中进行的开发都将遵循所安装库（如 NumPy, SciPy 的文档）的约定以及开发者自己的项目结构和规范。