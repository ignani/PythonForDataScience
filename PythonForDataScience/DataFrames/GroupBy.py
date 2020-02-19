# Sort, GroupBy, Remove Duplicates

import pandas as pd
import numpy as np

df = pd.DataFrame([('falcon', 'bird', 'Falconiformes', 389.0),
                    ('parrot', 'bird', 'Psittaciformes', 24.0),
                    ('lion', 'mammal', 'Carnivora', 80.2),
                    ('monkey', 'mammal', 'Primates', np.nan),
                    ('leopard', 'mammal', 'Carnivora', 58),
                   ('leopard', 'mammal', 'Carnivora', 59)],
                   columns=('name','class', 'order', 'max_speed'))

# Sort on the column name
df.sort_values('name', inplace = True)

# remove duplicates
df1 = df.drop_duplicates(subset ="name", keep = 'first')
grouped = df.groupby('class')
grouped.sum()