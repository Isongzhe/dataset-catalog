#!/usr/bin/env python3
"""
ERA5 Intake Catalog 使用範例
===========================

這個腳本展示如何有效使用 ERA5 intake catalog 進行各種分析任務。
針對 6TB 大小的資料集，記憶體效率和計算策略非常重要。
"""

import intake
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# 1. 基本資料載入 - 從 Catalog 開始
# ==============================================================================

def load_catalog():
    """載入 intake catalog"""
    print("📚 載入 ERA5 Intake Catalog...")
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    # 顯示可用的資料集
    print(f"可用資料集: {list(catalog)}")
    
    # 檢視資料集基本資訊
    print("資料集名稱: era5_hourly_global")
    print("資料集類型: Zarr")
    print("💡 使用 to_dask() 進行延遲載入以獲得最佳效能")
    
    return catalog

# ==============================================================================
# 2. 記憶體效率的資料載入策略
# ==============================================================================

def efficient_data_loading():
    """展示記憶體效率的資料載入方式"""
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    print("\n🚀 記憶體效率載入策略:")
    
    # 策略 1: 時間切片載入 (推薦用於分析)
    print("\n1️⃣ 時間切片載入 - 載入一個月的資料")
    ds_month = catalog.era5_hourly_global.to_dask().sel(
        time=slice('2020-01-01', '2020-01-31')
    )
    print(f"一個月資料大小: {ds_month.nbytes / 1e9:.2f} GB")
    
    # 策略 2: 空間切片載入 (區域分析)
    print("\n2️⃣ 空間切片載入 - 載入台灣周邊區域")
    ds_taiwan = catalog.era5_hourly_global.to_dask().sel(
        time=slice('2020-06-01', '2020-08-31'),  # 夏季
        latitude=slice(25, 20),   # 台灣緯度範圍
        longitude=slice(118, 123)  # 台灣經度範圍
    )
    print(f"台灣區域夏季資料大小: {ds_taiwan.nbytes / 1e6:.2f} MB")
    
    # 策略 3: 變數選擇載入
    print("\n3️⃣ 變數選擇載入 - 只載入溫度和風場")
    ds_selected = catalog.era5_hourly_global.to_dask()[
        ['temperature', '10m_u_component_of_wind', '10m_v_component_of_wind']
    ].sel(time=slice('2020-01-01', '2020-01-07'))
    print(f"選定變數一週資料大小: {ds_selected.nbytes / 1e6:.2f} MB")
    
    return ds_month, ds_taiwan, ds_selected

# ==============================================================================
# 3. 實際分析應用案例
# ==============================================================================

def climate_analysis_examples():
    """氣候分析應用範例"""
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    print("\n🌍 氣候分析應用範例:")
    
    # 範例 1: 計算月平均溫度
    print("\n📊 範例 1: 計算 2020 年各月平均溫度")
    
    # 逐月載入以節省記憶體
    monthly_temps = []
    for month in range(1, 13):
        start_date = f'2020-{month:02d}-01'
        if month == 12:
            end_date = '2020-12-31'
        else:
            end_date = f'2020-{month+1:02d}-01'
        
        # 載入該月資料
        ds_month = catalog.era5_hourly_global.to_dask().sel(
            time=slice(start_date, end_date)
        )
        
        # 計算月平均 (850 hPa 溫度)
        temp_850 = ds_month['temperature'].sel(level=850)
        monthly_mean = temp_850.mean(dim='time')
        monthly_temps.append(monthly_mean)
        
        print(f"  {month:2d}月 全球平均溫度: {float(monthly_mean.mean()):.2f} K")
    
    return monthly_temps

def extreme_weather_analysis():
    """極端天氣事件分析"""
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    print("\n⛈️  極端天氣事件分析:")
    
    # 載入颱風季節資料 (7-9月)
    print("\n🌀 分析 2020 年颱風季節的 CAPE 值")
    ds_typhoon = catalog.era5_hourly_global.to_dask().sel(
        time=slice('2020-07-01', '2020-09-30'),
        latitude=slice(30, 10),    # 西北太平洋區域
        longitude=slice(120, 150)
    )
    
    # 分析對流可用位能 (CAPE)
    cape = ds_typhoon['convective_available_potential_energy']
    
    # 找出高 CAPE 事件 (>2000 J/kg)
    high_cape_events = cape.where(cape > 2000)
    
    print(f"高 CAPE 事件發生次數: {high_cape_events.count().values}")
    print(f"最大 CAPE 值: {float(cape.max())} J/kg")
    print(f"平均 CAPE 值: {float(cape.mean())} J/kg")
    
    return cape

# ==============================================================================
# 4. 機器學習應用的資料準備
# ==============================================================================

