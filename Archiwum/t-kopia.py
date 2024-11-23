import sys
import datetime
import re
import subprocess
import time
from zebra import Zebra
import barcode
from barcode.writer import ImageWriter

def generate_barcode(imei):
    # Usuń wszystkie znaki, które nie są cyframi
    imei_digits = ''.join(filter(str.isdigit, imei))

    # Jeśli numer IMEI ma mniej niż 14 cyfr, dodaj zera z przodu, aby uzyskać pełny numer IMEI
    imei_digits = imei_digits.zfill(14)

    # Utwórz obiekt kodu kreskowego EAN-13
    ean = barcode.get_barcode_class('ean13')

    # Wygeneruj kod kreskowy w formacie EAN-13
    ean_barcode = ean(imei_digits, writer=ImageWriter())

    # Zapisz wygenerowany kod kreskowy do pliku PNG
    filename = f'barcode_{imei}.png'
    ean_barcode.save(filename)

    return filename

# Wersja Pythona
print(sys.version)

# Inicjalizacja zmiennej do przechowywania poprzedniej wartości zmiennej extracted_imei
previous_extracted_imei = None

# Otwarcie pliku na zewnątrz pętli
with open("wydrukowane_imei.txt", "a") as file:
    # Utwórz obiekt drukarki
    z = Zebra("Zebra_TLP2844")

    # Ustaw parametry drukarki
    z.setup(direct_thermal=True, label_height=(200, 3), label_width=300)

    while True:
        # Odczytaj zawartość schowka
        clipboard_text = subprocess.check_output(['pbpaste']).decode('utf-8')

        # Wyodrębnij numer IMEI
        match = re.search(r'IMEI:(.*?);', clipboard_text)
        if match:
            extracted_imei = match.group(1).strip()
        else:
            extracted_imei = "Nie znaleziono"
         
        # Sprawdź, czy wartość extracted_imei zmieniła się
        if extracted_imei != previous_extracted_imei:
            # Szablon etykiety z wstawionym numerem IMEI
            label_template = f"""
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q300
D20
A80,5,0,4,1,1,N,"*GWARANCJA*"
A60,40,0,3,1,1,N,"{extracted_imei}"
A60,100,0,1,1,1,N,"www.megaelektronik.pl"
P1
"""

            # Generowanie kodu kreskowego z numerem IMEI
            barcode_filename = generate_barcode(extracted_imei)

            # Wstawienie kodu kreskowego do szablonu etykiety
            label_template_with_barcode = label_template + f"""
N
LO140,170,2,3,3
BQ,2,10
FD{barcode_filename}
P1
"""

            # Wyślij kod EPL do drukarki
            z.output(label_template_with_barcode)

            # Zapisz wydrukowany numer IMEI wraz z datą i godziną do pliku tekstowego
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{current_time}: {extracted_imei}\n")
            file.flush()  # Upewnij się, że dane zostały faktycznie zapisane

            # Zaktualizuj poprzednią wartość zmiennej extracted_imei
            previous_extracted_imei = extracted_imei

        # Poczekaj przed ponownym sprawdzeniem zawartości schowka
        time.sleep(1)
