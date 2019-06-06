import json


def contains(list, filter) :
	for i in range(len(list)) :
		if filter(list[i]) : return i
	return None	


css = []
with open('colors.txt', 'r') as colorfile :
	css = json.load(colorfile)


colors = []



for cssRule in css :
	startindex = cssRule.find('rgb')
	limiter = 0
	while startindex >= 0 and limiter < 100 :
		i1 = cssRule.find('(', startindex)
		i2 = cssRule.find(')', startindex)
		colors.append({'color': cssRule[startindex:i2+1], 'count': 1})

		startindex = cssRule.find('rgb', startindex+1)
		limiter += 1


for i in range(len(colors)-1, -1, -1) :
	contain = contains(colors[0:i], lambda x: x['color'] == colors[i]['color'])
	if contain is not None :
		colors.pop(i)
		colors[contain]['count'] += 1


print(sorted(colors, key=lambda x: x['count'], reverse=True))
print(len(colors))
