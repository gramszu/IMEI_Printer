import subprocess
import re
import time
import datetime

# Inicjalizacja zmiennej do przechowywania poprzedniej wartości zmiennej extracted_text
previous_extracted_text = None

# Otwarcie pliku na zewnątrz pętli
with open("wydrukowane_imei.txt", "a") as file:
    while True:
        # Odczytaj zawartość schowka
        clipboard_text = subprocess.check_output(['pbpaste']).decode('utf-8')

        # Wyodrębnij tekst pomiędzy "IMEI:" a znakiem ";"
        match = re.search(r'IMEI:(.*?);', clipboard_text)
        if match:
            extracted_text = match.group(1).strip()
        else:
            extracted_text = "Nie znaleziono"

        # Sprawdź, czy wartość extracted_text zmieniła się
        if extracted_text != previous_extracted_text:
            # Utwórz zawartość kodu EPL z komendą P3 dla trzech kopii
            epl_code = f"""N
q800
Q50,20
B100,150,N {extracted_text}
P1
"""

            # Wysłanie kodu EPL do drukarki za pomocą polecenia lpr
            try:
                process = subprocess.Popen(['lpr', '-P', 'Zebra_TLP2844'], stdin=subprocess.PIPE)
                process.communicate(input=epl_code.encode('utf-8'))
                process.wait()
                print("Drukowanie zakończone.")

                # Zapisz wydrukowany numer IMEI wraz z datą i godziną do pliku tekstowego
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{current_time}: {extracted_text}\n")
                file.flush()  # Upewnij się, że dane zostały faktycznie zapisane

            except Exception as e:
                print(f"Wystąpił błąd podczas drukowania: {e}")

            # Zaktualizuj poprzednią wartość zmiennej extracted_text
            previous_extracted_text = extracted_text

        # Poczekaj przed ponownym sprawdzeniem zawartości schowka
        time.sleep(1)
