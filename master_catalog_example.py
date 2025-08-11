#!/usr/bin/env python3
"""
Master Catalog Usage Example
==========================

This example shows how to use the master catalog to discover
and access all available data catalogs.

作者: Lab Data Team
日期: 2024-12
"""

import intake
import os

def main():
    print("=== 主目錄使用範例 ===\n")
    
    # Set the catalog directory (can be relative or absolute)
    os.environ['CATALOG_DIR'] = '.'
    
    # Load the master catalog
    print("1. 載入主目錄索引:")
    try:
        master = intake.open_catalog('master_catalog.yaml')
        print("   ✓ 主目錄載入成功")
        
        # Show available catalogs
        print("\n2. 可用的資料目錄:")
        for name in master:
            entry = master[name]
            print(f"   📁 {name}:")
            print(f"      說明: {entry.description.split('包含')[0].strip()}")
            if hasattr(entry, 'metadata') and 'tags' in entry.metadata:
                tags = ', '.join(entry.metadata['tags'][:3])  # Show first 3 tags
                print(f"      標籤: {tags}")
        
        # Access specific catalogs through the master catalog
        print("\n3. 透過主目錄存取子目錄:")
        
        # Access ERA5 catalog
        print("   存取 ERA5 目錄:")
        era5_cat = master.era5_catalog()
        print(f"     可用資料集: {list(era5_cat)}")
        
        # Access observations catalog
        print("   存取觀測目錄:")
        obs_cat = master.observations_catalog()
        print(f"     可用資料集: {list(obs_cat)}")
        
        print("\n4. 搜尋功能示範:")
        print("   依標籤搜尋目錄:")
        
        for name in master:
            entry = master[name]
            if hasattr(entry, 'metadata') and 'tags' in entry.metadata:
                tags = entry.metadata['tags']
                if 'global' in tags:
                    print(f"     🌍 全球資料: {name}")
                elif 'regional' in tags:
                    print(f"     🗺️  區域資料: {name}")
        
        print("\n   依資料類型搜尋:")
        temp_catalogs = []
        for name in master:
            entry = master[name] 
            if hasattr(entry, 'metadata') and 'data_types' in entry.metadata:
                if 'temperature' in entry.metadata['data_types']:
                    temp_catalogs.append(name)
        
        print(f"     🌡️  包含溫度資料的目錄: {', '.join(temp_catalogs)}")
        
    except Exception as e:
        print(f"   ⚠ 載入說明: {e}")
        print("   請確認所有目錄檔案都存在於目前資料夾")
    
    print("\n=== 目錄組織架構說明 ===")
    print("""
📁 dataset-catalog/
├── 🗂️  master_catalog.yaml        # 主索引 (入口點)
├── 🌍 era5_intake_catalog.yaml    # ERA5 再分析資料
├── 📊 observations_catalog.yaml   # 測站觀測資料
├── 🛰️  satellite_catalog.yaml     # 衛星資料
├── 🔮 model_catalog.yaml          # 數值模式資料
└── 📝 *.py                        # 使用範例

優點:
✓ 依資料類型清楚分類
✓ 每個目錄可獨立維護
✓ 主索引提供統一入口
✓ 支援標籤和元資料搜尋
✓ 容易擴展新的資料類型
    """)
    
    print("\n💡 實際使用建議:")
    print("   1. 新使用者從 master_catalog.yaml 開始")
    print("   2. 依需求載入特定類型的目錄")
    print("   3. 使用標籤系統快速找到相關資料")
    print("   4. 新增資料時更新對應的專門目錄")

if __name__ == "__main__":
    main()
