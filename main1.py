import re
import random


def normalize(s):
    if not isinstance(s, str):
        s = str(s)
    s = s.lower()
    s = s.replace('ё', 'е')
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def levenshtein(a, b):
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            insert = previous[j] + 1
            delete = current[j - 1] + 1
            replace = previous[j - 1] + (ca != cb)
            current.append(min(insert, delete, replace))
        previous = current
    return previous[-1]


def similarity(a, b):
    if a == b:
        return 1.0
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 1.0
    return 1.0 - levenshtein(a, b) / max_len

def generate_test_data():
    # Эталонный большой список (1000 записей)
    large_list = []
    for i in range(1, 1001):
        value = f"name_{random.randint(1, 500)}_surname_{random.randint(1, 200)}"
        large_list.append({"id": i, "value": value})

    # Малый список (500 записей) с возможными ошибками
    small_list = []
    for i in range(1, 501):
        orig = random.choice(large_list)
        noisy = orig["value"]
        if random.random() < 0.7:
            if random.random() < 0.3:
                noisy = noisy.upper()
            if random.random() < 0.3:
                noisy = noisy.replace(' ', '  ')
            if random.random() < 0.3 and len(noisy) > 2:
                idx = random.randint(0, len(noisy) - 1)
                noisy = noisy[:idx] + noisy[idx + 1:]
            if random.random() < 0.3 and len(noisy) > 1:
                idx = random.randint(0, len(noisy) - 1)
                noisy = noisy[:idx] + random.choice('abcdefghijklmnopqrstuvwxyz') + noisy[idx + 1:]
        small_list.append({"id": i, "value": noisy})

    # Добавим несколько заведомо отсутствующих записей
    for i in range(1, 21):
        small_list.append({"id": 500 + i, "value": f"absent_record_{random.randint(1000, 9999)}"})

    return small_list[:500], large_list

THRESHOLD_SUGGEST = 0.75
TOP_K = 3


def find_matches(small_list, large_list):
    norm_small = [(item["id"], item["value"], normalize(item["value"])) for item in small_list]

    exact_index = {}
    large_norm = []
    large_by_id = {}
    for item in large_list:
        norm_val = normalize(item["value"])
        large_norm.append((item["id"], item["value"], norm_val))
        exact_index[norm_val] = item["id"]
        large_by_id[item["id"]] = item["value"]

    results = []
    for small_id, small_value, small_norm in norm_small:
        if small_norm in exact_index:
            large_id = exact_index[small_norm]
            results.append({
                "small_id": small_id,
                "small_value": small_value,
                "large_id": large_id,
                "large_value": large_by_id[large_id],
                "similarity": 1.0
            })
            continue

        candidates = []
        for large_id, large_value, large_norm_val in large_norm:
            sim = similarity(small_norm, large_norm_val)
            if sim >= THRESHOLD_SUGGEST:
                candidates.append({"large_id": large_id, "large_value": large_value, "sim": sim})

        candidates.sort(key=lambda x: x["sim"], reverse=True)
        top_candidates = candidates[:TOP_K]

        if top_candidates:
            print(f"\nЗапись ID={small_id}: {small_value}")
            print("Возможно, вы имели в виду:")
            for idx, cand in enumerate(top_candidates, 1):
                print(f"  {idx}. ID={cand['large_id']} — {cand['large_value']} (схожесть {cand['sim'] * 100:.1f}%)")
            print("0 - пропустить")

            while True:
                try:
                    choice = int(input("Ваш выбор: "))
                    if 0 <= choice <= len(top_candidates):
                        break
                    else:
                        print(f"Введите число от 0 до {len(top_candidates)}")
                except ValueError:
                    print("Некорректный ввод, повторите.")

            if choice == 0:
                results.append({
                    "small_id": small_id,
                    "small_value": small_value,
                    "large_id": None,
                    "large_value": None,
                    "similarity": top_candidates[0]["sim"] if top_candidates else 0.0
                })
            else:
                chosen = top_candidates[choice - 1]
                results.append({
                    "small_id": small_id,
                    "small_value": small_value,
                    "large_id": chosen["large_id"],
                    "large_value": chosen["large_value"],
                    "similarity": chosen["sim"]
                })
        else:
            print(f"\nЗапись ID={small_id}: {small_value} — подходящих вариантов не найдено")
            results.append({
                "small_id": small_id,
                "small_value": small_value,
                "large_id": None,
                "large_value": None,
                "similarity": 0.0
            })

    return results


if __name__ == "__main__":
    small, large = generate_test_data()
    print(f"Сгенерировано: small_list = {len(small)} записей, large_list = {len(large)} записей")

    results = find_matches(small, large)

    exact = sum(1 for r in results if r["similarity"] == 1.0)
    fuzzy = sum(1 for r in results if r["large_id"] is not None and r["similarity"] < 1.0)
    none = sum(1 for r in results if r["large_id"] is None)

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Точных совпадений: {exact}")
    print(f"Нечётких (выбрано): {fuzzy}")
    print(f"Не найдено: {none}")
    if exact + fuzzy > 0:
        avg_sim = sum(r['similarity'] for r in results if r['large_id'] is not None) / (exact + fuzzy)
        print(f"Средняя схожесть для найденных: {avg_sim:.3f}")
