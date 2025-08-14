# typing along with a youtube video
print("welcome to my computer game ")

playing = input("do you want to play?")

if playing != "yes":
    quit()

print("Okay lets play :)")

score = 0

answer = input("what does CPU stand for? ")
if answer.lower()== "central processing unit":
    print("Correct!")
score += 1

print("Incorrect")

answer = input("what does RAM stand for?")
if answer.lower() ==  "random access memory":
    print("Correct!")
    score += 1

else:
    print("Incorrect!")
answer = input("what does PSU stand for?")
if answer.lower() == "power supply":

    print("Correct!")
    score += 1
else:
    print("Incorrect! ")

print("you got " + str(score) + "questions correct!")
print("you got " + str(score/4 * 1) + " questions correct!")

#testing




