import numpy
from matplotlib import pyplot
from scipy.stats import pearsonr, spearmanr

# Create random data
data1 = 20 * numpy.random.randn(1000) + 100
data2 = data1 + (10 * numpy.random.randn(1000) + 50)

print('data1: mean=%.3f stdv=%.3f' % (numpy.mean(data1), numpy.std(data1)))
print('data2: mean=%.3f stdv=%.3f' % (numpy.mean(data2), numpy.std(data2)))

# Visualize data in graph
pyplot.scatter(data1,data2)
pyplot.show()

# Covariance
covariance = numpy.cov(data1, data2)
print(covariance)

'''
Entre -1 a 1
Zero -> Uncorrelated 
Positivo -> correlação positiva 
Negativo -> correlação negativa 
'''

# Pearson model
corr1, _ = pearsonr(data1,data2)
print('Pearsons correlation: %.3f' % corr1)

# Spearman model
corr2, _ = spearmanr(data1, data2)
print('Spearmans correlation: %.3f' % corr2)




