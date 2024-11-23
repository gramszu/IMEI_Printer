import sys
import datetime
import re
import subprocess
import time
import logging
from zebra import Zebra

# Konfiguracja logowania
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Wersja Pythona
print(sys.version)
logging.info(f"Uruchomiono skrypt z Pythonem {sys.version}")

# Inicjalizacja zmiennej do przechowywania poprzedniej wartości zmiennej extracted_imei
previous_extracted_imei = None

try:
    # Otwarcie pliku na zewnątrz pętli
    with open("wydrukowane_imei.txt", "a") as file:
        # Utwórz obiekt drukarki
        z = Zebra("Zebra_TLP2844")

        # Ustaw parametry drukarki
        z.setup(direct_thermal=True, label_height=(200, 3), label_width=300)

        while True:
            try:
                # Odczytaj zawartość schowka
                clipboard_text = subprocess.check_output(['pbpaste']).decode('utf-8')
                logging.debug(f"Zawartość schowka: {clipboard_text}")

                # Wyodrębnij numer IMEI
                match = re.search(r'IMEI:(.*?);', clipboard_text)
                if match:
                    extracted_imei = match.group(1).strip()
                    # Usunięcie niealfanumerycznych znaków
                    extracted_imei = re.sub(r'\W+', '', extracted_imei)
                    logging.debug(f"Wyodrębniony numer IMEI: {extracted_imei}")
                else:
                    extracted_imei = None
                    logging.warning("Nie znaleziono numeru IMEI w schowku.")

                # Sprawdź, czy wartość extracted_imei zmieniła się i czy jest poprawna
                if extracted_imei and extracted_imei != previous_extracted_imei:
                    # Szablon etykiety z wstawionym numerem IMEI
                    label_template = f"""
N
S2
D10
ZB
q300
Q320,28
A80,5,0,4,1,1,N,"*GWARANCJA*"
A60,40,0,3,1,1,N,"{extracted_imei}"
A60,100,0,1,1,1,N,"www.megaelektronik.pl"
P2
"""
                    try:
                        # Wyślij kod EPL do drukarki
                        z.output(label_template)
                        logging.info(f"Wysłano etykietę do drukarki z numerem IMEI: {extracted_imei}")
                    except Exception as e:
                        logging.error(f"Błąd podczas drukowania: {e}")

                    # Zapisz wydrukowany numer IMEI wraz z datą i godziną do pliku tekstowego
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f"{current_time}: {extracted_imei}\n")
                    file.flush()  # Upewnij się, że dane zostały faktycznie zapisane

                    # Zaktualizuj poprzednią wartość zmiennej extracted_imei
                    previous_extracted_imei = extracted_imei
                else:
                    logging.debug("Numer IMEI nie zmienił się lub jest niepoprawny.")

            except Exception as e:
                logging.error(f"Błąd podczas przetwarzania schowka: {e}")

            # Poczekaj przed ponownym sprawdzeniem zawartości schowka
            time.sleep(1)

except Exception as e:
    logging.critical(f"Błąd krytyczny: {e}")
