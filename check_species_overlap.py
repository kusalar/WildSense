import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://huggingface.co/wladradchenko/berkano.wladradchenko.ru/resolve/main/files/species_id_to_name.txt'
with urllib.request.urlopen(url) as res:
    lines = res.read().decode('utf-8').strip().split('\n')

model_species = [line.split(';')[1].strip('"').strip() for line in lines[1:] if ';' in line]

genera = ['Ocimum', 'Azadirachta', 'Nelumbo', 'Nymphaea', 'Hibiscus', 'Rosa', 'Ficus', 'Mangifera', 'Moringa', 'Tagetes', 'Jasminum', 'Bougainvillea', 'Catharanthus', 'Plumeria', 'Nerium', 'Solanum', 'Datura', 'Ricinus', 'Aloe', 'Mentha']

print("Genera presence:")
for g in genera:
    found = [m for m in model_species if g.lower() in m.lower().split()[0]]
    print(f"  {g}: {len(found)} species in model (e.g. {found[:2]})")
