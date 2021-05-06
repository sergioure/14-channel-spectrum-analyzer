import machine
import time
import math

led_enplaca = machine.Pin(25, machine.Pin.OUT)

sdi = machine.Pin(0,machine.Pin.OUT)
rclk = machine.Pin(1,machine.Pin.OUT)
srclk = machine.Pin(2,machine.Pin.OUT)

TR1 = machine.Pin(3,machine.Pin.OUT)
TR2 = machine.Pin(4,machine.Pin.OUT)
TR3 = machine.Pin(5,machine.Pin.OUT)
TR4 = machine.Pin(6,machine.Pin.OUT)
TR5 = machine.Pin(7,machine.Pin.OUT)
TR6 = machine.Pin(8,machine.Pin.OUT)
TR7 = machine.Pin(9,machine.Pin.OUT)
TR8 = machine.Pin(10,machine.Pin.OUT)

RGB_R = machine.PWM(machine.Pin(11))
RGB_G = machine.PWM(machine.Pin(12))
RGB_B = machine.PWM(machine.Pin(13))
RGB_R.freq(1000)
RGB_G.freq(1000)
RGB_B.freq(1000)

button1 = machine.Pin(14, machine.Pin.IN)
button2 = machine.Pin(15, machine.Pin.IN)

Strobe1 = machine.Pin(22,machine.Pin.OUT)
RST1_MSG= machine.Pin(21,machine.Pin.OUT)
Audio1 = machine.ADC(27)  #ADC1
Banda1 = [0,0,0,0,0,0,0,0]

Strobe2 = machine.Pin(20,machine.Pin.OUT)
RST2_MSG= machine.Pin(19,machine.Pin.OUT)
Audio2 = machine.ADC(26)  #ADC0
Banda2 = [0,0,0,0,0,0,0,0]

valor_1_8k = 0
valor_1_16k = 0
valor_1_24k = 0
valor_1_32k = 0
valor_1_40k = 0
valor_1_49k = 0
valor_1_57k = 0
valor_1_65k = 0

valor_2_8k = 0
valor_3_16k = 0
valor_2_24k = 0
valor_2_32k = 0
valor_2_40k = 0
valor_2_49k = 0
valor_2_57k = 0
valor_2_65k = 0

dato8k_1 = [0,0,0,0,0,0,0,0]
dato8k_2 = [0,0,0,0,0,0,0,0]
dato16k_1 = [0,0,0,0,0,0,0,0]
dato16k_2 = [0,0,0,0,0,0,0,0]
dato24k_1 = [0,0,0,0,0,0,0,0]
dato24k_2 = [0,0,0,0,0,0,0,0]
dato32k_1 = [0,0,0,0,0,0,0,0]
dato32k_2 = [0,0,0,0,0,0,0,0]
dato40k_1 = [0,0,0,0,0,0,0,0]
dato40k_2 = [0,0,0,0,0,0,0,0]
dato49k_1 = [0,0,0,0,0,0,0,0]
dato49k_2 = [0,0,0,0,0,0,0,0]
dato57k_1 = [0,0,0,0,0,0,0,0]
dato57k_2 = [0,0,0,0,0,0,0,0]
dato65k_1 = [0,0,0,0,0,0,0,0]
dato65k_2 = [0,0,0,0,0,0,0,0]

retardo =1200
retardo_led=300

       
# *** SUBRUTINAS ***
# *** SUBRUTINA PWM LEDS RGB ***
def leds_rgb(color):
# apagado
    if color == 0: 
        RGB_R.duty_u16(0)
        RGB_G.duty_u16(0)
        RGB_B.duty_u16(0)
        # VERDE
    if color == 1: 
        RGB_R.duty_u16(0)
        RGB_G.duty_u16(65535)
        RGB_B.duty_u16(0)
       # ROJO
    if color == 2: 
        RGB_R.duty_u16(65535)
        RGB_G.duty_u16(0)
        RGB_B.duty_u16(0)
       # AZUL
    if color == 3: 
        RGB_R.duty_u16(0)
        RGB_G.duty_u16(0)
        RGB_B.duty_u16(65535)
        # AMARILLO
    if color == 4: 
        RGB_R.duty_u16(65535)
        RGB_G.duty_u16(65535)
        RGB_B.duty_u16(0)
        # CYAN
    if color == 5: 
        RGB_R.duty_u16(0)
        RGB_G.duty_u16(65535)
        RGB_B.duty_u16(65535)
        # MAGENTA
    if color == 6: 
        RGB_R.duty_u16(65535)
        RGB_G.duty_u16(0)
        RGB_B.duty_u16(65535)
        # BLANCO
    if color == 7: 
        RGB_R.duty_u16(65535)
        RGB_G.duty_u16(65535)
        RGB_B.duty_u16(65535)
        
