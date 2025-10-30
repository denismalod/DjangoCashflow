# Django Cashflow Project

## Инструкции по запуску проекта

Для запуска этого проекта Django выполните следующие шаги:

1.  **Клонируйте репозиторий (если вы еще этого не сделали):**
    ```bash
    git clone https://github.com/denismalod/DjangoCashflow.git
    cd DjangoCashflow
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv .venv
    # Для Windows:
    .venv\Scripts\activate
    # Для macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Выполните миграции базы данных:**
    ```bash
    python cashflow/manage.py migrate
    ```

5.  **Создайте суперпользователя (по желанию, для доступа к админ-панели Django):**
    ```bash
    python cashflow/manage.py createsuperuser
    ```
    Следуйте инструкциям в терминале для создания пользователя.

6.  **Запустите сервер разработки:**
    ```bash
    python cashflow/manage.py runserver
    ```

7.  **Откройте проект в браузере:**
    После запуска сервера откройте ваш веб-браузер и перейдите по адресу:
    `http://127.0.0.1:8000/`

    Для доступа к админ-панели перейдите по адресу:
    `http://127.0.0.1:8000/admin/` (используйте учетные данные суперпользователя, созданные на шаге 5).
