import json

for i in range(1,203):
    fn = str(i) + ".json"
    f = open(fn, encoding="utf8")
    temp = json.load(f)
    f.close()
    
    json_object = json.dumps(temp)
    file_name =  str(i) + "-e.json"
    
    with open(file_name, "w") as outfile:
        outfile.write(json_object)