# *** SUBRUTINA FUNCIONAMIENTO 74HC595 ***
def hc595_shift(dat):
    rclk.low()
    time.sleep_us(1)
    for bit in range(7, -1, -1):
        srclk.low()
        time.sleep_us(1)
        value = 1 & (dat >> bit)
        sdi.value(value)
        time.sleep_us(1)
        srclk.high()
        time.sleep_us(1)
    time.sleep_us(1)
    rclk.high()
    time.sleep_us(1)
    
# *** SUBRUTINA MEDIDA DEL AUDIO ***
def Ciclo_case(valor_audio):
    resultado = 0
    if valor_audio>0 and valor_audio<=8191:
        resultado =1
    if valor_audio>8192 and valor_audio<=16383:
        resultado =2
    if valor_audio>16834 and valor_audio<=24575:
        resultado =3
    if valor_audio>24576 and valor_audio<=32767:
        resultado =4
    if valor_audio>32768 and valor_audio<=40959:
        resultado =5
    if valor_audio>40960 and valor_audio<=49151:
        resultado =6
    if valor_audio>49152 and valor_audio<=57343:
        resultado =7
    if valor_audio>57344 and valor_audio<=65535:
        resultado =8
    return resultado 
  
# *** SUBRUTINA PRINCIPAL - PRENDE LOS LEDS  ***
def LeerMSEGQ7():
    RST1_MSG.value(1)
    time.sleep_ms(1)
    RST1_MSG.value(0)
    time.sleep_us(75)
    
    for bit in range(0, 7, 1):
        Strobe1.value(0)
        time.sleep_us(40)
        Banda1[bit] = Audio1.read_u16()
        Strobe1.value(1)
        time.sleep_us(40)
#         print(Audio1.read_u16())
   
    RST2_MSG.value(1)
    time.sleep_ms(1)
    RST2_MSG.value(0)
    time.sleep_us(75)
    
    for bit in range(0, 7, 1):
        Strobe2.value(0)
        time.sleep_us(40)
        Banda2[bit] = Audio2.read_u16()
        Strobe2.value(1)
        time.sleep_us(40)
#         print(Audio2.read_u16())
      
#   *** se lee el primer valor analogico canal 1 - 63Hz ***
    valor_case = Ciclo_case(Banda1[0])
    if valor_case == 1:
        dato8k_1[0] =0
        dato16k_1[0] =0
        dato24k_1[0] =0
        dato32k_1[0] =0
        dato40k_1[0] =0
        dato49k_1[0] =0
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 2:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =0
        dato32k_1[0] =0
        dato40k_1[0] =0
        dato49k_1[0] =0
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 3:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =0
        dato40k_1[0] =0
        dato49k_1[0] =0
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 4:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =1
        dato40k_1[0] =0
        dato49k_1[0] =0
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 5:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =1
        dato40k_1[0] =1
        dato49k_1[0] =0
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 6:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =1
        dato40k_1[0] =1
        dato49k_1[0] =1
        dato57k_1[0] =0
        dato65k_1[0] =0
    if valor_case == 7:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =1
        dato40k_1[0] =1
        dato49k_1[0] =1
        dato57k_1[0] =1
        dato65k_1[0] =0
    if valor_case == 8:
        dato8k_1[0] =1
        dato16k_1[0] =1
        dato24k_1[0] =1
        dato32k_1[0] =1
        dato40k_1[0] =1
        dato49k_1[0] =1
        dato57k_1[0] =1
        dato65k_1[0] =1
        
