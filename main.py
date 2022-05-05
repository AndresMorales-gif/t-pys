from lpp.repl import start_repl


message = '''
  tttttt        tttttt tt  tt   tt  
  tttttt        tt  tt tt  tt tt  tt
    tt   tttttt tt  tt  tttt  tt   
    tt   tttttt tttttt   tt     tt 
    tt          tttttt   tt       tt 
    tt          tt       tt   tt  tt  
    tt          tt       tt     tt  
'''

def main() -> None:
  print('Welcome!!!')
  print(message)
  print('shell!!')

  start_repl()

if __name__ == '__main__':
  main()