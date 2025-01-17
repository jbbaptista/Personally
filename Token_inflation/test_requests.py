from tabulate import tabulate
table = [["Adelaide", 1295, 1158259, 600.5],
         ["Brisbane", 5905, 1857594, 1146.4],
         ["Darwin", 112, 120900, 1714.7],
         ["Hobart", 1357, 205556, 619.5],
         ["Sydney", 2058, 4336374, 1214.8],
         ["Melbourne", 1566, 3806092, 646.9],
         ["Perth", 5386, 1554769, 869.4]
        ]
headers = ["City name", "Area", "Population", "Annual Rainfall"]
print(tabulate([[row[0], row[1], "{:,}".format(row[2]), "{:,}".format(row[3])] for row in table], headers, floatfmt=".0f"))
