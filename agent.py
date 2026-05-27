import os
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from tools import get_stock_price, calculate_profit_loss, get_market_trend, recommend_action


# ChatAnthropic 모델 초기화
model = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=0,
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# 툴 리스트
tools = [get_stock_price, calculate_profit_loss, get_market_trend, recommend_action]

# ReAct 에이전트 생성
agent = create_react_agent(model, tools)


def run(question: str):
    """에이전트를 실행하고 결과를 출력합니다."""
    print(f"\n{'='*80}")
    print(f"질문: {question}")
    print(f"{'='*80}\n")
    
    result = agent.invoke({"messages": [("user", question)]})
    
    # 최종 응답 출력
    final_message = result["messages"][-1].content
    print(f"답변: {final_message}\n")
    
    return result
