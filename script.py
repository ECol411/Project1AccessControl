import random
import re

# ---------------------------------------------------------
# 1. INPUT NUMBER OF ATTRIBUTES
# ---------------------------------------------------------
n = int(input("Enter number of total attributes in the system: "))

# ---------------------------------------------------------
# 2. GENERATE n ATTRIBUTE TYPES
# ---------------------------------------------------------
attributes = []
for i in range(n):
    attributes.append(f"Attribute{i+1}")

print("\nGenerated Attributes:")
print(attributes)

# ---------------------------------------------------------
# 3. GENERATE 10 USERS WITH RANDOM ATTRIBUTES
# ---------------------------------------------------------
users = {}

for uid in range(1, 11):
    num_attr = random.randint(2, n)  # each user has at least 2 attributes
    user_attrs = random.sample(attributes, num_attr)
    users[f"User{uid}"] = user_attrs

print("\nGenerated Users and Their Attributes:")
for u, a in users.items():
    print(f"{u}: {a}")

# ---------------------------------------------------------
# Helper: Evaluate AND / OR expressions
# ---------------------------------------------------------
def eval_basic_expression(expr, user_attrs):
    """Evaluate simple expressions like (A AND B) or (A OR B)."""
    tokens = expr.strip().split()

    if "AND" in tokens:
        needed = [t for t in tokens if t.startswith("Attribute")]
        return all(a in user_attrs for a in needed)

    if "OR" in tokens:
        needed = [t for t in tokens if t.startswith("Attribute")]
        return any(a in user_attrs for a in needed)

    return False

# ---------------------------------------------------------
# Helper: Evaluate "k of (A, B, C)"
# ---------------------------------------------------------
def eval_k_of_expression(expr, user_attrs):
    """Evaluate expressions like '2 of (Attribute3, Attribute4, Attribute5)'."""
    match = re.match(r"(\d+)\s+of\s+\((.*?)\)", expr)
    if not match:
        return False

    k = int(match.group(1))
    attrs = [a.strip() for a in match.group(2).split(",")]

    count = sum(1 for a in attrs if a in user_attrs)
    return count >= k

# ---------------------------------------------------------
# 4. INPUT ACCESS CONTROL POLICY
# ---------------------------------------------------------
print("\nEnter an attribute-based access control policy.")
print("Examples:")
print("(Attribute1 AND Attribute2) OR (2 of (Attribute3, Attribute4, Attribute5))")
print("(Attribute1 AND Attribute2) OR (Attribute3 AND Attribute4)")

policy = input("\nEnter policy: ")

# ---------------------------------------------------------
# Parse policy into OR segments
# ---------------------------------------------------------
segments = [seg.strip() for seg in policy.split("OR")]

# ---------------------------------------------------------
# 5. EVALUATION
# ---------------------------------------------------------
print("\nEnter your attributes separated by commas:")
user_input = input("Your attributes: ")

user_attrs = [a.strip() for a in user_input.split(",")]

def evaluate_policy(policy_segments, user_attrs):
    for seg in policy_segments:
        seg = seg.strip()

        # Case 1: (A AND B) or (A OR B)
        if "AND" in seg or "OR" in seg:
            inner = seg.replace("(", "").replace(")", "")
            if eval_basic_expression(inner, user_attrs):
                return True

        # Case 2: k of (...)
        if "of" in seg:
            inner = seg.replace("(", "").replace(")", "")
            if eval_k_of_expression(inner, user_attrs):
                return True

    return False

result = evaluate_policy(segments, user_attrs)

print("\nAccess Evaluation Result:", "TRUE" if result else "FALSE")
