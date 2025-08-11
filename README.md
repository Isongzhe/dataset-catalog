# Dataset Catalog - 實驗室資料目錄系統

Professional multi-catalog data management system for atmospheric science research.

## Quick Start - 快速開始

Clone and setup:
```bash
git clone <this-repo>
cd dataset-catalog
bash setup.sh
```

That's it! The script will:
- ✅ Install uv package manager
- ✅ Install all dependencies (intake, xarray, dask, etc.)
- ✅ Run tests to verify everything works

## Catalog Organization - 目錄組織架構

Our catalogs are organized by **data type** for maximum clarity and maintainability:

```
📁 dataset-catalog/
├── 🗂️  master_catalog.yaml        # Main entry point - 主入口
├── 🌍 era5_intake_catalog.yaml    # ERA5 reanalysis data
├── 📊 observations_catalog.yaml   # Station & radiosonde data  
├── 🛰️  satellite_catalog.yaml     # Satellite products
├── 🔮 model_catalog.yaml          # Numerical model output
└── 📝 *_example.py                # Usage examples
```

### Why organize by data type?
- ✅ **Clear separation** - Each domain expert manages their data type
- ✅ **Independent updates** - Update catalogs without affecting others  
- ✅ **Easy discovery** - Users know exactly where to find data
- ✅ **Scalable** - Add new data types without reorganizing existing catalogs

## Usage Examples - 使用範例

### 1. Using Master Catalog (Recommended)
```python
import intake
import os

# Set catalog directory
os.environ['CATALOG_DIR'] = '.'

# Load master catalog (entry point)
master = intake.open_catalog('master_catalog.yaml')

# Access specific data types
era5_cat = master.era5_catalog()
obs_cat = master.observations_catalog()

# Use the data
era5_temp = era5_cat.era5_hourly_single_levels.to_dask()
```

### 2. Direct Catalog Access
```python
# Load specific catalogs directly
era5_cat = intake.open_catalog('era5_intake_catalog.yaml')
obs_cat = intake.open_catalog('observations_catalog.yaml')

# Access data
era5_data = era5_cat.era5_hourly_single_levels.to_dask()
```

### 3. Cross-catalog Search
```python
# Search across all catalogs by tags
for cat_name, catalog in all_catalogs.items():
    for ds_name in catalog:
        entry = catalog[ds_name]
        if 'temperature' in entry.metadata.get('tags', []):
            print(f"{cat_name}: {ds_name}")
```

## Run Examples - 執行範例

```bash
python multi_catalog_example.py      # Multi-catalog usage
python master_catalog_example.py     # Master catalog demo
python usage_examples.py            # ERA5 specific examples
```

## Testing - 測試

Run tests anytime:
```bash
python test_env.py      # Simple environment check
python -m pytest        # Full test suite
```

## Adding New Data - 新增資料

1. **Choose appropriate catalog** by data type
2. **Add new source** following existing patterns
3. **Include rich metadata** with tags and descriptions
4. **Update master catalog** if adding new data type
5. **Test your additions** with pytest

## Lab Deployment - 實驗室部署

Perfect for lab GitHub repositories:
- ✅ One-click installation for new lab members
- ✅ Consistent environment across all users  
- ✅ Professional catalog organization
- ✅ Easy maintenance and updates

---
*Designed for atmospheric science research labs* 🌤️
