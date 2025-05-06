# task_2.py

import csv
import timeit
from pathlib import Path


try:
    from BTrees.OOBTree import OOBTree
except ImportError:
    print("Warning: BTrees module not found. Falling back to dict for tree structure.")
    print("Please run 'pip install BTrees'")
    OOBTree = dict


def load_items(file_path):
    items = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Price'] = float(row['Price'])
            items.append(row)
    return items


def add_item_to_tree(tree, item):
    price = item['Price']
    if price not in tree:
        tree[price] = []
    tree[price].append(item)


def add_item_to_dict(dct, item):
    dct[item['ID']] = item


def range_query_tree(tree, min_price, max_price):
    result = []
    if hasattr(tree, 'items') and callable(tree.items):
        try:
            iterable = tree.items(min_price, max_price)
        except TypeError:
            iterable = tree.items()
    else:
        iterable = tree.items()
    for price, items in iterable:
        if min_price <= price <= max_price:
            result.extend(items)
    return result


def range_query_dict(dct, min_price, max_price):
    result = []
    for item in dct.values():
        price = item['Price']
        if min_price <= price <= max_price:
            result.append(item)
    return result


def main():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir.parent / 'data' / 'generated_items_data.csv'
    # 1. Load data
    items = load_items(csv_path)

    # 2. Initialize structures
    tree = OOBTree()
    dct = {}

    # 3. Populate structures
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dct, item)

    # 4. Define query range
    min_price, max_price = 10.0, 100.0

    # 5. Wrapper functions for timeit
    def query_tree():
        range_query_tree(tree, min_price, max_price)

    def query_dict():
        range_query_dict(dct, min_price, max_price)

    # 6. Measure execution time for 100 repeats
    reps = 100
    t_tree = timeit.timeit(query_tree, number=reps)
    t_dict = timeit.timeit(query_dict, number=reps)

    # 7. Print the results
    print(f"Total range_query time for OOBTree: {t_tree:.6f} seconds")
    print(f"Total range_query time for Dict:    {t_dict:.6f} seconds")

    # calculate many time OOBTree is faster than dict
    print(
        f"OOBTree is {t_dict / t_tree:.2f} times faster than Dict for range_query.")


if __name__ == '__main__':
    main()
