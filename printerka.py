import sys
print(sys.version)
import datetime
from zebra import Zebra
import time
import cups



# Definicja kodów kolorów ANSI1
RED = '\033[91m'
GREEN = '\033[92m'
END = '\033[0m'

from termcolor import colored



def print_mega_in_yellow_frame():
    #print("\n" * 1)
    
    text1 = "PRINTERKA  Megaelektronik v1.0"
    text2 = "     powered by gramszu"
    
    max_len = max(len(text1), len(text2))
    
    framed_text = f"{'*' * (max_len + 4)}\n"
    
    framed_text += f"* {colored(text1, 'blue')}{' ' * (max_len - len(text1))} *\n"
    framed_text += f"* {colored(text2, 'blue')}{' ' * (max_len - len(text2))} *\n"
    
    framed_text += f"{'*' * (max_len + 4)}"

    print(framed_text)





# Available labels
available_labels = {
    "Sim Ster + Box": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"125"
A370,140,0,5,1,1,B,"BOX"
A90,15,0,5,1,1,B,"SIM STER+"
A50,80,0,4,1,1,N,"VDC 5-25V Max 0.5A"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}
""",

    "Sim Ster+ PCB": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"125"
A370,140,0,5,1,1,B,"PCB"
A90,15,0,5,1,1,B,"SIM STER+"
A50,90,0,4,1,1,N,"VDC 5-25V Max 0.5A"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}
""",

    "Bram Ster+ Box": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"125"
A370,140,0,5,1,1,B,"BOX"
A90,15,0,5,1,1,B,"BRAM STER+"
A50,90,0,4,1,1,N,"VDC 5-25V Max 0.5A"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",

    "Bram Ster+ PCB": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"125"
A370,140,0,5,1,1,B,"PCB"
A90,15,0,5,1,1,B,"BRAM STER+"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",

 "Bram Ster+ PCB *25*": """\

N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"25"
A370,140,0,5,1,1,B,"PCB"
A90,15,0,5,1,1,B,"BRAM STER+"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}




""",
    
    "Sim Eco+ PCB": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A30,35,0,5,1,1,B,"SIM ECO+ PCB"
A150,100,0,4,1,1,N,"Sterownik GSM"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",
    "Sim Eco+ Box": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A30,35,0,5,1,1,B,"SIM ECO+ BOX"
A150,100,0,4,1,1,N,"Sterownik GSM"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",
    "Ster Max+ Box": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,140,0,5,1,1,B,"BOX"
A30,35,0,5,1,1,B,"STER MAX+"
A100,100,0,4,1,1,N,"zdalne sterowanie GSM"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",

    "Ster Max+ PCB": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,140,0,5,1,1,B,"PCB"
A30,35,0,5,1,1,B,"STER MAX+"
A100,100,0,4,1,1,N,"zdalne sterowanie GSM"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",

 "Czujnik CTS+ ****2.5m****": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,140,0,5,1,1,B,"2.5"
A30,35,0,5,1,1,B,"CTS+"
A100,100,0,4,1,1,N,"Czujnik temperatury"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",

    

"***Sim Ster+ 125***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,80,0,4,1,1,N,"Users -125-"
A80,40,0,4,1,1,N,"Sim Ster+ PCB"
P{num_labels}

""",


"***BRAM Ster+ 125***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"Users -125-"
A80,10,0,4,1,1,B,"BRAM STER+ PCB"
A90,50,0,4,1,1,N,"do wbudowania"

P{num_labels}

""",


"***Sim Eco+ ***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"Do wbudowania"
A80,10,0,4,1,1,B,"Sim ECO+ PCB"

P{num_labels}

""",

"***Ster Max+ ***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"standard"
A80,10,0,4,1,1,B,"Ster Max+ "

P{num_labels}

""",

"***BRAM Ster+ ***25***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"Users *25*"
A80,10,0,4,1,1,B,"Bram Ster+"
A90,50,0,4,1,1,N,"Standard"

P{num_labels}

""",    


"***Czujnik CTS+ ***2small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"Czujnik"
A80,10,0,4,1,1,B,"CTS+"
A90,50,0,4,1,1,N,"Standard 2.5m"

P{num_labels}

""",    
        

 "Bram Ster+ STARTER ": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q480
D20
A370,75,0,5,1,1,N,"2"
A370,140,0,5,1,1,B,""
A90,15,0,5,1,1,B,"STARTER+"
A50,120,0,4,1,1,B,"Master Code: C3D4"
A50,150,0,4,1,1,N,"Status:Test OK"
A50,180,0,4,1,1,N,"{datetime}"
A50,220,0,4,1,1,N,"www.megaelektronik.pl"
A130,260,0,4,1,1,N,"made in poland"
P{num_labels}

""",
    

"***STARTER+ ***2***small***": """\
N
S2
D2
ZT
JF
OD
R5,5
Q320,28
q350
D20
A90,90,0,4,1,1,N,"Users *2*"
A80,10,0,4,1,1,B,"STARTER+"
A90,50,0,4,1,1,N,"Standard"

P{num_labels}

""",        
    
}

def print_label(selected_label, num_labels):
    label_template = available_labels.get(selected_label, "")

    if label_template:
        label_template = label_template.replace("{num_labels}", num_labels)  # Zastąp {num_labels} w kodzie etykiety

        # Ustaw parametry drukarki
        z = Zebra("Zebra_TLP2844")  # Tutaj możesz ustawić domyślną drukarkę
        z.setup(direct_thermal=True, label_height=(400, 2), label_width=600)

        # Dodaj aktualną datę i godzinę do kodu ZPL
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        label_template = label_template.replace("{datetime}", now)

        # Wyślij kod ZPL do drukarki
        confirmation = input(f"do you want to be  sure print  {num_labels} labels ? (y/n): ")
        if confirmation.lower() == "y":
            #for _ in range(int(num_labels)):
                z.output(label_template)
            #print(f"Wydrukowano {num_labels} etykiety(y).")
        else:
            print("cancel printer.")
            
            
            
def print_frame(text):
    text_length = len(text)
    frame_width = text_length + 4

    print("+" * frame_width)
    print(f"+{' ' * (frame_width - 2)}+")
    print(f"+ {text} +")
    print(f"+{' ' * (frame_width - 2)}+")
    print("+" * frame_width)



def print_header(header_text):
    print_frame(header_text)            
            

def main():
    print ("\n" *1)
    print_mega_in_yellow_frame()
    #print_header("PRINTERKA ZEBRA 1.0 gramszu")
    print ("\n" *1)
    
    while True:
        print("Avaible labels : ")
        print()
        for i, label in enumerate(available_labels.keys(), start=1):
            print(f"{i} - {label}")

        print ("")
        selected_label_index = int(input("Label choice  (enter number): ")) - 1

        labels_list = list(available_labels.keys())
        selected_label = labels_list[selected_label_index]

        num_labels = input("How much ?: ")

        print(f"Label choice: {selected_label}, number of labels: {num_labels}")

        print_label(selected_label, num_labels)
        
        # Po wydrukowaniu etykiet, pytaj użytkownika, czy chce wydrukować kolejne
        

if __name__ == "__main__":
    main()






