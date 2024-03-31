f = open("textfile.txt", "r")
lines = f.readlines()
lines.sort()
 
last = None
unique = []

counter = 0
for i, line in enumerate(lines):
    current_unique = 0
    
    line = line.strip()
    if i != 0:
        if line and  line != lines[i-1]:
            current_unique += 1
            
            counter = 1
            unique.append({"word": line, "total": counter})
        else:
            counter += 1
            unique[current_unique]['total'] = counter
    else:
        counter = 1
        unique.append({"word": line, "total": counter})
             
         
     
     
print(str(unique))
 
 
# f
# 
# pets = [
#     {'name': 'Max', 'age': 8},
#         {'name': 'Daisy', 'age': 3},
#     {'name': 'Milo', 'age': 5},
# ]
# 
# pets.sort(key=lambda x: x['age'])
# print(str(pets))
# 
# def log(func):
#     def wrapper():
#         print("beofre.")
#         func()
#         print("after.")
#     return wrapper