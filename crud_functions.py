import sqlite3


def initiate_db():
    connection_DB = sqlite3.connect ( 'initiate.db' )
    cursor = connection_DB.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description   TEXT NOT NULL,
    price INTEGER 
    )
    '''
    )
    # индекс по названию и описанию
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON Products (title, description)")

    titles = ('MES2424', 'ESR-200', 'VP-30P-WB', 'MA4000-PX Eltex')
    descriptions = ('Ethernet-коммутатор MES2424, 24 порта 10/100/1000BASE-T, 4 порта 1000BASE-X/10GBASE-R, L3, 220В AC',
                  'ESR-200 FSTEC | Межсетевой экран Eltex 4 порта 1G, 4хcombo-порта 1G, Firewall Perfomance 0,9 Гбит/с, ФСТЭК А4',
                  'IP-телефоны для офиса. ЖК-дисплей и интегрированный гигабитный коммутатор. Качество звука обеспечивается объединением технологии HD Voice и голосового широкополосного кодека OPUS. Оснащена встроенными модулями Wi-Fi и Bluetooth.',
                   'Модульное OLT для построения узла GPON высокой плотности. Устанавливаются модули PLC8, PP4X. OLT поддерживает от 8 до 128 портов GPON.')
    prices = (15000, 219490, 5000, 378900) # Ценники не совсем отрытая информация, для данной работы этой информации достаточно

    for i in range(4):
        cursor.execute(" INSERT INTO Products (title,  description, price ) VALUES ( ?, ?, ?)", (titles[i], descriptions[i], prices[i] ))

    connection_DB.commit()
    connection_DB.close()

def get_all_products ():
    connection_DB = sqlite3.connect ( 'initiate.db' )
    cursor = connection_DB.cursor()
    cursor.execute('SELECT * FROM Products  ')
    rows = cursor.fetchall()

    connection_DB.commit()
    connection_DB.close()
    return rows
