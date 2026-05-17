import random

# Kamus data vendor dan prefix
VENDOR_PREFIXES = {
    "Google"  : ["3C:5A:B4", "D8:3B:BF"],
    "Apple"   : ["00:1C:B3", "00:1E:C2", "00:21:E9"],
    "Samsung" : ["00:00:F0", "00:07:AB", "00:12:47"],
    "Infinix" : ["08:8C:1A", "4C:94:10", "74:7E:80"],
    "Oppo"    : ["E4:40:97", "00:9C:06", "24:7A:B4", "30:10:E4"],
    "Xiaomi"  : ["CC:EB:5E", "C0:06:C3", "4C:5E:0C", "F4:3A:7B"],
    "Realme"  : ["0C:90:43", "0C:E6:7C", "60:71:08", "E8:86:14"],
    "Vivo"    : ["08:23:B2", "08:7F:98", "0C:60:46", "10:F6:81",
                 "1C:DA:27", "3C:A3:48", "5C:1C:B9", "60:91:F3",
                 "88:6A:B1", "9C:A5:C0"]
}

def generate_mac_by_vendor(vendor_name):
    # Mengubah input teks agar tidak sensitif huruf besar/kecil
    vendor_key = vendor_name.capitalize()

    if vendor_key not in VENDOR_PREFIXES:
        raise ValueError(f"Vendor '{vendor_name}' tidak ditemukan. Pilih: Apple, Samsung, atau Google.")

    # Memilih salah satu prefix secara acak dari vendor yang dipilih
    prefix = random.choice(VENDOR_PREFIXES[vendor_key])

    # Membuat 3 byte (6 digit) terakhir secara acak
    suffix = [random.randint(0x00, 0xff) for _ in range(3)]
    suffix_str = ":".join(f"{b:02x}" for b in suffix)

    # Menggabungkan prefix dan suffix
    mac_address = f"{prefix}:{suffix_str}"
    return mac_address.upper()

# --- CONTOH PENGGUNAAN ---
if __name__ == "__main__":
    # Uji coba untuk setiap vendor
    for vendor in ["Apple", "Samsung", "Oppo", "Vivo", "Infinix", "Xiaomi", "Realme"]:
        print(f"MAC {vendor}: {generate_mac_by_vendor(vendor)}")
