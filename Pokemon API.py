import requests

class pokemon_info:
    def __init__(self,name):
        self.name=name
        self.url=f"https://pokeapi.co/api/v2/pokemon/{self.name}/"
        self.response=(requests.get(self.url))
        self.data=self.response.json()

    def get_info(self):
       
        if (self.response.status_code==200):
            # print((requests.get(self.url).json()))
            print(f"Name:{self.data['name']}")
            print(f"ID:{self.data['id']}")
            print(f"Height:{self.data['height']}")
            print(f"Type:{self.data['types'][0]['type']['name']}")
            for a in self.data['abilities']:
                print(f"Ability:{a['ability']['name']}")
        else:
            print(f"Error:{self.response.status_code}")


p1=pokemon_info("pikachu")
p1.get_info()
p2=pokemon_info("squirtle")
p2.get_info()




        

        
    


