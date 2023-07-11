Mus='1996'
Yas=2023-int(Mus)
print(Yas)

r1=5
r2=6
cevre =2*r1*3.14
alan =r1**2
print('cevre: '  ,cevre)
print("alan" ,alan)

# bu işlem string dizisi ile ilgili 

name1="Asiye"
name2="Rümeysa"
print("My name is {} {}".format(name1,name2))
r=15200/700 
print("Sonuc {r3: .3}".format(r3=r)) #float ifadesinin virgülden sonrası için kullanılır 
result =name1[::-1]  #dizini tersten yazmak için kullanılır
print(result)


#tuple verisii 


#dictionary#


sehirler =['kocaeli','istanbul']
plakalar =[41,34]

print(plakalar[sehirler.index(('kocaeli'))])


# Tuple ve Liste farkı 
'''
Tuple ('','') gibi 
Liste ise ['','']
Tuple listesinde listeyi baştan yazabiliriz ancak ama içine atama yapamayız silmede yapamayız
Listede ise bunu yapabiliriz

'''
Tuple=('Asiye','Rümeysa',26)
print(Tuple)

'''
Dictionary 

key value şekilindeki listeler 
{'key' : value} şeklinde ilerler  
'''

sehir ={'Kocaeli':41, 'Ankara': 6,  }
sehir['İstanbul']=34
print(sehir['Kocaeli'])

###


'''
 Value Reference Types 
 
 *Listesi üzerinde bir eşitleme yapıldıktan sonra ki liste aynı adrese yazılır,
    birinin üzerinde yapılan bir değişiklik direk diğerini etkiler.
'''
l= ["asiye","rumeysa"]
k = ['unsal','rumeysa']
l=k

l[0]="Sabun"
print(k)
# liste values arası ilişki 
values =1,2,3
print(values)
x,y,z=values
print(x,y,z)

deg = 1,2 ,3 ,4 ,5 ,6 
o,p, *t=deg
print(o,p,t)
