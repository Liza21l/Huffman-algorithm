
import heapq
from collections import Counter


# Вузол дерева Хаффмана
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Завдання 1. Частотний аналіз символів
def calculate_frequencies(text):
    return Counter(text)


# Побудова дерева Хаффмана
def build_huffman_tree(frequencies):
    if not frequencies:
        return None

    heap = [
        Node(char, freq)
        for char, freq in frequencies.items()
    ]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right

        heapq.heappush(heap, parent)

    return heap[0]


# Створення таблиці кодів
def build_codes(root):
    codes = {}

    def generate_codes(node, code):
        if node is None:
            return

        if node.char is not None:
            codes[node.char] = code if code else "0"
            return

        generate_codes(node.left, code + "0")
        generate_codes(node.right, code + "1")

    generate_codes(root, "")
    return codes


# Завдання 2. Кодування тексту
def encode_text(text, codes):
    return "".join(codes[char] for char in text)


# Декодування тексту
def decode_text(encoded_text, root):
    if root is None:
        return ""

    # Особливий випадок: текст містить лише один вид символу
    if root.char is not None:
        return root.char * len(encoded_text)

    decoded = []
    current = root

    for bit in encoded_text:
        if bit == "0":
            current = current.left
        elif bit == "1":
            current = current.right
        else:
            raise ValueError("Код має містити лише 0 та 1")

        if current.char is not None:
            decoded.append(current.char)
            current = root

    if current != root:
        raise ValueError("Некоректний закодований текст")

    return "".join(decoded)


# Основна програма
def main():
    file_name = "text.txt"

    # Читаємо текстовий файл
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        print("Файл порожній.")
        return

    # Завдання 1
    frequencies = calculate_frequencies(text)
    tree = build_huffman_tree(frequencies)
    codes = build_codes(tree)

    print("Частота символів:")
    for char, freq in sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0])
    ):
        print(f"{repr(char)}: {freq}")

    print("\nКоди Хаффмана:")
    for char, code in sorted(codes.items()):
        print(f"{repr(char)}: {code}")

    # Завдання 2
    encoded_text = encode_text(text, codes)
    decoded_text = decode_text(encoded_text, tree)

    print("\nПочатковий текст:")
    print(text)

    print("\nЗакодований текст:")
    print(encoded_text)

    print("\nДекодований текст:")
    print(decoded_text)

    print("\nПеревірка:", decoded_text == text)

    # Зберігаємо результати у файли
    with open("encoded.txt", "w", encoding="utf-8") as file:
        file.write(encoded_text)

    with open("decoded.txt", "w", encoding="utf-8") as file:
        file.write(decoded_text)


if __name__ == "__main__":
    main()
