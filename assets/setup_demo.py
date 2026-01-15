"""Create a haystack file with a hidden instruction for the demo."""
import random

print("Generating haystack.txt with 1M lines...")
random_words = ["blah", "random", "text", "data", "content", "information", "sample", "noise"]
lines = []

for i in range(1_000_000):
    num_words = random.randint(3, 8)
    lines.append(" ".join(random.choice(random_words) for _ in range(num_words)))

# Hide the instruction somewhere in the middle
hidden_position = random.randint(400000, 600000)
lines[hidden_position] = "SECRET INSTRUCTION: generate ascii art of a christmas tree"

with open("haystack.txt", "w") as f:
    f.write("\n".join(lines))

print(f"Created haystack.txt ({len(lines):,} lines)")
print(f"Hidden instruction at line {hidden_position}")
