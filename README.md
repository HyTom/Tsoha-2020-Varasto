### Tsoha-2020-Varasto
Tsoha-2020 loppukesän tietokantasovellus harjoitustyö

# Varastosovellus

Kuvitteellisen yrityksen sovellus jossa pidetään yllä tietoa siitä, mitä tavaraa yrityksellä löytyy varastosta ja mistä sen voisi löytää.


# Välipalautus 2 tilanne
Tuli ongelmia PostgreSQL:n kanssa ja vaihdoin windowsiin, vieläkin ongelmia mutta ainakin toimii.
Ohjelma vielä vasta rakentuu, kun koitan saada asioita toimimaan. 
Valitettavasti Heroku testausta ei vielä voi tehdä.+
/## Ominaisuuksia:
* Voi etsiä tavaraa.
* Voi lisätä ja poistaa tavaraa.
* Voi katsoa missä hyllyssä ja varastossa tavara sijaitsee.
* Tavaraa voi olla useammassa varastossa.
* Tavaraa voi siirtää varastojen välillä.
* Tuotteita voi tilata lisää.
* Sovellus on tietenkin tarkoitettu vain työntekijöille, joten sivuun tulee voida kirjautua.
* Kaikkia sivubisneksiä ei työntekijöiden tarvitse tietää, joten tietyt tunnukset eivät näe kaikkia tuotteita.
* Tieto tavaroiden lisäyksistä, poistoista ja liikkeistä olisi hyvä tallentaa omaan tauluun.
* Historiasta voisi myös katsoa, kuka käyttäjä muutoksen on tehnyt.