#*** se lee el primer valor analogico canal 1 - 160Hz ***
    valor_case = Ciclo_case(Banda1[1])
    if valor_case == 1:
        dato8k_1[1] =0
        dato16k_1[1] =0
        dato24k_1[1] =0
        dato32k_1[1] =0
        dato40k_1[1] =0
        dato49k_1[1] =0
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 2:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =0
        dato32k_1[1] =0
        dato40k_1[1] =0
        dato49k_1[1] =0
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 3:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =0
        dato40k_1[1] =0
        dato49k_1[1] =0
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 4:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =1
        dato40k_1[1] =0
        dato49k_1[1] =0
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 5:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =1
        dato40k_1[1] =1
        dato49k_1[1] =0
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 6:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =1
        dato40k_1[1] =1
        dato49k_1[1] =1
        dato57k_1[1] =0
        dato65k_1[1] =0
    if valor_case == 7:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =1
        dato40k_1[1] =1
        dato49k_1[1] =1
        dato57k_1[1] =1
        dato65k_1[1] =0
    if valor_case == 8:
        dato8k_1[1] =1
        dato16k_1[1] =1
        dato24k_1[1] =1
        dato32k_1[1] =1
        dato40k_1[1] =1
        dato49k_1[1] =1
        dato57k_1[1] =1
        dato65k_1[1] =1
    
# *** se lee el primer valor analogico canal 1 - 400Hz ***
    valor_case = Ciclo_case(Banda1[2])
    if valor_case == 1:
        dato8k_1[2] =0
        dato16k_1[2] =0
        dato24k_1[2] =0
        dato32k_1[2] =0
        dato40k_1[2] =0
        dato49k_1[2] =0
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 2:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =0
        dato32k_1[2] =0
        dato40k_1[2] =0
        dato49k_1[2] =0
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 3:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =0
        dato40k_1[2] =0
        dato49k_1[2] =0
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 4:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =1
        dato40k_1[2] =0
        dato49k_1[2] =0
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 5:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =1
        dato40k_1[2] =1
        dato49k_1[2] =0
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 6:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =1
        dato40k_1[2] =1
        dato49k_1[2] =1
        dato57k_1[2] =0
        dato65k_1[2] =0
    if valor_case == 7:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =1
        dato40k_1[2] =1
        dato49k_1[2] =1
        dato57k_1[2] =1
        dato65k_1[2] =0
    if valor_case == 8:
        dato8k_1[2] =1
        dato16k_1[2] =1
        dato24k_1[2] =1
        dato32k_1[2] =1
        dato40k_1[2] =1
        dato49k_1[2] =1
        dato57k_1[2] =1
        dato65k_1[2] =1
        
# *** se lee el primer valor analogico canal 1 - 1000Hz ***
    valor_case = Ciclo_case(Banda1[3])
    if valor_case == 1:
        dato8k_1[3] =0
        dato16k_1[3] =0
        dato24k_1[3] =0
        dato32k_1[3] =0
        dato40k_1[3] =0
        dato49k_1[3] =0
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 2:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =0
        dato32k_1[3] =0
        dato40k_1[3] =0	
        dato49k_1[3] =0
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 3:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =0
        dato40k_1[3] =0
        dato49k_1[3] =0
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 4:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =1
        dato40k_1[3] =0
        dato49k_1[3] =0
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 5:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =1
        dato40k_1[3] =1
        dato49k_1[3] =0
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 6:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =1
        dato40k_1[3] =1
        dato49k_1[3] =1
        dato57k_1[3] =0
        dato65k_1[3] =0
    if valor_case == 7:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =1
        dato40k_1[3] =1
        dato49k_1[3] =1
        dato57k_1[3] =1
        dato65k_1[3] =0
    if valor_case == 8:
        dato8k_1[3] =1
        dato16k_1[3] =1
        dato24k_1[3] =1
        dato32k_1[3] =1
        dato40k_1[3] =1
        dato49k_1[3] =1
        dato57k_1[3] =1
        dato65k_1[3] =1
            
