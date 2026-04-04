# Core firmware

Cíl: výkonově citlivá vrstva běžící na ESP32-P4.

## Odpovědnosti
- inicializace kamery, displeje, SD karty a EF rozhraní
- čtení tlačítek a vstupů
- live view a snímání fotek
- ukládání snímků na SD
- řízení napájení a sleep režimů
- chybové stavy a recovery

## Hlavní moduly
- `camera`
- `display`
- `storage`
- `input`
- `power`
- `ef_mount`
- `system`

## Tok spuštění
1. boot
2. hardware init
3. load settings
4. start camera pipeline
5. start UI
6. enter event loop

## Důležité poznámky
- tento program má být napsaný v C/C++ nad ESP-IDF
- obrazová cesta nesmí jít přes interpret
- GUI může používat LVGL
