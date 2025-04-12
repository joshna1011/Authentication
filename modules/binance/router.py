from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import RedirectResponse
from ..user.utils.response import success_response, failure_response
from .binance_util import Binance
from datetime import datetime

router = APIRouter()

def get_binance():
    return Binance()

@router.get("/coins")
async def get_all_coin_details(binance: Binance = Depends(get_binance)):
    try:
        coins_data = await binance.get_all_coins()
        return success_response(coins_data, "Coins data fetched successfully")
    except Exception as e:
        return failure_response(message=f"Error fetching coins data: {str(e)}")

@router.get("/coin/{symbol}")
async def get_coin_status(symbol: str, binance: Binance = Depends(get_binance)):
    try:
        coin_data = await binance.get_coin_detail(symbol)
        percent_change = float(coin_data["priceChangePercent"])
        trend = "up" if percent_change > 0 else "down" if percent_change < 0 else "neutral"
        coin_data["trend"] = trend
        return success_response(coin_data, "Coin data fetched successfully")
    except Exception as e:
        return failure_response(message=f"Error fetching coin data: {str(e)}")

@router.get("/coin/{symbol}/graph")
async def get_coin_graph_data(
    symbol: str,
    interval: str = Query(default="1h", enum=["1m", "5m", "15m", "1h", "4h", "1d"]),
    limit: int = Query(default=24, ge=1, le=1000),
    binance: Binance = Depends(get_binance)
):
    try:
        # Use the Binance utility method instead of direct API call
        kline_data = await binance.get_coin_graph_data(symbol, interval, limit)

        # Format for graph
        result = []
        for kline in kline_data:
            result.append({
                "time": datetime.utcfromtimestamp(kline[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            })

        return success_response(result, "Graph data fetched successfully")
    except Exception as e:
        return failure_response(message=f"Error fetching graph data: {str(e)}")