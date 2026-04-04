# RP-Hovorka - Fotaoparát©®™

Fotaoparát©®™ - Projekt protože mám zápal a málo ale i moc peněz.
Cíl je sestrojit fotoaparát, s rozhraním, volitelními funkcemi atd. atd. atd. 

## Obsah
- [Funkce](#funkce)
- [Hardware TODO před výrobou](#hardware-todo-před-výrobou)
  - [KRITICKÉ (musí být hotové)](#kritické-musí-být-hotové)
  - [DŮLEŽITÉ (doporučené)](#důležité-doporučené)
  - [NICE TO HAVE](#nice-to-have)
- [Double-check před odesláním](#double-check-před-odesláním)
  - [Hardware zapojení](#hardware-zapojení)
  - [Finální kontrola PCB](#finální-kontrola-pcb)
- [Komponenty](#komponenty)

---

## Funkce

- Programovatelná tlačítka
- Nastavení clony, iso a rychlosti závěrky
- display, možná i periferie (blesk, mikrofon, reprák?...)
- haha
- jak vtipný by bylo kdybych tam dal DOOM? [kdybych fakt jo chtěl](https://github.com/alexkid77/ESP32P4DOOM)
---

## 🔴 Hardware TODO před výrobou

### KRITICKÉ (musí být hotové):

- [✅] **I2C Pull-up rezistory pro kameru**
  - `I2C_SDA → 4.7kΩ → 3.3V`
  - `I2C_SCL → 4.7kΩ → 3.3V`
  - Pouzdro: 0402 nebo 0603
  - Umístění: blízko kamery nebo ESP32-P4

- [ ] **DC-DC měniče kontrola**
  - 7.2V → 3.3V (hlavní napájení)
  - 7.2V → 6V (objektiv motor)
  - 7.2V → 5.5V (objektiv logika)
  - Zkontrolovat: IC type, kondenzátory, feedback rezistory

- [ ] **Power supply piny ESP32-P4**
  - Všechny VDD piny zapojené?
  - Decoupling: 100nF u KAŽDÉHO VDD pinu (0402 nebo 0603)
  - 10µF na každých 4-5 VDD pinů (0603 nebo 0805)

- [✅] **Power button zapojení**
  - GPIO pin vybraný (libovolný volný GPIO)
  - 10kΩ pull-up k 3.3V
  - Software: Light Sleep mode

### DŮLEŽITÉ (doporučené):

- [ ] **SD karta ESD ochrana**
  - Díl: ESDA6V1-5SC6 (SOT-23-6)
  - Umístění: <5mm od SD konektoru
  - (volitelné, ale doporučené za ~$0.20)

- [✅] **Canon 550D tlačítka pinout**
  - Najít/změřit pinout flex kabelu
     -> mám, dvě silné cesty jsou A a K diody (katoda je na kraji ven), naproti je spol. vodič tlačítek
  - Určit zapojení (matice/analog ladder/samostatné GPIO)
      -> je to žebřík, yapojení už mám

- [ ] **Krytal předělat**
  -LSCS nemá ten krystal co jsem původně plánoval.
    resp. má ale jiný pinout, musím reroutovat
  
  ### NICE TO HAVE:

- [ ] **LEDky indikace stavu** (pokud zbyde místo) -> je jedna původní červená, možná jednu přidam
- [ ] **Test points** (3.3V, 7.2V, GND) - volitelné

---

## ✅ Double-check před odesláním

### Hardware zapojení:

- **Flash QSPI**
  - Správně zapojené, impedance OK

- **USB zapojení**
  - Ověřené + ESD ochrana (USBLC6-2SC6)

- **Strapping piny ESP32-P4**
  - Pull-up/down správně

- **Boot/Reset obvod**
  - Funkční

- **Kamera MIPI CSI-2 pinout** - 15-pin ověřený ✅
  - CSI_DATA_P0/N0, CSI_DATA_P1/N1
  - CSI_CLK_P/N
  - I2C_SDA/SCL (pin 11, 12)
  - 3.3V napájení (pin 14)
  - CAM_SHDN (pin 15)

- **Display MIPI DSI pinout** - 15-pin ověřený ✅
  - DSI_DATA_P0/N0, DSI_DATA_P1/N1
  - DSI_CLK_P/N
  - Touch I2C (TP_SDA/TP_SCL)
  - Backlight PWM

- **SD karta**
  - Zapojení hotové

- **Canon EF mount**
  - Kontakty vyřešené

- **Canon baterie 7.2V**
  - Konektor, ochrana proti přepólování

### Finální kontrola PCB:

- [ ] **Ground plane**
  - Solid GND pour na obou stranách

- [ ] **Power planes**
  - 3.3V plane (pokud je místo)

- [ ] **Mounting holes**
  - Pozice určena (z Canon 550D)

- [ ] **Konektory footprinty** - všechny správné
  - Kamera FPC 15-pin (Hirose FH12-22S-0.5SH?)
  - Display FPC 15-pin
  - SD karta
  - USB-C
  - Canon EF mount kontakty

- [ ] **Decoupling kondenzátory**
  - Všude kde mají být

- [ ] **Silkscreen popisky**
  - Jasné označení konektorů

---

## 📦 Komponenty

**MCU:** ESP32-P4

**Kamera:** Arducam IMX219 8MPx s objektivem M12 LS1820 (NOIR)

**Display:** Waveshare 2.8" DSI LCD (s touch)

**Baterie:** Canon 7.2V (z Canon EOS 550D)

**Objektiv:** Canon EF lens mount (z Canon EOS 550D)

**Tlačítka:** Z Canon EOS 550D

**DC-DC měniče:**
- 7.2V → 3.3V
- 7.2V → 6V (objektiv motor)
- 7.2V → 5.5V (objektiv logika)
- ESP32-P4 interní 1.8V LDO

**ESD ochrana:**
- USB: USBLC6-2SC6 (SOT-23-6)
- SD karta: ESDA6V1-5SC6 (SOT-23-6) - volitelné
