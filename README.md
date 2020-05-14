# Кластеризация в рамках информационного поиска

Данный проект направлен на исследование кластеризации документов как задачи информационного поиска.

В качестве данных для обработки будут использованы курсы платформы Stepik

На **20.03.2020** подготовлен функционал загрузки информации о курсах, однако осталось ещё немного доработать его для получения полных сведений, необходимых для анализа

На **04.04.2020** доработана программа по скачиванию необходимых данных русскоязычных курсов более чем с 50 обучающимимся. Также скачаны такие данные. Вся информация доступна в архиве allRelevant.zip, в формате json

На **17.04.2020** выполнен стемминг (отсечение окончаний) полученных данных, их можно просмотреть в архиве *"stemmed.zip"*, затем была построена матрица "Частота термина - обратная частота в документе" для моно-, би- и триграмм, а на ней произведена пробная кластеризация четырьмя методами. Интерпретация данных позволит увидеть качество работы программы и принять решение об изменении параметров алгоритмов

К **14.05.2020** завершено написание программного кода. Можно посмотреть результаты кластеризации на графике. Однако, библиотека *matplotlib*, к сожалению, не предоставляет удобного API для вывода описания точек по наведению мыши. Поэтому для просмотра наименований документов необходимо раскомментировать строки в файле *visual.py*, получив вывод всех названий сразу. Выглядит страшно, но зато можно оценить результат. Наиболее удовлетворительный результат был получен для 5 кластеров по биграммам с максимальной df (document frequency) = 0.5 и минимальной 0.005 для словаря длины 10000. Удалось заметить, что кластеризация произошла по таким категориям, как "Информационные технологии и программирование", "Олимпиады", "Языки", "Курсы для школы" и все остальные. Перехожу к написанию пояснительной записки, дальнейшие наработки буду проводить после сессии.
