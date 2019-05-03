import pandas as pd
import numpy as np

data = pd.read_csv('data/adult.data.csv')

print('1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?')
print(data['sex'].value_counts(), '\n')


print('2. Каков средний возраст (признак age) женщин?')
print(data[data['sex'] == ' Female']['age'].mean(), '\n')


print('3. Какова доля граждан Германии (признак native-country)?')
print(data['native-country'][data['native-country'] == ' Germany'].value_counts() / len(data), '\n')


print('4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех,\n',
      'кто получает более 50K в год (признак salary) и тех,\n',
      'кто получает менее 50K в год?')
print(data.groupby(['salary'])['age'].agg([np.mean, np.std]), '\n')


print('6. Правда ли, что люди, которые получают больше 50k,\n',
      'имеют как минимум высшее образование? (признак education –\n',
      'Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)')
print(data['education'][data['salary'] == ' >50K'].value_counts(), '\n')


print('7. Выведите статистику возраста для каждой расы (признак race) и каждого пола.\n',
      'Используйте groupby и describe. Найдите таким\n',
      'образом максимальный возраст мужчин расы Amer-Indian-Eskimo.')
print(data.groupby(['sex', 'race'])['age'].describe(percentiles=[]), '\n')


print('8. Среди кого больше доля зарабатывающих много (>50K):\n',
      'среди женатых или холостых мужчин (признак marital-status)?\n',
      'Женатыми считаем тех, у кого marital-status начинается с Married\n',
      '(Married-civ-spouse, Married-spouse-absent или Married-AF-spouse),\n'
      'остальных считаем холостыми.')
print('Married  : ', data['marital-status'][data['marital-status'].str.startswith(' Mar')]
      [data['sex'] == ' Male'][data['salary'] == ' >50K'].value_counts().sum() / len(data))
print('Unmarried: ', data['marital-status'][data['marital-status'].str.endswith('d')]
      [data['sex'] == ' Male'][data['salary'] == ' >50K'].value_counts().sum() / len(data), '\n')


print('9. Какое максимальное число часов человек работает в неделю\n'
      '(признак hours-per-week)? Сколько людей работают такое количество\n'
      'часов и каков среди них процент зарабатывающих много?')
print('Час  Человек', '\n',
      data['hours-per-week'][data['hours-per-week'] == data['hours-per-week'].max()].value_counts(), '\n',
      pd.crosstab(data['hours-per-week'][data['hours-per-week'] == data['hours-per-week'].max()],
                  data['salary'], normalize=True), '\n')


print('10. Посчитайте среднее время работы (hours-per-week) зарабатывающих\n',
      'мало и много (salary) для каждой страны (native-country).')
print(data.pivot_table(['hours-per-week'], ['native-country', 'salary'], aggfunc='mean')[43:53])
