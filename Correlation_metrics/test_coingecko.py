import seaborn as sb
from matplotlib import pyplot as plt
import random

'''
Test
'''

# Create random lists , B dependent from A

a = list()
b = list()

for i in range(100):
    value = random.random()*(random.random()*100)
    a.append(value)

    if value < 20:
        value_1 = value/5
    elif value >20 and value < 75:
        value_1 = value/10
    else:
        value_1 = value/100

    b.append(value_1)

print(a)
print('')
print(b)

sb.regplot(a, b, x="a", y="b")
plt.show()
