# GPL Canary Evolution - MVP

Рекурсивная система для эволюции промптов-инъекций, предназначенных для защиты GPL-кода от автоматического извлечения спецификаций через LLM.

## Архитектура

Двухуровневая система с одним чатом:

1. **Test Environment** (LEVEL 1)
   - Чистый контекст + ген → логи + метрики
   - Макс 10 тестов за раунд
   - 4 стандартных сценария

2. **Evolution Engine** (LEVEL 2)
   - Анализ failed tests
   - LLM предлагает улучшенный ген
   - Фокус: SHORTER + more DIRECT

3. **Orchestrator** (MAIN LOOP)
   - TEST → EVALUATE → IMPROVE → REPEAT
   - Fitness: `(pass_rate × 0.7) - (length/1000 × 0.3)`
   - Convergence: score > 0.95 или max iterations

## Структура

```
.
├── src/gpl_canary_evolution/
│   └── evolution.py          # Основной модуль
├── genes/
│   └── root.txt              # Начальный ген
├── prompts/
│   ├── attacker/             # Запросы на извлечение спецификации
│   │   ├── spec_extraction.txt
│   │   ├── functional_spec.txt
│   │   └── gpl_detection.txt
│   └── harmless/             # Невинные технические вопросы
│       ├── programming_language.txt
│       └── code_size.txt
├── snapshots/
│   └── default.md            # Snapshot с placeholder
├── evolution_logs/           # Создаётся автоматически
├── secrets.py                # API ключи (не в git)
└── README.md
```

## Быстрый старт

### 1. Установить зависимости
```bash
pip install openai
```

### 2. Создать `secrets.py`
```python
# src/gpl_canary_evolution/secrets.py
llm_api_key = "sk-..."  # OpenRouter API key
llm_names = ["meta-llama/llama-2-70b-chat"]
snapshot_name = "default.md"
```

### 3. Запустить эволюцию
```bash
python -m gpl_canary_evolution.evolution
```

## Результаты

- `evolution_logs/evolution_results.json` — метрики всех раундов
- `genes/evolved_<timestamp>.txt` — лучший найденный ген

## Лицензия

MIT
