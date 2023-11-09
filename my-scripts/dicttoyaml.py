import yaml


d = {"a":1, "b":[1,2,3,4], "c":[{"x":1000}, {"y":200}, {"z":{"a":0}}]}

result = yaml.dump(d)
print(result)


print(d["c"][2])

