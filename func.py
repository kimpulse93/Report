import pandas as pd
import matplotlib.pyplot as plt

# Количетво решенных  1 2 ЛП
def kol_resh_vden(df):
    ds1 = df[['Номер', 'Дата решения', 'ЛП']]
    # Создание сводной таблицы1
    krd = ds1.pivot_table(index='Дата решения', columns='ЛП', values='Номер', aggfunc='count')  # колво решенных на 1 2лп
    plt.figure(figsize=(20, 10))
    plt.plot(krd, color='green', marker='o', linestyle='--', markerfacecolor='blue')
    # plt.plot(krd, color='red', marker='o', linestyle='--', markerfacecolor='blue')
    x = 0
    for i in krd.values:
        plt.text(krd.index[x], i[0]+20.0, "%d" % i[0], ha="center")
        plt.text(krd.index[x], i[1] + 20.0, "%d" % i[1], ha="center")
        x = x + 1
    plt.title("Кол-во Решенных на 1,2 ЛП", fontsize=14, fontweight="bold")
    plt.xlabel("Дата решения", fontsize=14, fontweight="bold")
    plt.ylabel("Кол-во", fontsize=14, fontweight="bold")
    plt.grid(True)
    # Количетво решенных
    plt.savefig('krd.png')
    return krd


def kol_resh_klast(df):
    ds2 = df[['Номер', 'Группа поддержки', 'ЛП']]
    krk = ds2.pivot_table(index='Группа поддержки', columns='ЛП', values='Номер', aggfunc='count')
    krk.plot.bar(rot='horizontal', figsize=(20, 12 ))
    plt.xticks(rotation=90)
    plt.title("Кол-во Решенных в разрезе кластеров", fontsize=14, fontweight="bold")
    x = 0
    for i in krk.values.fillna(0):
        plt.text(krk.index[x], i[0]+20, "%d" % i[0], ha="center")
        plt.text(krk.index[x], i[1] + 20, "%d" % i[1], ha="center")
        x = x + 1
    plt.xlabel("Кол-во", fontsize=14, fontweight="bold")
    plt.ylabel("Кластер", fontsize=14, fontweight="bold")
    plt.savefig("krk.png", dpi=800)
    return krk


def kol_resh_vden_proc(df):
    x = 0
    ds1 = df[['Номер', 'Дата решения', 'ЛП']]
    krd = ds1.pivot_table(index='Дата решения', columns='ЛП', values='Номер',
                          aggfunc='count')  # колво решенных на 1 2лп
    a = krd
    a['3'] = a['1'] / (a['1'] + a['2']) * 100
    prd = a[['3']]
    plt.figure(figsize=(18, 7))
    plt.plot(prd, color='red', marker='o', linestyle='--', markerfacecolor='blue')
    plt.grid(True)
    plt.title("Ежедневный процент Решенных на 1ЛП", fontsize=14, fontweight="bold")
    plt.xlabel("Дата решения", fontsize=14, fontweight="bold")
    plt.ylabel("Процент", fontsize=14, fontweight="bold")
    for i in prd.values:
        plt.text(prd.index[x], i[0]+0.5, "%d" % i[0], ha="center")
        x = x + 1
    plt.savefig('prd.png')
    return prd


def kol_vozvr(df):
    ds3 = df[['Количество возвратов на доработку', 'Исполнитель', 'Номер', 'ЛП']]
    a = ds3.query('ЛП == "1"')
    s = a.pivot_table(index='Исполнитель', columns='Количество возвратов на доработку', values='Номер', aggfunc='count')
    print(s)
    ds4 = pd.DataFrame(s.to_records()).fillna(0)
    ds4['summa'] = ds4['1'] + ds4['2'] + ds4['3']
    d5 = ds4[['Исполнитель', 'summa']]
    print(d5)
    plt.show()
    return d5, ds4





