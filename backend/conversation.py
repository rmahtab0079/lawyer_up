bot  = []
person = []

i = 0
test = ""
while test != "finished":
    if i % 2 == 0:
        test = input("bot chat: ")
        bot.append(test)
    else:
        test = input("person chat: ")
        person.append(test)
    i += 1

print(person)
print(bot)