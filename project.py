import os
import json

class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
        self.file_path='dir_price'


    def load_prices(self):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        file_n = 0
        lines_n = 0
        for file_name in os.listdir(self.file_path):
            if 'price' in file_name:
                file_n += 1
                print('Файл с прайсом', file_name)
                with open(os.path.join(self.file_path, file_name), 'r', encoding='utf-8') as ff:
                    header = ff.readline()
                    prod_name_num, price_num, weight_num = self._search_product_price_weight(header)
                    file_data = ff.readlines()
                    for line in file_data:
                        lines_n += 1
                        line_data = line.split(',')
                        prod_name = line_data[prod_name_num].strip().lower()
                        if len(prod_name) > self.name_length:
                            self.name_length = len(prod_name)
                        price = int(line_data[price_num].strip())
                        weight = int(line_data[weight_num].strip())
                        cost = round(price / weight, 2)
                        self.data.append((cost, prod_name, price, weight, file_name))
        self.data.sort()
        return f'обработано файлов:  {file_n}, Всего позиций:  {lines_n}'
    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        data = headers.lower().strip().split(',')
        for ind in range(len(data)):
            if data[ind] in ('товар', 'название', 'продукт', 'наименование'):
                prod_name_num = ind
            if data[ind] in ('розница', 'цена'):
                price_num = ind
            if data[ind] in ('вес', 'масса', 'фасовка'):
                weight_num = ind
        return prod_name_num, price_num, weight_num

    def export_to_html(self):
        f_name = (os.path.join(self.file_path,'output.html'))
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Цена за кг.</th>
                    <th>Файл</th>
                    </tr>
        '''
        for number, item in enumerate(self.data):
            cost, product_name, price, weight, file_name = item
            result += '<tr>'
            result += f'<td>{number + 1}</td>'
            result += f'<td>{product_name}</td>'
            result += f'<td>{price}</td>'
            result += f'<td>{weight}</td>'
            result += f'<td>{cost}</td>'
            result += f'<td>{file_name}</td>'
            result += '</tr>\n'
        result += '</tbody>'
        result += '</table>'
        with open(f_name, 'w') as f:
            f.write(result)
        return f'HTML файл успешно создан: {f_name}'

    def find_text(self, text):
        text = text.lower()
        data = [item for item in self.data if text in item[1]]
        data.sort()
        return data

pm = PriceMachine()
print(pm.load_prices())

try:
    while True:
        fr = input("Введите фрагмент наименования товара для поиска (или 'exit' для выхода): ")
        if fr == 'exit':
            break
        else:
            result = pm.find_text(fr)
            if result:
                print("Результаты поиска:")
                print(
                    f'{"№": <4}  {"Наименование": <{pm.name_length}} {"цена":^6} {"вес":^4} {"цена за кг.":^12} {"файл"}')
                for idx, item in enumerate(result):
                    print(
                        f'{idx + 1: <4}  {item[1]: <{pm.name_length}} {item[2]:^5}  {item[3]:^4} {item[0]:^12} {item[4]}')
            else:
                print("Нет результатов по вашему запросу.")
                print(f"Вы искали: {fr}")

except Exception as e:
    print(f"Произошла ошибка: {e}")

print("Работа завершена.")
print(pm.export_to_html())

'''
добавить в условие "цена за кг и сортировка"
развитие задания: 
'''