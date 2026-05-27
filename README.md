# 주식 트레이더 AI 에이전트

LangChain과 LangGraph를 활용한 주식 매매 의사결정 지원 AI 에이전트입니다.

## 프로젝트 설명

이 프로젝트는 Claude AI 모델을 기반으로 한 ReAct 에이전트로, 주식 시장 정보를 조회하고 매매 의사결정을 지원합니다. 사용자의 질문에 따라 적절한 툴을 선택하여 실행하고, 종합적인 분석 결과를 제공합니다.

## 주요 기능 (툴 목록)

### 1. get_stock_price
- **기능**: 주식 종목의 현재가를 조회합니다.
- **지원 종목**: 삼성전자, 카카오, 네이버, 현대차, LG에너지솔루션
- **입력**: ticker (종목명)
- **출력**: 해당 종목의 현재가

### 2. calculate_profit_loss
- **기능**: 매수가, 매도가, 수량을 기반으로 수익/손실을 계산합니다.
- **입력**: buy_price (매수가), sell_price (매도가), quantity (수량)
- **출력**: 수익/손실 금액 및 수익률(%)

### 3. get_market_trend
- **기능**: 주식 종목의 시장 추세를 조회합니다.
- **입력**: ticker (종목명)
- **출력**: 해당 종목의 추세 정보 (상승/하락/횡보 및 상세 설명)

### 4. recommend_action
- **기능**: 종목의 추세와 수익률을 기반으로 매매 행동을 추천합니다.
- **입력**: ticker (종목명), trend (추세), current_price (현재가), buy_price (매수가)
- **출력**: 매수/매도/관망 추천
- **추천 로직**:
  - 상승 추세 + 수익률 10% 미만 → 매수 추천
  - 상승 추세 + 수익률 10% 이상 → 매도 추천
  - 하락 추세 → 관망 추천
  - 횡보 추세 → 관망 추천

## 설치 방법

1. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## 실행 방법

1. ANTHROPIC_API_KEY 환경변수를 설정합니다:

**Windows (CMD):**
```cmd
set ANTHROPIC_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

2. 프로그램을 실행합니다:
```bash
python main.py
```

## 프로젝트 구조

```
stock_trader_agent/
├── tools.py          # 4개의 주식 관련 툴 정의
├── agent.py          # ReAct 에이전트 생성 및 실행 로직
├── main.py           # 메인 실행 파일 (예제 질문 포함)
├── requirements.txt  # 필요한 패키지 목록
└── README.md         # 프로젝트 설명서
```

## 예제 질문

프로그램은 다음과 같은 질문들을 처리할 수 있습니다:

1. "삼성전자 지금 사도 될까? 현재가 확인하고 추세도 봐줘. 내 매수가는 70000원이야"
2. "카카오를 65000원에 100주 샀는데 지금 팔면 얼마 남아?"
3. "네이버 현재가랑 추세 확인하고 180000원에 50주 보유 중인데 매도할지 말지 추천해줘"

## 주의사항

- 이 프로젝트는 Mock 데이터를 사용하며, 실제 주식 시장 데이터를 제공하지 않습니다.
- 실제 투자 결정에 사용하지 마시고, 학습 및 데모 목적으로만 사용하세요.
- ANTHROPIC_API_KEY는 코드에 하드코딩하지 않으며, 환경변수로 관리합니다.
