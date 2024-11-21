# Scadapy

Проект для работы с ModbusTCP.

## Конфигруация сервера

Приложение читает данные с Modbus-сервера по протоколу TCP. Конфигурация сервера задается в файле *modbus-config.yaml*.
Пример конфиг-файла:

```yaml
servers:
  - 502:
    - reg1:
        reg_addr: 0
        reg_type: "Float"

    - reg2:
        reg_addr: 2
        reg_type: "Float"

  - 503:
    - reg1:
        reg_addr: 0
        reg_type: "Float"
```
* `502, 503` - порты серверов;
* `reg1, reg2` - имена регистров;
* `reg_addr` - адрес регистра;
* `reg_type` - тип значений на данном регистре.

## Установка

```shell
git clone https://github.com/ddombrovskii/scadapy.git
cd scadapy
pip install -r requirements.txt
```

## Запуск
Старт приложения производится с помощью запуска файла `main.py`

```shell
python main.py
```

Протестировано на версии Python 3.10.
