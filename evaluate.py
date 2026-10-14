import json
from pathlib import Path

from main import classify_category

DATA_FILE = Path(__file__).parent / "data" / "tickets.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    tickets = json.load(file)

test_ids = {
    "D003", "D006", "D009",
    "D013", "D016", "D019",
    "D022", "D025",
    "D029", "D030"
}

test_set = [
    ticket for ticket in tickets
    if ticket["ticket_id"] in test_ids
]

training_set = [
    ticket for ticket in tickets
    if ticket["ticket_id"] not in test_ids
]

correct = 0

print("Held-out test results")
print("-" * 40)

for ticket in test_set:
    predicted = classify_category(ticket["message"])
    actual = ticket["category"]

    if predicted == actual:
        correct += 1

    print(
        f'{ticket["ticket_id"]}: '
        f'Expected={actual}, Predicted={predicted}'
    )

accuracy = correct / len(test_set) * 100

print("-" * 40)
print(f"Reference examples: {len(training_set)}")
print(f"Test examples: {len(test_set)}")
print(f"Correct predictions: {correct}/{len(test_set)}")
print(f"Test accuracy: {accuracy:.2f}%")