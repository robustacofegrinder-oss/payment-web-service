import secrets
import string

def generate_key():
    alphabet = string.ascii_uppercase + string.digits
    parts = []

    for _ in range(4):
        parts.append(
            "".join(secrets.choice(alphabet) for _ in range(5))
        )

    return "PY-" + "-".join(parts)

if __name__ == "__main__":
    print("مفتاح عميل جديد:")
    print(generate_key())
