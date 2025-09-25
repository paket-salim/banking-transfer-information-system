# Banking Transfer Information System

Учебный проект по курсу «Разработка информационных систем».  
Веб-приложение для осуществления переводов между банковскими счетами с поддержкой ролей пользователей.  

## Описание проекта

Приложение реализует функциональность перевода средств между счетами клиентов банка через веб-интерфейс.  
Система поддерживает четыре роли: клиент, операционист, аналитик и владелец банка.  
Реализованы авторизация, выполнение запросов по клиентам и счетам, формирование отчётов и перевод средств с учётом валютных курсов.  

## Стек технологий

- **Backend**: Python, Flask, MySQL  
- **Frontend**: HTML, CSS, Jinja2 Templates  
- **Инструменты**: PyCharm, MySQL Workbench, UML (Use Case, Class, Sequence diagrams)  

## Функционал

- Авторизация пользователей по ролям (client / operator / analyst / owner)  
- Работа с запросами:
  - Поиск клиентов по ФИО, дате рождения, адресу, телефону, дате заключения договора  
  - Получение информации о счетах и операциях  
- Работа с отчётами:
  - Формирование SQL-запросов через `reports.json` и вывод данных в интерфейсе  
- Переводы между счетами:
  - Проверка доступного остатка  
  - Конвертация валют по курсу банка на дату операции  
  - Запись в историю операций и журнал переводов  

## Структура проекта
- Banking-transfer-information-system/
  - blueprint_auth/ # Авторизация
    - sql
    - templates
    - auth.py
  - blueprint_query/ # Поисковые запросы по клиентам и счетам
    - sql
    - templates
    - query.py
  - blueprint_report/ # Формирование отчётов
    - sql
    - templates
    - report.py
  - blueprint_transfer/ # Логика переводов между счетами
    - sql
    - templates
    - transfer.py
  - DB/ # Работа с базой данных (подключение, SQL provider)
  - data_files/ # Конфиги
  - templates/ # Общие HTML-шаблоны (меню, формы)
  - static/ # Стили CSS
  - access.py # Регулирование доступа
  - main.py # Точка входа приложения
  - requirements.txt

## Структура базы данных
<img width="745" height="713" alt="erd" src="https://github.com/user-attachments/assets/418adfa3-78e3-4231-a6c6-d97e56f4a397" />

## Установка и запуск

### Предварительные требования
- Установленный **Python 3.11+**;  
- Установленный **MySQL Server**;
- Установленный **pip**.

### Настройка базы данных
1. Создайте базу данных MySQL, например `bank_transfer_db`;
2. Импортируйте таблицы вручную по схеме проекта;
3. Настройте файл `data_files/.db_config.json` на основе `data_files/.db_config_example.json`.  
   Пример:
```
// data_files/.db_config_example.json

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=bank_transfer_db
SECRET_KEY=your_secret_key
```

### Запуск приложения
```
// bash

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python main.py
```
Приложение будет доступно по адресу: http://localhost:5000/

## Скриншоты интерфейса
### Главная страница и меню авторизации
<img width="1851" height="995" alt="Снимок экрана 2025-09-25 214145" src="https://github.com/user-attachments/assets/713bcced-6517-475d-9e39-46e5f990bf80" />
<img width="1845" height="998" alt="Снимок экрана 2025-09-25 214222" src="https://github.com/user-attachments/assets/274f61f1-a9bd-4960-8d56-c008f1f61b21" />

---

### Интерфейс владельца
<img width="1848" height="995" alt="Снимок экрана 2025-09-25 214237" src="https://github.com/user-attachments/assets/49578d24-7e16-4b74-a355-eaed418d19f8" />
<img width="1845" height="993" alt="image" src="https://github.com/user-attachments/assets/43bb4b30-a011-4d52-a5e9-27970aeb3380" />

### Интерфейс операциониста
<img width="1846" height="1000" alt="image" src="https://github.com/user-attachments/assets/279eb807-c3f7-40d3-89ee-ce2e19b54a15" />
<img width="1840" height="993" alt="Снимок экрана 2025-09-25 215349" src="https://github.com/user-attachments/assets/e865866e-41fb-4f21-84a5-fb64177ebeb8" />
<img width="1846" height="996" alt="Снимок экрана 2025-09-25 215537" src="https://github.com/user-attachments/assets/54a9d44d-1aac-4b08-b229-2145a6e6c2e9" />
<img width="1845" height="995" alt="Снимок экрана 2025-09-25 215508" src="https://github.com/user-attachments/assets/0e08aecc-36e0-45f7-ab9c-8fbb572d3c18" />

### Интерфейс аналитика (поиск клиентов)
<img width="1853" height="995" alt="image" src="https://github.com/user-attachments/assets/071c05eb-d965-45b3-8954-6706c2ba7e81" />
<img width="1844" height="993" alt="Снимок экрана 2025-09-25 214503" src="https://github.com/user-attachments/assets/3810b2ad-d86d-4920-88ea-9eaebad146f0" />

### Интерфейс клиента (осуществление переводов)
<img width="1843" height="990" alt="Снимок экрана 2025-09-25 214804" src="https://github.com/user-attachments/assets/b7833305-fc02-4792-8e3f-f1ceb14bbb18" />
<img width="1841" height="998" alt="Снимок экрана 2025-09-25 214841" src="https://github.com/user-attachments/assets/3ac54c2e-f2fc-4e10-9055-5b809082663c" />
<img width="1844" height="995" alt="Снимок экрана 2025-09-25 214850" src="https://github.com/user-attachments/assets/8e6dfc29-cd05-4f0e-8e9b-8fc8fb991094" />

---
Автор

Проект выполнен в рамках учебного курса «Разработка информационных систем».
Автор: __paket-salim__

---
