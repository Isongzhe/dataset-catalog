# Modern Scientific Data Workflows with UV, Intake & Dask

A comprehensive workshop demonstrating modern Python tools for scientific data processing, covering environment management, data cataloging, and efficient computation.

## 🎯 Overview

This project provides hands-on tutorials for modernizing scientific data workflows using cutting-edge Python tools:

- **[UV](https://docs.astral.sh/uv/)**: Ultra-fast Python package and project management
- **[Intake](https://intake.readthedocs.io/)**: Unified data cataloging and access
- **[Dask](https://docs.dask.org/)**: Scalable parallel computing for data science
- **[CF Conventions](https://cfconventions.org/)**: Scientific metadata standards

## 📚 Workshop Content

### Part 1: UV - Modern Python Project Management
**Duration:** 10-20 minutes  
**File:** [`script/01_uv_introduction.ipynb`](script/01_uv_introduction.ipynb)

Learn to replace traditional Python tooling (`pip`, `venv`, `pip-tools`) with a single, blazingly fast solution:

- **Environment Setup**: Initialize projects with modern standards
- **Dependency Management**: 10-100x faster package resolution
- **Jupyter Integration**: Seamless kernel registration
- **Reproducibility**: Automatic lock files and version management

### Part 2: Intake + Dask - Scientific Data Processing
**Duration:** 20-30 minutes  
**File:** [`script/02_intake_and_dask.ipynb`](script/02_intake_and_dask.ipynb)

Master efficient processing of large scientific datasets:

- **Data Cataloging**: Unified access to multiple data formats
- **Lazy Evaluation**: Process datasets larger than memory
- **Scientific Standards**: CF-compliant metadata generation
- **Quality Assurance**: Automated compliance checking

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ installed
- Basic familiarity with Jupyter notebooks
- Understanding of scientific data formats (NetCDF, Zarr)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Isongzhe/dataset-catalog.git
   cd dataset-catalog
   ```

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set up the environment:**
   ```bash
   uv sync
   ```

4. **Register Jupyter kernel:**
   ```bash
   uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=<kernel-name>
   ```

5. **Start Jupyter:**
   ```bash
   uv run jupyter lab
   ```

6. **Select the "dataset-catalog" kernel** and open the workshop notebooks.

## 📁 Project Structure

```
dataset-catalog/
├── README.md                   # This file
├── pyproject.toml             # Modern Python project configuration
├── uv.lock                    # Locked dependency versions
├── script/                    # Workshop notebooks
│   ├── 01_uv_introduction.ipynb
│   └── 02_intake_and_dask.ipynb
├── catalogs/                  # Data catalog definitions
│   ├── era5_intake_catalog.yaml
│   ├── radar_intake_catalog.yaml
│   └── station_intake_catalog.yaml ## wait to update
```

## 🔧 Technologies Demonstrated

| Tool | Purpose | Benefits |
|------|---------|----------|
| **UV** | Package & environment management | 10-100x faster than pip, unified tooling |
| **Intake** | Data cataloging | Unified access, rich metadata, sharing |
| **Dask** | Parallel computing | Lazy evaluation, memory efficiency, scalability |
| **Xarray** | Scientific data structures | Labeled arrays, CF conventions |
| **Zarr/NetCDF** | Data storage formats | Cloud-optimized, self-describing |

## 📊 Sample Datasets

The workshop includes real-world scientific data examples:

- **QPSUMS Radar Data**: High-resolution precipitation radar from Taiwan
- **ERA5 Reanalysis**: Global atmospheric reanalysis data
- **Station Data**: Meteorological observations

## 🎓 Learning Outcomes

After completing this workshop, participants will be able to:

1. **Modernize Development Workflows**
   - Replace traditional Python tooling with UV
   - Create reproducible, shareable environments
   - Integrate modern tools with Jupyter

2. **Implement Efficient Data Processing**
   - Design lazy evaluation pipelines with Dask
   - Process datasets larger than available memory
   - Optimize computational graphs for performance

3. **Apply Scientific Best Practices**
   - Create CF-compliant metadata
   - Validate data against international standards
   - Build reproducible scientific workflows

4. **Organize and Share Data**
   - Design effective data catalogs with Intake
   - Implement consistent data access patterns
   - Document datasets with rich metadata

## 🔍 Advanced Topics

For further exploration beyond the workshop:

- **Distributed Computing**: Scale Dask across multiple machines
- **Cloud Integration**: Deploy workflows on cloud platforms
- **Custom Drivers**: Extend Intake for specialized data formats
- **Workflow Automation**: Integrate with CI/CD pipelines

## 🤝 Contributing

This project is designed for educational purposes. Contributions are welcome:

1. **Bug Reports**: Open issues for any problems encountered
2. **Improvements**: Suggest enhancements to workshop content
3. **Additional Examples**: Contribute new datasets or use cases
4. **Documentation**: Help improve explanations and clarity

## 📄 License

This project is available under the MIT License. See individual tool documentation for their respective licenses.

## 🙏 Acknowledgments

- **UV Team**: For revolutionizing Python package management
- **Intake Community**: For building excellent data cataloging tools
- **Dask Developers**: For enabling scalable scientific computing
- **CF Conventions Committee**: For scientific metadata standards

## 📞 Support

For questions or issues:

1. Check the workshop notebooks for detailed explanations
2. Consult the [Issues](https://github.com/Isongzhe/dataset-catalog/issues) page
3. Review official documentation for each tool
4. Open a new issue for project-specific problems

---

**Last Updated:** August 2025  
**Workshop Version:** 1.0  
**Recommended Python:** 3.11+
