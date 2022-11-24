# import re

with open("aclImdb/train/unsup/10_0.txt") as f:
    lines = f.readlines()

# split_string = re.split('[.]', lines[0])
split_string = lines[0].split(".")
print("The formatted output is below:\n")
for x in split_string:
    new_string = x.split("<br /><br />")
    print(new_string[0])
f.close()
