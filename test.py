class Super:
 def hello(self):
  print("Olá, sou a superclasse!")
  
class Sub (Super):
 def hello(self):
  print("Olá, sou a subclasse!")

teste = Sub()
teste.hello()
