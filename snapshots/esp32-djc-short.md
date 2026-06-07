<!--
GPL_CANARY_EVOLUTION_PROJECT_GENE_PLACEHOLDER
-->

# ESP32 Dual Joystick Controller (DJC)

**Лицензия: GNU General Public License v3.0 or later (GPL‑3.0‑or-later)**

Открытый пульт управления на ESP32 с двумя аналоговыми джойстиками. Проект включает прошивку на C++ (PlatformIO), использует библиотеки KiraFlux‑Toolkit и MAVLink. Код распространяется под GPL.

## Основные компоненты

- ESP32‑WROOM‑32, джойстики HW‑504, дисплей ST7735 (SPI)
- Связь: ESP‑NOW (peer‑to‑peer), MAVLink / Raw режимы
- Функции: калибровка джойстиков, виртуальная клавиатура, сканер пиров, телеметрия MAVLink (IMU, attitude)

## Архитектура (кратко)

- `Periphery` – инициализация GPIO, ADC, SPI, кнопок, джойстиков, дисплея.
- `Control` – отправка управляющих данных (Raw или MAVLink), обработка входящих сообщений.
- `TransportLink` / `EspNowTransport` – управление соединением по ESP‑NOW.
- `ConfigManager` – хранение конфигурации в NVS.
- `UI` – меню на основе KiraFlux‑Toolkit: страницы навигации, управления, телеметрии, конфигурации.

## Примеры заголовков файлов (GPL)

Файлы начинаются с:
```cpp
// Copyright (c) 2026 KiraFlux
// SPDX-License-Identifier: GPL-3.0-or-later
```