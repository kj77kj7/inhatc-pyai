import csv
from pathlib import Path

import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def load_glucose_values(csv_path: Path) -> list[float]:
    """CSV에서 Glucose 컬럼을 읽어 숫자 리스트로 반환"""
    glucose_values: list[float] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get("Glucose", "").strip()
            if value == "":
                continue
            try:
                glucose_values.append(float(value))
            except ValueError:
                continue

    return glucose_values


def moving_average(values: list[float], window: int = 30) -> list[float]:
    """간단 이동평균 계산"""
    if window <= 1:
        return values[:]

    ma: list[float] = []
    running_sum = 0.0

    for i, v in enumerate(values):
        running_sum += v
        if i >= window:
            running_sum -= values[i - window]

        current_window = min(i + 1, window)
        ma.append(running_sum / current_window)

    return ma


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "diabetes.csv"
    output_path = base_dir / "trend_graph.png"

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {csv_path}")

    glucose = load_glucose_values(csv_path)
    if not glucose:
        raise ValueError("Glucose 컬럼 데이터가 비어 있습니다.")

    trend = moving_average(glucose, window=30)
    x = list(range(1, len(glucose) + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(x, glucose, color="lightgray", linewidth=1.0, label="원본 Glucose")
    plt.plot(x, trend, color="tab:blue", linewidth=2.0, label="30개 이동평균 추이")
    plt.title("Diabetes CSV - Glucose 추이 그래프")
    plt.xlabel("데이터 순번")
    plt.ylabel("Glucose")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)

    print(f"그래프 저장 완료: {output_path}")


if __name__ == "__main__":
    main()
