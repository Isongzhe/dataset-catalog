#!/usr/bin/env python3
"""
Multi-catalog Usage Example
=========================

This example shows how to work with multiple data catalogs
organized by data type.

作者: Lab Data Team
日期: 2024-12
"""

import intake

def main():
    print("=== 多重資料目錄使用範例 ===\n")
    
    # Load different catalogs by data type
    print("1. 載入不同類型的資料目錄:")
    era5_cat = intake.open_catalog('era5_intake_catalog.yaml')
    obs_cat = intake.open_catalog('observations_catalog.yaml') 
    sat_cat = intake.open_catalog('satellite_catalog.yaml')
    model_cat = intake.open_catalog('model_catalog.yaml')
    
    print("   ✓ ERA5 再分析資料目錄")
    print("   ✓ 觀測資料目錄") 
    print("   ✓ 衛星資料目錄")
    print("   ✓ 模式資料目錄")
    
    # List available datasets in each catalog
    print("\n2. 檢視各目錄中的資料集:")
    
    print("\n   ERA5 目錄:")
    for name in era5_cat:
        print(f"     - {name}")
    
    print("\n   觀測目錄:")
    for name in obs_cat:
        print(f"     - {name}")
        
    print("\n   衛星目錄:")
    for name in sat_cat:
        print(f"     - {name}")
        
    print("\n   模式目錄:")
    for name in model_cat:
        print(f"     - {name}")
    
    # Example: Load data from different sources
    print("\n3. 載入不同來源的資料:")
    
    try:
        # Load ERA5 data
        print("   載入 ERA5 溫度資料...")
        era5_temp = era5_cat.era5_hourly_single_levels.to_dask()
        print(f"     ERA5 資料形狀: {era5_temp.dims}")
        
        # Load station data  
        print("   載入測站資料...")
        station_entry = obs_cat.station_temperature
        print(f"     測站資料描述: {station_entry.description[:50]}...")
        
        print("   ✓ 成功載入多種資料類型!")
        
    except Exception as e:
        print(f"   ⚠ 資料載入說明 (檔案路徑需要設定): {e}")
    
    # Show how to search across catalogs
    print("\n4. 跨目錄搜尋範例:")
    print("   搜尋包含 '溫度' 的資料集:")
    
    all_catalogs = {
        'ERA5': era5_cat,
        '觀測': obs_cat, 
        '衛星': sat_cat,
        '模式': model_cat
    }
    
    for cat_name, catalog in all_catalogs.items():
        for ds_name in catalog:
            try:
                entry = catalog[ds_name]
                if '溫度' in entry.description:
                    print(f"     - {cat_name}: {ds_name}")
            except Exception:
                # Skip entries that require parameters
                pass
    
    print("\n=== 範例完成 ===")
    print("\n💡 提示:")
    print("   - 依資料類型組織目錄便於管理")
    print("   - 每個目錄可獨立維護和更新")
    print("   - 使用標籤系統便於跨目錄搜尋")
    print("   - 統一的 metadata 格式確保一致性")

if __name__ == "__main__":
    main()
