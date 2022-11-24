Поиск документов на cbr.ru

Программа ищет документы pdf на сайте https://www.cbr.ru.

Предусмотрена возможность запуска с разными браузерами (Сhrome, Firefox).

Для поиска элементов используется XPATH.


        Для атрибуты для запуска:
        --browser (firefox or chrome) - для выбора браузера. (browser=chrome default)
        --threads_count (цифра - число потоков) - для работы в несколько потоков. (threads_count=1 default)
        --method (selenium or requests) - для выбора метода поиска файлов. (threads_count=selenium default)
        --headless (true or false) - для режима графического интерфейса. (headless=True default)

        Пример запуска через Firefox в 2 потока c поддержкой графического интерфейса:

            python main.py --browser firefox --headless false --threads 4 --method selenium