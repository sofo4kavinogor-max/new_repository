from main import *

if __name__ == "__main__":
    small_test = [
        {'id': 1, 'value': "Иванов И."},
        {'id': 2, 'value': "Петров А."}
    ]
    large_test = [
        {'id': 101, 'value': "Иванов Иван"},
        {'id': 102, 'value': "Петров Алексей"},
        {'id': 103, 'value': "Сидоров"}
    ]

    results = find_matches(small_test, large_test)

    print("\n" + "=" * 70)
    print("ИТОГОВЫЙ СПИСОК (small_id → large_id, схожесть)")
    print("-" * 70)
    for r in results:
        if r['large_id']:
            print(
                f"{r['small_id']:3} | {r['small_value']:20} -> {r['large_id']:4} | {r['large_value']:25} | {r['similarity']:.2f}")
        else:
            print(f"{r['small_id']:3} | {r['small_value']:20} -> НЕ НАЙДЕНО")