# *** se lee el primer valor analogico canal 1 - 2500Hz ***
    valor_case = Ciclo_case(Banda1[4])
    if valor_case == 1:
        dato8k_1[4] =0
        dato16k_1[4] =0
        dato24k_1[4] =0
        dato32k_1[4] =0
        dato40k_1[4] =0
        dato49k_1[4] =0
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 2:
        dato8k_1[4] =1	
        dato16k_1[4] =1
        dato24k_1[4] =0
        dato32k_1[4] =0
        dato40k_1[4] =0	
        dato49k_1[4] =0
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 3:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =0
        dato40k_1[4] =0
        dato49k_1[4] =0
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 4:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =1
        dato40k_1[4] =0
        dato49k_1[4] =0
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 5:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =1
        dato40k_1[4] =1
        dato49k_1[4] =0
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 6:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =1
        dato40k_1[4] =1
        dato49k_1[4] =1
        dato57k_1[4] =0
        dato65k_1[4] =0
    if valor_case == 7:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =1
        dato40k_1[4] =1
        dato49k_1[4] =1
        dato57k_1[4] =1
        dato65k_1[4] =0
    if valor_case == 8:
        dato8k_1[4] =1
        dato16k_1[4] =1
        dato24k_1[4] =1
        dato32k_1[4] =1
        dato40k_1[4] =1
        dato49k_1[4] =1
        dato57k_1[4] =1
        dato65k_1[4] =1
            
# *** se lee el primer valor analogico canal 1 - 6250Hz ***
    valor_case = Ciclo_case(Banda1[5])
    if valor_case == 1:
        dato8k_1[5] =0
        dato16k_1[5] =0
        dato24k_1[5] =0
        dato32k_1[5] =0
        dato40k_1[5] =0
        dato49k_1[5] =0
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 2:
        dato8k_1[5] =1	
        dato16k_1[5] =1
        dato24k_1[5] =0
        dato32k_1[5] =0
        dato40k_1[5] =0	
        dato49k_1[5] =0
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 3:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =0
        dato40k_1[5] =0
        dato49k_1[5] =0
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 4:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =1
        dato40k_1[5] =0
        dato49k_1[5] =0
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 5:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =1
        dato40k_1[5] =1
        dato49k_1[5] =0
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 6:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =1
        dato40k_1[5] =1
        dato49k_1[5] =1
        dato57k_1[5] =0
        dato65k_1[5] =0
    if valor_case == 7:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =1
        dato40k_1[5] =1
        dato49k_1[5] =1
        dato57k_1[5] =1
        dato65k_1[5] =0
    if valor_case == 8:
        dato8k_1[5] =1
        dato16k_1[5] =1
        dato24k_1[5] =1
        dato32k_1[5] =1
        dato40k_1[5] =1
        dato49k_1[5] =1
        dato57k_1[5] =1
        dato65k_1[5] =1
        
# *** se lee el primer valor analogico canal 1 - 16KHz ***
    valor_case = Ciclo_case(Banda1[6])
    if valor_case == 1:
        dato8k_1[6] =0
        dato16k_1[6] =0
        dato24k_1[6] =0
        dato32k_1[6] =0
        dato40k_1[6] =0
        dato49k_1[6] =0
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 2:
        dato8k_1[6] =1	
        dato16k_1[6] =1
        dato24k_1[6] =0
        dato32k_1[6] =0
        dato40k_1[6] =0	
        dato49k_1[6] =0
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 3:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =0
        dato40k_1[6] =0
        dato49k_1[6] =0
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 4:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =1
        dato40k_1[6] =0
        dato49k_1[6] =0
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 5:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =1
        dato40k_1[6] =1
        dato49k_1[6] =0
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 6:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =1
        dato40k_1[6] =1
        dato49k_1[6] =1
        dato57k_1[6] =0
        dato65k_1[6] =0
    if valor_case == 7:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =1
        dato40k_1[6] =1
        dato49k_1[6] =1
        dato57k_1[6] =1
        dato65k_1[6] =0
    if valor_case == 8:
        dato8k_1[6] =1
        dato16k_1[6] =1
        dato24k_1[6] =1
        dato32k_1[6] =1
        dato40k_1[6] =1
        dato49k_1[6] =1
        dato57k_1[6] =1
        dato65k_1[6] =1
        
    #   *** se lee el primer valor analogico canal 2- 63Hz ***
    valor_case = Ciclo_case(Banda2[0])
    if valor_case == 1:
        dato8k_2[0] =0
        dato16k_2[0] =0
        dato24k_2[0] =0
        dato32k_2[0] =0
        dato40k_2[0] =0
        dato49k_2[0] =0
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 2:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =0
        dato32k_2[0] =0
        dato40k_2[0] =0
        dato49k_2[0] =0
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 3:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =0
        dato40k_2[0] =0
        dato49k_2[0] =0
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 4:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =1
        dato40k_2[0] =0
        dato49k_2[0] =0
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 5:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =1
        dato40k_2[0] =1
        dato49k_2[0] =0
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 6:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =1
        dato40k_2[0] =1
        dato49k_2[0] =1
        dato57k_2[0] =0
        dato65k_2[0] =0
    if valor_case == 7:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =1
        dato40k_2[0] =1
        dato49k_2[0] =1
        dato57k_2[0] =1
        dato65k_2[0] =0
    if valor_case == 8:
        dato8k_2[0] =1
        dato16k_2[0] =1
        dato24k_2[0] =1
        dato32k_2[0] =1
        dato40k_2[0] =1
        dato49k_2[0] =1
        dato57k_2[0] =1
        dato65k_2[0] =1
        
