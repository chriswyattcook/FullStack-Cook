import requests
import json
import jsonify

pokemon_number=str(1)

url = 'http://pokeapi.co/api/v2/pokemon/'+pokemon_number

r = requests.get(url)

r.jsonify()

outfile = open('pokemon.json','w')

outfile.write(r)