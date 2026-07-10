# BuTik - Simple Bruteforce Voucher Hotspot

BuTik adalah sebuah skrip otomatisasi berbasis Python yang dirancang untuk melakukan pengujian penetrasi (*penetration testing*) ringan pada halaman login captive portal (Hotspot) berbasis MikroTik. Alat ini bekerja dengan mensimulasikan percobaan login kode voucher secara acak berbasiskan konfigurasi karakter dan panjang tertentu.

## Fungsi Utama
*   **Dual-Method Authentication Handling**: Otomatis mendeteksi dan mendukung mekanisme login menggunakan metode **CHAP** (dengan enkripsi MD5 berbasis *challenge*) maupun **PAP** (teks polos/plain text).
*   **Stealth Request Simulation**: Menggunakan repositori User-Agent perangkat seluler (Android) secara acak serta menyertakan *header* pelengkap untuk meminimalkan deteksi pemblokiran standar oleh sistem keamanan portal.
*   **Session Continuity & History**: Menyimpan setiap riwayat percobaan kode voucher ke dalam file log agar tidak terjadi pengujian duplikat pada kode yang sama di sesi berikutnya.
*   **Dynamic Delay (Anti-Rate Limiting)**: Menyediakan jeda waktu (*delay*) acak di antara setiap permintaan untuk menghindari deteksi *rate-limiting* (pembatasan frekuensi) pada sisi server.

## Kegunaan
Skrip ini ditujukan untuk **tujuan edukasi, audit keamanan, dan pengujian kerentanan internal** (*security assessment*) oleh administrator jaringan guna menguji seberapa kuat kombinasi karakter voucher hotspot yang diterapkan (menghindari kerentanan tebakan voucher yang terlalu pendek atau mudah ditebak).

---

## Persyaratan Sistem

Pastikan perangkat Anda telah terinstal Python 3.x dan pustaka `requests`:
```bash
pip install -r requirements.txt
```

### Config file `config.ini`
```ini
[TARGET]
name = Wifi_Kantor_Test
url = [http://10.10.10.1/](http://10.10.10.1/)

[SETTINGS]
charset = abcdefghijklmnopqrstuvwxyz0123456789
error_class = notice
length = 5
delay_min = 0.5
delay_max = 1.5

[HISTORY]
file = history.txt
success = success.txt
```

## Penjelasan Parameter Konfigurasi:
- [TARGET]:
	- name: Nama penanda target yang akan muncul pada banner skrip.
	- url: Alamat dasar (base URL) halaman login captive portal MikroTik Anda.

- [SETTINGS]:
	- charset: Kumpulan karakter yang akan digunakan untuk menyusun kode voucher acak.
    - error_class: Nama class untuk menangkap pesan error
	- length: Panjang digit kode voucher yang akan diuji.
	- delay_min & delay_max: Rentang waktu jeda minimum dan maksimum (dalam detik) antar-permintaan request.

- [HISTORY]:
	- file: File log untuk mencatat semua kode voucher yang sudah pernah dicoba.
	- success: File log khusus untuk menyimpan kode voucher yang berhasil menembus autentikasi sistem.

# License
[GNU GPLv3](./LICENSE)
