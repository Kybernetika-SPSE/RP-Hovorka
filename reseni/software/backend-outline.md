# Backend

Cíl: lehká řídicí vrstva nad core firmwarem.

## Odpovědnosti
- správa stavů zařízení
- logika režimů focení
- obsluha tlačítek a akcí uživatele
- nastavení ISO, clony, času a dalších voleb
- komunikace mezi GUI a hardwarem
- ukládání konfigurace
- jednoduché debug nebo servisní API

## Hlavní moduly
- `state_machine`
- `settings`
- `input_router`
- `capture_controller`
- `lens_controller`
- `ui_commands`

## Typický tok
1. přijde vstup z tlačítka nebo UI
2. backend vyhodnotí akci
3. pošle příkaz do core vrstvy
4. core provede hardware operaci
5. backend dostane výsledek a aktualizuje stav

## Co sem nepatří
- obrazový pipeline
- preview z kamery
- těžké grafické kreslení
- nízkoúrovňové DMA a timing kritické věci

## Poznámka
- backend může být později rozšířen o velmi lehké skriptování nebo servisní rozhraní, ale ne jako hlavní běhové jádro fotoaparátu
