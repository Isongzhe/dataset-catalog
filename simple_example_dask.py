#!/usr/bin/env python3
"""
簡單的 ERA5 Catalog 使用範例
針對 6TB 資料集的實用載入方式 (使用 Dask)
"""

import intake
import warnings
warnings.filterwarnings('ignore')

def main():
    print("🌍 ERA5 Intake Catalog 實用範例")
    print("=" * 50)
    
    # 1. 載入 catalog
    print("\n📚 載入 catalog...")
    catalog = intake.open_catalog("*_intake_catalog.yaml")
    print(f"✅ 可用資料集: {list(catalog)}")
    
    # 2. 載入一週的資料（使用 Dask 記憶體友好）
    print("\n📊 載入一週的資料 (2020-01-01 到 2020-01-07)...")
    print("💡 使用 to_dask() 進行延遲載入...")
    try:
        ds_week = catalog.era5_hourly_global.to_dask().sel(
            time=slice('2020-01-01', '2020-01-07')
        )
        print(f"✅ 成功設定載入! 資料大小: {ds_week.nbytes / 1e9:.2f} GB")
        print(f"📋 時間範圍: {ds_week.time.values[0]} 到 {ds_week.time.values[-1]}")
        print(f"🌡️  可用變數: {list(ds_week.data_vars)[:5]}... (共 {len(ds_week.data_vars)} 個)")
        
        # 3. 分析地面溫度 (這時會觸發實際載入)
        print("\n🌡️  分析 850 hPa 溫度...")
        temp_850 = ds_week['temperature'].sel(level=850)
        print(f"   平均溫度: {float(temp_850.mean()):.2f} K ({float(temp_850.mean()) - 273.15:.2f} °C)")
        print(f"   最高溫度: {float(temp_850.max()):.2f} K ({float(temp_850.max()) - 273.15:.2f} °C)")
        print(f"   最低溫度: {float(temp_850.min()):.2f} K ({float(temp_850.min()) - 273.15:.2f} °C)")
        
        # 4. 分析風速
        print("\n💨 分析 10 米風速...")
        u_wind = ds_week['10m_u_component_of_wind']
        v_wind = ds_week['10m_v_component_of_wind']
        wind_speed = (u_wind**2 + v_wind**2)**0.5
        
        print(f"   平均風速: {float(wind_speed.mean()):.2f} m/s")
        print(f"   最大風速: {float(wind_speed.max()):.2f} m/s")
        
        # 5. 分析降水
        print("\n🌧️  分析總降水量...")
        precip = ds_week['total_precipitation']
        total_precip = precip.sum(dim='time')
        
        print("   週總降水量統計:")
        print(f"     全球平均: {float(total_precip.mean()):.6f} m")
        print(f"     全球最大: {float(total_precip.max()):.6f} m")
        
    except Exception as e:
        print(f"❌ 載入失敗: {e}")
        return
    
    # 6. 示範區域分析
    print("\n🗺️  區域分析範例 (台灣附近)...")
    try:
        taiwan_region = catalog.era5_hourly_global.to_dask().sel(
            time=slice('2020-01-01', '2020-01-07'),
            latitude=slice(26, 21),   # 台灣緯度
            longitude=slice(118, 123) # 台灣經度
        )
        
        print(f"✅ 台灣區域資料大小: {taiwan_region.nbytes / 1e6:.2f} MB")
        print(f"📏 空間範圍: {len(taiwan_region.latitude)} x {len(taiwan_region.longitude)} 格點")
        
        # 台灣區域平均溫度
        taiwan_temp = taiwan_region['temperature'].sel(level=850).mean()
        print(f"🌡️  台灣區域850 hPa 平均溫度: {float(taiwan_temp) - 273.15:.1f} °C")
        
    except Exception as e:
        print(f"❌ 區域分析失敗: {e}")
    
    print("\n🎉 範例執行完成!")

if __name__ == "__main__":
    main()
