import numpy as np

AList = np.random.normal(10.0, 5.0, 25)
AList

listOfNums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for number in listOfNums:
    print(number)
    if number % 2 == 0:
        print("is even")
    else:
        print("is odd")

listOfNums[:4]  # List from beginning to 4. This will not list the item in index 4. Since it starts from 0, it will list total 4 items, that is till 3 (included)
listOfNums[2:4]  # Lists items 2 & 3
listOfNums[5:]  # Lists everthing from 5th item till the end
listOfNums[-2:]  # from the end 2 items

listOfNums.extend([11, 12, 13, 14])
listOfNums.append([15, 16])  # if we need to add multiple items, then use extend. This adds a list at the end

# If we call the len function, it wil print 15, while we have numbers till 16. This is because, 15 & 16 are part of a sub list within the list.
# The 14th item is a list, while the rest are of type int.
# This is because, append only accepts 1 item, for appending multiple items, use extend.
len(listOfNums)

