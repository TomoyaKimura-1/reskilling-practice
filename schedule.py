
import json
import sys
from pathlib import Path
from datetime import date, datetime, time, timedelta, timezone


# ① schedule.json を読み込む関数
def load_schedule():
    file_path = Path(__file__).parent / "schedule.json"

    if not file_path.exists():
        raise FileNotFoundError("schedule.json が見つかりません。同じフォルダに配置してください。")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ② 指定した日付の予定だけに絞り、時刻順に並べる関数
def filter_schedule(schedule, target_date):
    result = []

    for item in schedule:
        start = datetime.fromisoformat(item["start"])

        if start.date() == target_date:
            result.append(item)

    return sorted(result, key=lambda item: item["start"])


# ③ 予定1件を表示用の文字列にする関数
def format_schedule(item):
    start = datetime.fromisoformat(item["start"])
    end = datetime.fromisoformat(item["end"])

    location = item.get("location") or "（場所なし）"

    return (
        f"{start:%H:%M}-{end:%H:%M}  "
        f"{item['title']}  "
        f"@{location}"
    )


# メイン処理
def main():
    try:
        # 日付の指定がなければ日本時間の今日を使う
        if len(sys.argv) >= 2:
            target_date = date.fromisoformat(sys.argv[1])
        else:
            jst = timezone(timedelta(hours=9))
            target_date = datetime.now(jst).date()

        # 予定を読み込む
        schedule = load_schedule()

        # 指定日の予定に絞る
        daily_schedule = filter_schedule(schedule, target_date)

        # 結果を表示する
        print(f"{target_date} の予定 {len(daily_schedule)} 件")

        for item in daily_schedule:
            print(format_schedule(item))

    except FileNotFoundError as e:
        print(f"エラー：{e}")

    except ValueError:
        print("エラー：日付は YYYY-MM-DD の形式で指定してください。")

    except json.JSONDecodeError:
        print("エラー：schedule.json のJSON形式が正しくありません。")


if __name__ == "__main__":
    main()
