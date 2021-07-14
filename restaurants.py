import pymongo

file = open('restaurants.json', 'r')

for i in range (10):
    data = file.readline()
    arr =  data.split(':')
    if '{"address"' in arr:
        print ('Name :', arr[arr.index('{"address"')+1])
