from langchain_core.tools import tool


@tool
def get_stock_price(ticker: str) -> str:
    """주식 종목의 현재가를 조회합니다."""
    stock_prices = {
        "삼성전자": 75000,
        "카카오": 52000,
        "네이버": 185000,
        "현대차": 230000,
        "LG에너지솔루션": 410000
    }
    
    if ticker in stock_prices:
        return f"{ticker}의 현재가는 {stock_prices[ticker]:,}원입니다."
    else:
        return f"{ticker} 종목을 찾을 수 없습니다."


@tool
def calculate_profit_loss(buy_price: float, sell_price: float, quantity: int) -> str:
    """매수가, 매도가, 수량을 기반으로 수익/손실을 계산합니다."""
    profit_loss = (sell_price - buy_price) * quantity
    profit_rate = ((sell_price - buy_price) / buy_price) * 100
    
    return f"수익/손실: {profit_loss:,.0f}원 (수익률: {profit_rate:.2f}%)"


@tool
def get_market_trend(ticker: str) -> str:
    """주식 종목의 시장 추세를 조회합니다."""
    market_trends = {
        "삼성전자": "상승 / 최근 3일 연속 상승세, 반도체 업황 개선 기대감",
        "카카오": "하락 / 최근 규제 이슈로 약세 지속",
        "네이버": "횡보 / 뚜렷한 방향성 없이 보합세 유지",
        "현대차": "상승 / 전기차 수출 호조로 강세",
        "LG에너지솔루션": "하락 / 배터리 수요 둔화 우려로 약세"
    }
    
    if ticker in market_trends:
        return f"{ticker} 추세: {market_trends[ticker]}"
    else:
        return f"{ticker} 종목의 추세 정보를 찾을 수 없습니다."


@tool
def recommend_action(ticker: str, trend: str, current_price: float, buy_price: float) -> str:
    """종목의 추세와 수익률을 기반으로 매매 행동을 추천합니다."""
    profit_rate = ((current_price - buy_price) / buy_price) * 100
    
    if "상승" in trend:
        if profit_rate < 10:
            return f"{ticker} 추천: 매수 (상승 추세이며 수익률 {profit_rate:.2f}%로 아직 10% 미만)"
        else:
            return f"{ticker} 추천: 매도 (상승 추세이며 수익률 {profit_rate:.2f}%로 10% 이상 달성)"
    elif "하락" in trend:
        return f"{ticker} 추천: 관망 (하락 추세, 현재 수익률 {profit_rate:.2f}%)"
    else:  # 횡보
        return f"{ticker} 추천: 관망 (횡보 추세, 현재 수익률 {profit_rate:.2f}%)"