#*** se lee el primer valor analogico canal 2- 160Hz ***
    valor_case = Ciclo_case(Banda2[1])
    if valor_case == 1:
        dato8k_2[1] =0
        dato16k_2[1] =0
        dato24k_2[1] =0
        dato32k_2[1] =0
        dato40k_2[1] =0
        dato49k_2[1] =0
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 2:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =0
        dato32k_2[1] =0
        dato40k_2[1] =0
        dato49k_2[1] =0
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 3:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =0
        dato40k_2[1] =0
        dato49k_2[1] =0
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 4:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =1
        dato40k_2[1] =0
        dato49k_2[1] =0
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 5:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =1
        dato40k_2[1] =1
        dato49k_2[1] =0
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 6:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =1
        dato40k_2[1] =1
        dato49k_2[1] =1
        dato57k_2[1] =0
        dato65k_2[1] =0
    if valor_case == 7:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =1
        dato40k_2[1] =1
        dato49k_2[1] =1
        dato57k_2[1] =1
        dato65k_2[1] =0
    if valor_case == 8:
        dato8k_2[1] =1
        dato16k_2[1] =1
        dato24k_2[1] =1
        dato32k_2[1] =1
        dato40k_2[1] =1
        dato49k_2[1] =1
        dato57k_2[1] =1
        dato65k_2[1] =1
    
# *** se lee el primer valor analogico canal 2- 400Hz ***
    valor_case = Ciclo_case(Banda2[2])
    if valor_case == 1:
        dato8k_2[2] =0
        dato16k_2[2] =0
        dato24k_2[2] =0
        dato32k_2[2] =0
        dato40k_2[2] =0
        dato49k_2[2] =0
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 2:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =0
        dato32k_2[2] =0
        dato40k_2[2] =0
        dato49k_2[2] =0
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 3:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =0
        dato40k_2[2] =0
        dato49k_2[2] =0
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 4:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =1
        dato40k_2[2] =0
        dato49k_2[2] =0
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 5:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =1
        dato40k_2[2] =1
        dato49k_2[2] =0
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 6:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =1
        dato40k_2[2] =1
        dato49k_2[2] =1
        dato57k_2[2] =0
        dato65k_2[2] =0
    if valor_case == 7:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =1
        dato40k_2[2] =1
        dato49k_2[2] =1
        dato57k_2[2] =1
        dato65k_2[2] =0
    if valor_case == 8:
        dato8k_2[2] =1
        dato16k_2[2] =1
        dato24k_2[2] =1
        dato32k_2[2] =1
        dato40k_2[2] =1
        dato49k_2[2] =1
        dato57k_2[2] =1
        dato65k_2[2] =1
        
# *** se lee el primer valor analogico canal 2- 1000Hz ***
    valor_case = Ciclo_case(Banda2[3])
    if valor_case == 1:
        dato8k_2[3] =0
        dato16k_2[3] =0
        dato24k_2[3] =0
        dato32k_2[3] =0
        dato40k_2[3] =0
        dato49k_2[3] =0
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 2:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =0
        dato32k_2[3] =0
        dato40k_2[3] =0	
        dato49k_2[3] =0
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 3:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =0
        dato40k_2[3] =0
        dato49k_2[3] =0
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 4:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =1
        dato40k_2[3] =0
        dato49k_2[3] =0
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 5:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =1
        dato40k_2[3] =1
        dato49k_2[3] =0
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 6:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =1
        dato40k_2[3] =1
        dato49k_2[3] =1
        dato57k_2[3] =0
        dato65k_2[3] =0
    if valor_case == 7:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =1
        dato40k_2[3] =1
        dato49k_2[3] =1
        dato57k_2[3] =1
        dato65k_2[3] =0
    if valor_case == 8:
        dato8k_2[3] =1
        dato16k_2[3] =1
        dato24k_2[3] =1
        dato32k_2[3] =1
        dato40k_2[3] =1
        dato49k_2[3] =1
        dato57k_2[3] =1
        dato65k_2[3] =1
            
