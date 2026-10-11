import random
print ("ЧЕГО СКАЗАТЬ-ТО ХОТЕЛ, МИЛОК?!")
a=str(input())
k=0
running=True
end="ПОКА!"
while running:
    if a==end:
        k+=1
    else:
        k=0
    if k==3:
        break
    if a.upper()==a:
        print("НЕТ, НИ РАЗУ С",random.randint(1930,1950) ,"ГОДА")
        a=str(input())
    else:
        print("АСЬ?! ГОВОРИ ГРОМЧЕ, ВНУЧЕК!")
        a=str(input())
print("ДО СВИДАНИЯ, МИЛЫЙ!")

