#!/bin/bash
# =============================================================================
# Lab Intake Environment - 一鍵安裝腳本
# =============================================================================
# 這個腳本會安裝 uv 和所有 intake 相關的依賴
# 使用方式: bash setup.sh
# =============================================================================

set -e  # 遇到錯誤就停止

echo "🔬 Lab Intake Environment - 一鍵安裝"
echo "===================================="

# 檢查是否在正確的目錄
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 錯誤: 找不到 pyproject.toml!"
    echo "   請在正確的目錄執行此腳本"
    exit 1
fi

# 檢查指令是否存在的函數
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. 安裝 uv (如果還沒有)
echo "📦 檢查 uv 安裝狀態..."
if command_exists uv; then
    echo "✅ uv 已安裝: $(uv --version)"
else
    echo "⬇️  正在安裝 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # 把 uv 加到當前 session 的 PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command_exists uv; then
        echo "✅ uv 安裝成功: $(uv --version)"
    else
        echo "❌ uv 安裝失敗，請手動安裝:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

# 2. 安裝所有依賴
echo "🔧 安裝 intake 環境..."
uv sync

# 3. 測試安裝
echo "🧪 測試安裝結果..."

# 測試基本套件
echo "  - 測試核心套件..."
uv run python -c "
import intake, xarray, dask, zarr, numpy, matplotlib
print('✅ 所有核心套件都可以正常匯入')
"

# 測試 catalog 載入 (如果有的話)
if [ -f "dataset_intake.yaml" ]; then
    echo "  - 測試 catalog 載入..."
    uv run python -c "
import intake
try:
    catalog = intake.open_catalog('dataset_intake.yaml')
    datasets = list(catalog)
    print(f'✅ Catalog 載入成功，找到 {len(datasets)} 個資料集: {datasets}')
except Exception as e:
    print(f'⚠️  Catalog 測試失敗: {e}')
    print('   這可能是因為資料路徑無法存取，但不影響環境安裝')
"
else
    echo "  - 沒有找到 catalog 檔案，跳過測試"
fi

echo ""
echo "🎉 安裝完成！"
echo ""
echo "📋 使用方式:"
echo "  # 啟動 Python 環境"
echo "  uv run python"
echo ""
echo "  # 或是執行 Python 腳本"
echo "  uv run python your_script.py"
echo ""
echo "  # 在 Python 中使用 intake"
echo "  import intake"
echo "  catalog = intake.open_catalog('your_catalog.yaml')"
echo "  ds = catalog.your_dataset.to_dask()"
echo ""
echo "💡 提醒:"
echo "  - 使用 to_dask() 而不是 read() 來載入大資料"
echo "  - 可以隨時添加新的 catalog YAML 檔案"
echo "  - 所有常用的分析套件都已安裝 (xarray, dask, matplotlib 等)"
echo ""
echo "🔧 如需重新安裝: uv sync"
