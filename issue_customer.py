from issue_license import generate_key
from license_registry import add_license

def issue_customer(customer=""):
    key = generate_key()
    record = add_license(key, customer)
    return record

if __name__ == "__main__":
    customer = input("اسم أو رمز العميل: ").strip()
    record = issue_customer(customer)

    print("تم إصدار ترخيص جديد.")
    print("المفتاح:", record["key"])
    print("العميل:", record["customer"])
    print("الحالة: فعال")
