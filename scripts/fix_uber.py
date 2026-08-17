from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = "const map=q=>'https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(q),uber=q=>'uber://?action=setPickup&pickup=my_location&dropoff%5Bnickname%5D='+encodeURIComponent(q)+'&dropoff%5Bformatted_address%5D='+encodeURIComponent(q);"

new = r'''const map=q=>'https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(q);
const uberDest={
'Meliá Lisboa Oriente Lisbon':[38.76927,-9.09842,'Meliá Lisboa Oriente','Av. D. João II 31, 1990-083 Lisboa, Portugal'],
'Parque das Nações Lisbon':[38.76820,-9.09550,'Parque das Nações','Parque das Nações, Lisboa, Portugal'],
'Praça do Comércio Lisbon':[38.70775,-9.13659,'Praça do Comércio','Praça do Comércio, 1100-148 Lisboa, Portugal'],
'Lupita Lisbon':[38.70672,-9.14534,'Lupita Pizzaria','Rua de São Paulo 79, 1200-427 Lisboa, Portugal'],
'Cerâmicas na Linha Lisbon':[38.71016,-9.14249,'Cerâmicas na Linha','Rua Capelo 16, 1200-087 Lisboa, Portugal'],
'Miradouro de Santa Luzia Lisbon':[38.71174,-9.13022,'Miradouro de Santa Luzia','Largo de Santa Luzia, 1100-487 Lisboa, Portugal'],
'Miradouro da Senhora do Monte Lisbon':[38.71916,-9.13268,'Miradouro da Senhora do Monte','Largo Monte, 1170-253 Lisboa, Portugal'],
'Rosa da Rua Lisbon':[38.71468,-9.14600,'Rosa da Rua','Rua da Rosa 265, 1200-385 Lisboa, Portugal'],
'Porto Campanhã Station':[41.14871,-8.58530,'Porto Campanhã','Rua de Pinheiro de Campanhã, Porto, Portugal'],
'Porto Cathedral':[41.14282,-8.61120,'Porto Cathedral','Terreiro da Sé, 4050-573 Porto, Portugal'],
'Jardim do Morro Porto':[41.13732,-8.60928,'Jardim do Morro','Jardim do Morro, Vila Nova de Gaia, Portugal'],
'daTerra Baixa Porto':[41.14376,-8.61158,'daTerra Baixa','Rua de Mouzinho da Silveira 249, 4050-421 Porto, Portugal'],
'Ribeira Porto':[41.14063,-8.61104,'Ribeira','Praça da Ribeira, Porto, Portugal'],
'São Bento Station Porto':[41.14557,-8.61034,'São Bento Station','Praça de Almeida Garrett, 4000-069 Porto, Portugal'],
'Sintra Station Portugal':[38.79932,-9.38508,'Sintra Station','Av. Dr. Miguel Bombarda, 2710-590 Sintra, Portugal'],
'Monserrate Palace Sintra':[38.79384,-9.42065,'Park and Palace of Monserrate','Rua Barbosa du Bocage 136, 2710-405 Sintra, Portugal'],
"Piadina's Wine & Co Sintra":[38.79765,-9.39093,"Piadina's Wine & Co",'Rua da Ferraria 7, 2710-555 Sintra, Portugal'],
'Quinta da Regaleira Sintra':[38.79650,-9.39690,'Quinta da Regaleira','Rua Barbosa du Bocage 5, 2710-567 Sintra, Portugal'],
'Casa Piriquita Sintra':[38.79738,-9.39074,'Casa Piriquita','Rua Padarias 1, 2710-603 Sintra, Portugal'],
'MAAT Museum Lisbon':[38.69580,-9.19420,'MAAT','Av. Brasília, 1300-598 Lisboa, Portugal'],
'Pastéis de Belém Lisbon':[38.69750,-9.20320,'Pastéis de Belém','Rua de Belém 84, 1300-085 Lisboa, Portugal'],
'Jerónimos Monastery Lisbon':[38.69786,-9.20649,'Jerónimos Monastery','Praça do Império, 1400-206 Lisboa, Portugal'],
'Lisbon Cruise Terminal':[38.71280,-9.12670,'Lisbon Cruise Terminal','Doca Jardim do Tabaco, Av. Infante Dom Henrique, 1100-651 Lisboa, Portugal'],
'Silver Muse':[38.71280,-9.12670,'Lisbon Cruise Terminal','Doca Jardim do Tabaco, Av. Infante Dom Henrique, 1100-651 Lisboa, Portugal']
};
function uber(q){
 const d=uberDest[q]||[null,null,q,q];
 let u='uber://riderequest?pickup=my_location';
 if(d[0]!=null&&d[1]!=null) u+='&dropoff%5Blatitude%5D='+d[0]+'&dropoff%5Blongitude%5D='+d[1];
 u+='&dropoff%5Bnickname%5D='+encodeURIComponent(d[2])+'&dropoff%5Bformatted_address%5D='+encodeURIComponent(d[3]);
 return u;
}'''

if old not in s:
    raise SystemExit('Expected v28 Uber helper not found')

s = s.replace(old, new, 1)
s = s.replace('content="v28-uber-native-riderequest"', 'content="v29-uber-riderequest-coordinates"', 1)
s = s.replace('class="uber" target="_blank" href="${uber(x[6])}"', 'class="uber" href="${uber(x[6])}"')

assert 'uber://riderequest?pickup=my_location' in s
assert 'dropoff%5Blatitude%5D' in s
assert 'dropoff%5Bformatted_address%5D' in s
p.write_text(s)
