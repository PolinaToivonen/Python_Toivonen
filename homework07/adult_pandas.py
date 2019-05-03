import pandas as pd
import numpy as np

df = pd.read_csv('adult_data.csv')

print('1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?')
print(df['sex'].value_counts(), '\n')


print('2. Каков средний возраст (признак age) женщин?')
print(df[df['sex'] == ' Female']['age'].mean(), '\n')


print('3. Какова доля граждан Германии (признак native-country)?')
print(df['native-country'][df['native-country'] == ' Germany'].value_counts() / len(df), '\n')


print('4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех,\n',
      'кто получает более 50K в год (признак salary) и тех,\n',
      'кто получает менее 50K в год?')
print(df.groupby(['salary'])['age'].agg([np.mean, np.std]), '\n')


print('6. Правда ли, что люди, которые получают больше 50k,\n',
      'имеют как минимум высшее образование? (признак education –\n',
      'Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)')
print(df['education'][df['salary'] == '>50K'].value_counts(), '\n')


print('7. Выведите статистику возраста для каждой расы (признак race) и каждого пола.\n',
      'Используйте groupby и describe. Найдите таким\n',
      'образом максимальный возраст мужчин расы Amer-Indian-Eskimo.')
print(df.groupby(['sex', 'race'])['age'].describe(percentiles=[]), '\n')


print('8. Среди кого больше доля зарабатывающих много (>50K):\n',
      'среди женатых или холостых мужчин (признак marital-status)?\n',
      'Женатыми считаем тех, у кого marital-status начинается с Married\n',
      '(Married-civ-spouse, Married-spouse-absent или Married-AF-spouse),\n'
      'остальных считаем холостыми.')
print('Married  : ', df['marital-status'][df['marital-status'].str.startswith('Mar')]
      [df['sex'] == 'Male'][df['salary'] == '>50K'].value_counts().sum() / len(df))
print('Unmarried: ', df['marital-status'][df['marital-status'].str.endswith('d')]
      [df['sex'] == 'Male'][df['salary'] == '>50K'].value_counts().sum() / len(df), '\n')


print('9. Какое максимальное число часов человек работает в неделю\n'
      '(признак hours-per-week)? Сколько людей работают такое количество\n'
      'часов и каков среди них процент зарабатывающих много?')
print('Час  Человек', '\n',
      df['hours-per-week'][df['hours-per-week'] == df['hours-per-week'].max()].value_counts(), '\n',
      pd.crosstab(df['hours-per-week'][df['hours-per-week'] == df['hours-per-week'].max()],
                  df['salary'], normalize=True), '\n')


print('10. Посчитайте среднее время работы (hours-per-week) зарабатывающих\n',
      'мало и много (salary) для каждой страны (native-country).')
print(df.pivot_table(['hours-per-week'], ['native-country', 'salary'], aggfunc='mean')[43:53])
