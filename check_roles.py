import os
import re

# ==============================
# CONFIGURASI — EDIT JIKA PERLU
# ==============================
PROJECT_DIR = "foodsystem"  # folder project kamu
ALLOWED_DECORATORS = [
    "role_required",
    "roles_required",
    "customer_required",
    "restaurant_required",
    "driver_required",
    "admin_required",
    "login_required",
]

# ==============================
# FUNGSI CEK FILE
# ==============================

def scan_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    functions = re.findall(r"^def ([a-zA-Z_0-9]+)\(", content, re.MULTILINE)
    decorated = re.findall(r"@([a-zA-Z_0-9]+)", content)

    unprotected = []

    # Cek setiap function, apakah ada decorator proteksi?
    for func in functions:
        # Cari decorator yang tepat sebelum fungsi
        match = re.search(
            r"(@[a-zA-Z_0-9]+[\s]*)+def " + func + r"\(",
            content,
            re.MULTILINE
        )

        if match:
            block = match.group(0)
            found_deco = [
                d for d in ALLOWED_DECORATORS if f"@{d}" in block
            ]
            if not found_deco:
                unprotected.append(func)
        else:
            unprotected.append(func)

    return unprotected


# ==============================
# SCAN SEMUA APP
# ==============================

def scan_project():
    print("🔍 Memeriksa semua view.py…\n")

    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file == "views.py":
                full_path = os.path.join(root, file)
                print(f"📌 Mengecek: {full_path}")

                unprotected = scan_file(full_path)

                if not unprotected:
                    print("   ✔ Semua view terlindungi.\n")
                else:
                    print("   ⚠ View berikut TIDAK punya role-check:")
                    for fn in unprotected:
                        print("     -", fn)
                    print()

scan_project()
