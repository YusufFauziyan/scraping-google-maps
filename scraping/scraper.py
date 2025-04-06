from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def scroll_down(driver):
    """Scroll panel hasil Google Maps sampai bawah"""
    try:
        # Temukan panel scrollable (class atau role-nya bisa berubah)
        scrollable_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="main"]//div[@aria-label]'))
        )
        
        last_height = 0
        while True:
            # Scroll ke bawah
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_panel)
            time.sleep(2)  # Tunggu loading
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_panel)
            if new_height == last_height:
                break  # Berhenti jika sudah di paling bawah
            last_height = new_height
    except Exception as e:
        print("Gagal scroll:", e)

def scrape_coffee_shops():
    options = Options()
    options.add_argument("--window-size=1200,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/maps/search/coffee+shop+di+Sukabumi,+Jawa+Barat")

    time.sleep(5)  # Tunggu halaman terbuka
    scroll_down(driver)  # Scroll untuk muat semua tempat

    # Cari semua card tempat (gunakan XPath lebih generik)
    places = driver.find_elements(By.CLASS_NAME, 'UaQhfb')
    print(f"Found {len(places)} places.")

    data = []
    for place in places:
        try:
            try:
                name = place.find_element(By.CLASS_NAME, 'qBF1Pd').text
            except:
                name = 'N/A'

            try:
                address = place.find_element(By.XPATH, ".//span[contains(text(),'Jl.')]").text
            except:
                address = "Alamat tidak ditemukan"
        
            try:
                rating = place.find_element(By.CLASS_NAME, 'MW4etd').text
            except:
                rating = "N/A"

            print(f"Nama: {name}, Alamat: {address}, Rating: {rating}")

            data.append({
                "name": name,
                "address": address,
                "rating": rating
            })

        except Exception as e:
            print(f"Gagal ekstrak data: {e}")
            continue


    driver.quit()

    # Simpan ke JSON
    os.makedirs("data", exist_ok=True)
    with open("data/sukabumi_coffee_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Berhasil menyimpan {len(data)} coffee shop!")

if __name__ == "__main__":
    scrape_coffee_shops()