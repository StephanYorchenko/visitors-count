# visitors-count

Счётчик посещений

Запуск счётчика:

    (env) ~/proj_folder $ python app.py 

Запуск тестовых страниц /test_page1 и /test_page2

    ~/proj_folder/templates $python3 -m http.server или другим аналогичным способом

----

Проверка количества посещений: ```http://<addr_of_server_with_counter>/get_count?id=<page_id>&period=[today|28d|all]``` - получить число посещений страницы по её идентификатору.

Ответ приходит в формате json: ```{'all': int, 'unique': int}```

По умолчанию, отдаётся статистика за последние 24 часа, 28 дней и за всё время одновременно (6 чисел)

Если не указан id, то сервер ваозвращает 404

Если указан неверный period, то сервер возвращает 400

-----

```<img src="http://<addr_of_server_with_counter>/update_count?id=<id>" alt="">``` - необходимо вставить на страницу, посещения которой хотим посчитать.
Например, ```<img src="http://0.0.0.0:8080/update_count?id=1" alt="""```

----

```<img src="http://0.0.0.0:8080/get_image?id=1" title="Показано количество посещений и  количество уникальных посещений за последние 24 часа" alt="" border="0">``` - позволяет разместить на сайте каринку со статистикой за последние 24 часа.

----

* Класс для работы с базой данных, в которой сохраняются данные счётчика
* Подсчёт уникальных и неуникальных посещений
* Возможность получить данные о посещениях за последний день, 28 дней и всего
* Тесты на логику приложения
* Картинка с цифрами посещения за последние 24 часа




Юрченко Степан ФТ-201
