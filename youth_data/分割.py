import json

filepath = 'youth_xxm.json'

with open(filepath,'r') as f:
	data = json.loads(f.read())

# print(data[0])
# print(len(data))


d = dict()

d['A'] = data[:100]
d['B'] = data[100:200]
d['C'] = data[200:-1]
# d['D'] = data[100:150]
# d['E'] = data[150:200]
# d['F'] = data[200:-1]

savepath = filepath.split(".")[0]
for key ,value in d.items():
	path  = savepath + "_" + str(key) + ".json"
	with open(path,'w') as f:
		json.dump(value,f)
print('ok')