# *** se lee el primer valor analogico canal 2- 2500Hz ***
    valor_case = Ciclo_case(Banda2[4])
    if valor_case == 1:
        dato8k_2[4] =0
        dato16k_2[4] =0
        dato24k_2[4] =0
        dato32k_2[4] =0
        dato40k_2[4] =0
        dato49k_2[4] =0
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 2:
        dato8k_2[4] =1	
        dato16k_2[4] =1
        dato24k_2[4] =0
        dato32k_2[4] =0
        dato40k_2[4] =0	
        dato49k_2[4] =0
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 3:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =0
        dato40k_2[4] =0
        dato49k_2[4] =0
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 4:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =1
        dato40k_2[4] =0
        dato49k_2[4] =0
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 5:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =1
        dato40k_2[4] =1
        dato49k_2[4] =0
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 6:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =1
        dato40k_2[4] =1
        dato49k_2[4] =1
        dato57k_2[4] =0
        dato65k_2[4] =0
    if valor_case == 7:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =1
        dato40k_2[4] =1
        dato49k_2[4] =1
        dato57k_2[4] =1
        dato65k_2[4] =0
    if valor_case == 8:
        dato8k_2[4] =1
        dato16k_2[4] =1
        dato24k_2[4] =1
        dato32k_2[4] =1
        dato40k_2[4] =1
        dato49k_2[4] =1
        dato57k_2[4] =1
        dato65k_2[4] =1
            
# *** se lee el primer valor analogico canal 2- 6250Hz ***
    valor_case = Ciclo_case(Banda2[5])
    if valor_case == 1:
        dato8k_2[5] =0
        dato16k_2[5] =0
        dato24k_2[5] =0
        dato32k_2[5] =0
        dato40k_2[5] =0
        dato49k_2[5] =0
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 2:
        dato8k_2[5] =1	
        dato16k_2[5] =1
        dato24k_2[5] =0
        dato32k_2[5] =0
        dato40k_2[5] =0	
        dato49k_2[5] =0
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 3:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =0
        dato40k_2[5] =0
        dato49k_2[5] =0
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 4:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =1
        dato40k_2[5] =0
        dato49k_2[5] =0
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 5:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =1
        dato40k_2[5] =1
        dato49k_2[5] =0
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 6:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =1
        dato40k_2[5] =1
        dato49k_2[5] =1
        dato57k_2[5] =0
        dato65k_2[5] =0
    if valor_case == 7:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =1
        dato40k_2[5] =1
        dato49k_2[5] =1
        dato57k_2[5] =1
        dato65k_2[5] =0
    if valor_case == 8:
        dato8k_2[5] =1
        dato16k_2[5] =1
        dato24k_2[5] =1
        dato32k_2[5] =1
        dato40k_2[5] =1
        dato49k_2[5] =1
        dato57k_2[5] =1
        dato65k_2[5] =1
        
# *** se lee el primer valor analogico canal 2- 16KHz ***
    valor_case = Ciclo_case(Banda2[6])
    if valor_case == 1:
        dato8k_2[6] =0
        dato16k_2[6] =0
        dato24k_2[6] =0
        dato32k_2[6] =0
        dato40k_2[6] =0
        dato49k_2[6] =0
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 2:
        dato8k_2[6] =1	
        dato16k_2[6] =1
        dato24k_2[6] =0
        dato32k_2[6] =0
        dato40k_2[6] =0	
        dato49k_2[6] =0
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 3:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =0
        dato40k_2[6] =0
        dato49k_2[6] =0
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 4:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =1
        dato40k_2[6] =0
        dato49k_2[6] =0
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 5:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =1
        dato40k_2[6] =1
        dato49k_2[6] =0
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 6:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =1
        dato40k_2[6] =1
        dato49k_2[6] =1
        dato57k_2[6] =0
        dato65k_2[6] =0
    if valor_case == 7:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =1
        dato40k_2[6] =1
        dato49k_2[6] =1
        dato57k_2[6] =1
        dato65k_2[6] =0
    if valor_case == 8:
        dato8k_2[6] =1
        dato16k_2[6] =1
        dato24k_2[6] =1
        dato32k_2[6] =1
        dato40k_2[6] =1
        dato49k_2[6] =1
        dato57k_2[6] =1
        dato65k_2[6] =1
        
