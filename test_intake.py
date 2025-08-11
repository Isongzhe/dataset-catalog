"""
Pytest 測試套件 - Intake 環境測試
================================
"""

import pytest
import os

def test_basic_imports():
    """測試基本套件匯入"""
    import intake  # noqa: F401
    import xarray  # noqa: F401
    import dask  # noqa: F401
    import zarr  # noqa: F401
    import numpy  # noqa: F401
    import matplotlib  # noqa: F401
    import pandas  # noqa: F401

def test_intake_functionality():
    """測試 intake 基本功能"""
    import intake
    
    # 建立一個簡單的測試 catalog
    test_catalog_content = """
sources:
  test_data:
    driver: csv
    args:
      urlpath: "{{ CATALOG_DIR }}/test_data.csv"
    description: "Test dataset"
"""
    
    # 寫入測試檔案
    with open("test_catalog.yaml", "w") as f:
        f.write(test_catalog_content)
    
    # 建立測試 CSV 資料
    import pandas as pd
    test_df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    test_df.to_csv("test_data.csv", index=False)
    
    try:
        # 測試載入 catalog
        catalog = intake.open_catalog("test_catalog.yaml")
        assert "test_data" in catalog
        
        # 測試載入資料
        data = catalog.test_data.read()
        assert len(data) == 3
        
    finally:
        # 清理測試檔案
        for f in ["test_catalog.yaml", "test_data.csv"]:
            if os.path.exists(f):
                os.remove(f)

def test_xarray_dask_integration():
    """測試 xarray 和 dask 整合"""
    import xarray as xr
    import dask.array as da
    
    # 建立測試資料
    data = da.ones((10, 20), chunks=(5, 10))
    coords = {"x": range(10), "y": range(20)}
    ds = xr.Dataset({"temperature": (["x", "y"], data)}, coords=coords)
    
    # 測試基本操作
    mean_temp = ds.temperature.mean()
    assert mean_temp.compute() == 1.0

@pytest.mark.skipif(
    not os.path.exists("dataset_intake.yaml"),
    reason="No dataset_intake.yaml found"
)
def test_era5_catalog_loading():
    """測試 ERA5 catalog 載入 (如果存在的話)"""
    import intake
    
    catalog = intake.open_catalog("dataset_intake.yaml")
    assert "era5_hourly_global" in catalog
    
    # 測試取得資料源 (不實際載入)
    source = catalog.era5_hourly_global
    assert source is not None
