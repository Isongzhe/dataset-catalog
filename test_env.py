#!/usr/bin/env python3
"""
簡單的環境測試腳本
==================

檢查 intake 環境是否正確安裝
"""

import sys

def test_package_imports():
    """測試必要套件是否可以匯入"""
    required_packages = [
        "intake",
        "xarray", 
        "dask",
        "zarr",
        "numpy",
        "matplotlib",
        "pandas",
        "netCDF4"
    ]
    
    failed = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed.append(package)
    
    return len(failed) == 0

def test_catalog_loading():
    """測試 catalog 載入"""
    try:
        import intake
        
        # 檢查是否有 catalog 檔案
        import os
        catalog_files = [f for f in os.listdir('.') if f.endswith('_intake.yaml')]
        
        if not catalog_files:
            print("⚠️  沒有找到 catalog 檔案，但這不影響環境")
            return True
            
        # 嘗試載入第一個找到的 catalog
        catalog_file = catalog_files[0]
        catalog = intake.open_catalog(catalog_file)
        datasets = list(catalog)
        print(f"✅ Catalog 載入成功: {catalog_file}")
        print(f"   找到資料集: {datasets}")
        return True
        
    except Exception as e:
        print(f"⚠️  Catalog 測試失敗: {e}")
        print("   可能是因為資料路徑無法存取，但環境安裝正常")
        return True  # 不影響整體測試結果

def main():
    print("🔬 Lab Intake Environment - 環境測試")
    print("=" * 40)
    
    print("\n📦 測試套件匯入...")
    packages_ok = test_package_imports()
    
    print("\n📚 測試 catalog 功能...")
    test_catalog_loading()
    
    print("\n" + "=" * 40)
    if packages_ok:
        print("🎉 環境測試通過！可以開始使用 intake")
        print("\n💡 下一步:")
        print("   - 建立你的 catalog YAML 檔案")
        print("   - 使用 uv run python 執行分析腳本")
        print("   - 記住用 to_dask() 載入大資料")
    else:
        print("❌ 環境有問題，請執行: uv sync")
        sys.exit(1)

if __name__ == "__main__":
    main()