# *** empezamos a encender los leds por filas ***
#  *** audio 1 ***
    valor_1_8k = (dato8k_1[0]*1) + (dato8k_1[1]*2) + (dato8k_1[2]*4) + (dato8k_1[3]*8) + (dato8k_1[4]*16) + (dato8k_1[5]*32) + (dato8k_1[6]*64) 
    valor_1_16k = (dato16k_1[0]*1) + (dato16k_1[1]*2) + (dato16k_1[2]*4) + (dato16k_1[3]*8) + (dato16k_1[4]*16) + (dato16k_1[5]*32) + (dato16k_1[6]*64) 
    valor_1_24k = (dato24k_1[0]*1) + (dato24k_1[1]*2) + (dato24k_1[2]*4) + (dato24k_1[3]*8) + (dato24k_1[4]*16) + (dato24k_1[5]*32) + (dato24k_1[6]*64)
    valor_1_32k = (dato32k_1[0]*1) + (dato32k_1[1]*2) + (dato32k_1[2]*4) + (dato32k_1[3]*8) + (dato32k_1[4]*16) + (dato32k_1[5]*32) + (dato32k_1[6]*64)
    valor_1_40k = (dato40k_1[0]*1) + (dato40k_1[1]*2) + (dato40k_1[2]*4) + (dato40k_1[3]*8) + (dato40k_1[4]*16) + (dato40k_1[5]*32) + (dato40k_1[6]*64)
    valor_1_49k = (dato49k_1[0]*1) + (dato49k_1[1]*2) + (dato49k_1[2]*4) + (dato49k_1[3]*8) + (dato49k_1[4]*16) + (dato49k_1[5]*32) + (dato49k_1[6]*64)
    valor_1_57k = (dato57k_1[0]*1) + (dato57k_1[1]*2) + (dato57k_1[2]*4) + (dato57k_1[3]*8) + (dato57k_1[4]*16) + (dato57k_1[5]*32) + (dato57k_1[6]*64)
    valor_1_65k = (dato65k_1[0]*1) + (dato65k_1[1]*2) + (dato65k_1[2]*4) + (dato65k_1[3]*8) + (dato65k_1[4]*16) + (dato65k_1[5]*32) + (dato65k_1[6]*64)
#  *** audio 2 ***
    valor_2_8k = (dato8k_2[0]*1) + (dato8k_2[1]*2) + (dato8k_2[2]*4) + (dato8k_2[3]*8) + (dato8k_2[4]*16) + (dato8k_2[5]*32) + (dato8k_2[6]*64) 
    valor_2_16k = (dato16k_2[0]*1) + (dato16k_2[1]*2) + (dato16k_2[2]*4) + (dato16k_2[3]*8) + (dato16k_2[4]*16) + (dato16k_2[5]*32) + (dato16k_2[6]*64) 
    valor_2_24k = (dato24k_2[0]*1) + (dato24k_2[1]*2) + (dato24k_2[2]*4) + (dato24k_2[3]*8) + (dato24k_2[4]*16) + (dato24k_2[5]*32) + (dato24k_2[6]*64)
    valor_2_32k = (dato32k_2[0]*1) + (dato32k_2[1]*2) + (dato32k_2[2]*4) + (dato32k_2[3]*8) + (dato32k_2[4]*16) + (dato32k_2[5]*32) + (dato32k_2[6]*64)
    valor_2_40k = (dato40k_2[0]*1) + (dato40k_2[1]*2) + (dato40k_2[2]*4) + (dato40k_2[3]*8) + (dato40k_2[4]*16) + (dato40k_2[5]*32) + (dato40k_2[6]*64)
    valor_2_49k = (dato49k_2[0]*1) + (dato49k_2[1]*2) + (dato49k_2[2]*4) + (dato49k_2[3]*8) + (dato49k_2[4]*16) + (dato49k_2[5]*32) + (dato49k_2[6]*64)
    valor_2_57k = (dato57k_2[0]*1) + (dato57k_2[1]*2) + (dato57k_2[2]*4) + (dato57k_2[3]*8) + (dato57k_2[4]*16) + (dato57k_2[5]*32) + (dato57k_2[6]*64)
    valor_2_65k = (dato65k_2[0]*1) + (dato65k_2[1]*2) + (dato65k_2[2]*4) + (dato65k_2[3]*8) + (dato65k_2[4]*16) + (dato65k_2[5]*32) + (dato65k_2[6]*64)
    
