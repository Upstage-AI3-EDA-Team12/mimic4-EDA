import pandas as pd

df = pd.read_csv("./data/merged_data.csv", encoding='cp949')

df.drop(['흡연상태', '음주여부', '구강검진수검여부', '치아우식증유무', '치석'], axis=1, inplace=True)

new_columns = {'기준년도': 'year', '가입자일련번호': 'id', '시도코드': 'region', '성별': 'sex', '연령대코드(5세단위)': 'age', 
               '신장(5cm단위)': 'height', '체중(5kg단위)': 'weight', '허리둘레': 'waist', 
               '시력(좌)': 'sight(left)', '시력(우)': 'sight(right)', '청력(좌)': 'hearing(left)', '청력(우)': 'hearing(right)', 
               '수축기혈압': 'SBP', '이완기혈압': 'DBP', '식전혈당(공복혈당)': 'FBG', 
               '총콜레스테롤': 'TC', '트리글리세라이드': 'NF', 'HDL콜레스테롤': 'HDL', 'LDL콜레스테롤': 'LDL', 
               '혈색소': 'Hgb', '요단백': 'urine protein', '혈청크레아티닌': 'serum creatinine', 
               '혈청지오티(AST)': 'AST', '혈청지피티(ALT)': 'ALT', '감마지티피': 'GTP'}
df.rename(columns=new_columns, inplace=True)

df['sight(left)'].fillna(df['sight(right)'], inplace=True)
df['sight(right)'].fillna(df['sight(left)'], inplace=True)
df.dropna(subset=['sight(right)', 'sight(left)'], inplace=True)
df['sight'] = (df['sight(left)'] + df['sight(right)']) / 2
df.drop(['sight(left)', 'sight(right)'], axis=1, inplace=True)

df['hearing(left)'].fillna(df['hearing(right)'], inplace=True)
df['hearing(right)'].fillna(df['hearing(left)'], inplace=True)
df.dropna(subset=['hearing(right)', 'hearing(left)'], inplace=True)
df['hearing'] = (df['hearing(left)'] + df['hearing(right)']) / 2
df.drop(['hearing(left)', 'hearing(right)'], axis=1, inplace=True)

df.dropna(subset=['waist', 'SBP', 'DBP', 'FBG', 'Hgb', 'urine protein', 'serum creatinine', 'AST', 'ALT', 'GTP', 'TC', 'NF', 'HDL', 'LDL'], inplace=True)

df.to_csv("./data/preprocessed_data.csv", index=False)