def ml_data_preparation():
    """為機器學習準備資料"""
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    print("\n🤖 機器學習資料準備:")
    
    # 準備訓練資料 (2017-2022)
    print("\n📚 準備訓練資料集 (2017-2022)")
    
    # 定義感興趣的變數
    ml_variables = [
        'temperature',
        'specific_humidity', 
        '10m_u_component_of_wind',
        '10m_v_component_of_wind',
        'surface_pressure',
        'total_precipitation'
    ]
    
    # 載入訓練資料 (僅載入部分時間以示範)
    train_data = catalog.era5_hourly_global.to_dask()[ml_variables].sel(
        time=slice('2020-01-01', '2020-01-31'),  # 示範用一個月
        level=850  # 只取 850 hPa 層
    )
    
    print(f"訓練資料形狀:")
    for var in ml_variables:
        if var in train_data:
            shape = train_data[var].shape
            print(f"  {var}: {shape}")
    
    # 資料正規化範例
    print("\n📊 資料正規化統計:")
    for var in ml_variables:
        if var in train_data and train_data[var].dims:
            mean_val = float(train_data[var].mean())
            std_val = float(train_data[var].std())
            print(f"  {var}: mean={mean_val:.3f}, std={std_val:.3f}")
    
    return train_data

# ==============================================================================
# 5. 進階分析技巧
# ==============================================================================

def advanced_analysis_techniques():
    """進階分析技巧"""
    catalog = intake.open_catalog("dataset_intake.yaml")
    
    print("\n🔬 進階分析技巧:")
    
    # 技巧 1: 使用 Dask 進行並行計算
    print("\n⚡ 技巧 1: Dask 並行計算")
    
    # 載入資料但不立即計算 (lazy loading)
    ds = catalog.era5_hourly_global.to_dask().sel(
        time=slice('2020-06-01', '2020-06-30')
    )
    
    # 計算溫度的時間標準差 (使用 Dask)
    temp_std = ds['temperature'].std(dim='time')
    print(f"溫度標準差計算設定完成，尚未執行")
    print(f"計算圖大小: {temp_std.nbytes / 1e6:.2f} MB")
    
    # 技巧 2: 分塊處理大量資料
    print("\n📦 技巧 2: 分塊處理")
    
    # 按時間分塊處理一年的資料
    def process_monthly_chunks(year=2020):
        results = []
        for month in range(1, 13):
            start_date = f'{year}-{month:02d}-01'
            if month == 12:
                end_date = f'{year}-12-31'
            else:
                next_month = month + 1
                end_date = f'{year}-{next_month:02d}-01'
            
            # 處理該月資料
            chunk = catalog.era5_hourly_global.to_dask().sel(
                time=slice(start_date, end_date)
            )
            
            # 執行某種計算 (例如：平均值)
            monthly_result = chunk['surface_pressure'].mean()
            results.append(float(monthly_result))
            
            print(f"  處理完成: {year}-{month:02d}")
        
        return results
    
    # 執行分塊處理 (示範前3個月)
    print("執行分塊處理 (示範前3個月):")
    monthly_results = []
    for month in [1, 2, 3]:
        start_date = f'2020-{month:02d}-01'
        end_date = f'2020-{month+1:02d}-01'
        
        chunk = catalog.era5_hourly_global.to_dask().sel(
            time=slice(start_date, end_date)
        )
        result = float(chunk['surface_pressure'].mean())
        monthly_results.append(result)
        print(f"  2020-{month:02d} 平均地面氣壓: {result:.2f} Pa")
    
    return monthly_results

# ==============================================================================
# 6. 效能優化建議
# ==============================================================================

def performance_optimization_tips():
    """效能優化建議"""
    print("\n⚡ 效能優化建議:")
    print("""
    1. 🕐 時間切片優先
       - 避免載入完整 8 年資料
       - 使用 ds.sel(time=slice('start', 'end'))
       
    2. 🗺️  空間切片
       - 針對研究區域載入資料
       - 使用 ds.sel(latitude=slice(max, min), longitude=slice(min, max))
       
    3. 📊 變數選擇
       - 只載入需要的變數: ds[['var1', 'var2']]
       - 避免載入不必要的壓力層
       
    4. 💾 記憶體管理
       - 使用 ds.chunk() 重新分塊
       - 設定適當的 Dask worker 記憶體限制
       
    5. 🔄 批次處理
       - 對大量資料使用時間分塊處理
       - 避免一次性載入超過系統記憶體的資料
       
    6. 💿 儲存中間結果
       - 將處理後的資料存為 NetCDF 或 Zarr
       - 使用 ds.to_netcdf() 或 ds.to_zarr()
    """)

# ==============================================================================
# 主程式 - 執行所有範例
# ==============================================================================

def main():
    """主程式 - 執行所有使用範例"""
    print("=" * 60)
    print("ERA5 Intake Catalog 使用指南")
    print("=" * 60)
    
    try:
        # 1. 載入 catalog
        catalog = load_catalog()
        
        # 2. 記憶體效率載入
        month_data, taiwan_data, selected_data = efficient_data_loading()
        
        # 3. 氣候分析範例
        monthly_temps = climate_analysis_examples()
        
        # 4. 極端天氣分析
        cape_data = extreme_weather_analysis()
        
        # 5. 機器學習資料準備
        ml_data = ml_data_preparation()
        
        # 6. 進階分析技巧
        advanced_results = advanced_analysis_techniques()
        
        # 7. 效能優化建議
        performance_optimization_tips()
        
        print("\n✅ 所有範例執行完成!")
        print(f"💡 總共展示了 {len(['catalog', 'loading', 'climate', 'extreme', 'ml', 'advanced'])} 種使用方式")
        
    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")
        print("💡 請確認:")
        print("   - dataset_intake.yaml 檔案存在")
        print("   - 網路連線正常")
        print("   - NAS 路徑可以存取")

if __name__ == "__main__":
    main()