# *** Activacion de los leds y de los mosfets controlado por retardo ***
    hc595_shift(valor_1_8k)
    hc595_shift(valor_2_8k)
    TR8.value(1)
    time.sleep_us(retardo)
    TR8.value(0)
    
    hc595_shift(valor_1_16k)
    hc595_shift(valor_2_16k)
    TR7.value(1)
    time.sleep_us(retardo)
    TR7.value(0)
    
    hc595_shift(valor_1_24k)
    hc595_shift(valor_2_24k)
    TR6.value(1)
    time.sleep_us(retardo)
    TR6.value(0)
    
    hc595_shift(valor_1_32k)
    hc595_shift(valor_2_32k)
    TR5.value(1)
    time.sleep_us(retardo)
    TR5.value(0)
    
    hc595_shift(valor_1_40k)
    hc595_shift(valor_2_40k)
    TR4.value(1)
    time.sleep_us(retardo)
    TR4.value(0)
    
    hc595_shift(valor_1_49k)
    hc595_shift(valor_2_49k)
    TR3.value(1)
    time.sleep_us(retardo)
    TR3.value(0)
    
    hc595_shift(valor_1_57k)
    hc595_shift(valor_2_57k)
    TR2.value(1)
    time.sleep_us(retardo)
    TR2.value(0)
    
    hc595_shift(valor_1_65k)
    hc595_shift(valor_2_65k)
    TR1.value(1)
    time.sleep_us(retardo)
    TR1.value(0)

# *** SUBRUTINA BOTON 1 - PRUEBA LOS LEDS  ***
def button_one():
    if button1.value() == 1:
        time.sleep_ms(20)
        TR8.value(0)
        TR7.value(0)
        TR6.value(0)
        TR5.value(0)
        TR4.value(0)
        TR3.value(0)
        TR2.value(0)
        TR1.value(0)
        led_enplaca.value(1)
        time.sleep_ms(400)
        led_enplaca.value(0)
        time.sleep_ms(400)
        led_enplaca.value(1)
        time.sleep_ms(400)
        led_enplaca.value(0)
        hc595_shift(127)
        hc595_shift(127)
        TR1.value(1)
        time.sleep_ms(retardo_led)
        TR1.value(0)
        TR2.value(1)
        time.sleep_ms(retardo_led)
        TR2.value(0)
        TR3.value(1)
        time.sleep_ms(retardo_led)
        TR3.value(0)
        TR4.value(1)
        time.sleep_ms(retardo_led)
        TR4.value(0)
        TR5.value(1)
        time.sleep_ms(retardo_led)
        TR5.value(0)
        TR6.value(1)
        time.sleep_ms(retardo_led)
        TR6.value(0)
        TR7.value(1)
        time.sleep_ms(retardo_led)
        TR7.value(0)
        TR8.value(1)
        time.sleep_ms(retardo_led)
        TR8.value(0)
        TR1.value(0)
        TR2.value(1)
        time.sleep_ms(retardo_led)
        TR2.value(0)
        TR3.value(1)
        time.sleep_ms(retardo_led)
        TR3.value(0)
        TR4.value(1)
        time.sleep_ms(retardo_led)
        TR4.value(0)
        TR5.value(1)
        time.sleep_ms(retardo_led)
        TR5.value(0)
        TR6.value(1)
        time.sleep_ms(retardo_led)
        TR6.value(0)
        TR7.value(1)
        time.sleep_ms(retardo_led)
        TR7.value(0)
        TR8.value(1)
        time.sleep_ms(retardo_led)
        TR8.value(0)
        
      
# *** PROGRAMA PRINCIPAL ***
while True:
    button_one()
    LeerMSEGQ7()
   