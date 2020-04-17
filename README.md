# Кластеризация в рамках информационного поиска

Данный проект направлен на исследование кластеризации документов как задачи информационного поиска.

В качестве данных для обработки будут использованы курсы платформы Stepik

На **20.03.2020** подготовлен функционал загрузки информации о курсах, однако осталось ещё немного доработать его для получения полных сведений, необходимых для анализа

На **04.04.2020** доработана программа по скачиванию необходимых данных русскоязычных курсов более чем с 50 обучающимимся. Также скачаны такие данные. Вся информация доступна в архиве allRelevant.zip, в формате json

На **17.04.2020** выполнен стемминг (отсечение окончаний) полученных данных, их можно просмотреть в архиве *"stemmed.zip"*, затем была построена матрица "Частота термина - обратная частота в документе" для моно-, би- и триграмм, а на ней произведена пробная кластеризация четырьмя методами. Интерпретация данных позволит увидеть качество работы программы и принять решение об изменении параметров алгоритмов