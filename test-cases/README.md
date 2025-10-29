# 📋 Casos de Prueba - Project Automation CF

## 🔗 Google Sheet (Fuente única de verdad)

https://docs.google.com/spreadsheets/d/1edGFYzfhE9EyjqVpDxS6mDWzh30CBfRi0SVHn3WQDF4/edit?gid=869932423#gid=869932423

## 📊 Cobertura

Total casos: 34
Automatizados: 34 (100%)

## ▶️ Ejecutar tests
```bash
# Ejecutar un caso específico
pytest -m TC_API_01 -v

# Ejecutar por prioridad
pytest -m high -v

# Ejecutar por módulo
pytest -m auth -v
```