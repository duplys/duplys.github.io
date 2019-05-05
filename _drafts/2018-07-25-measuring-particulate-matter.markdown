---
layout: post
title:  "Particulate Matter!"
date:   2018-07-08 21:46:03 +0200
categories: raspi python physics
---

# Inspiration
My inspiration to experiment with the Nova SDS-011 sensor to measure particulate matter came after reading the article "Feinstaubmessung mit dem Raspberry-Pi" by Charly K\"uhnast in the german Linux Magazine, issue 06/18 (page 20). 


# Particulate Matter
Particulate matter (PM), also known as particle pollution, is a complex mixture of extremely small particles and liquid droplets that get into the air [2]. It is the sum of all solid and liquid particles suspended in air many of which are hazardous [3]. This complex mixture includes both organic and inorganic particles, such as dust, pollen, soot, smoke, and liquid droplets. These particles vary greatly in size, composition, and origin [3], and have impact on climate and and the human health [1].

Particle pollution includes inhalable particles with a diameter of $$\leq$$ 10 micrometers (PM10), and fine inhalable particles with a diameters of $$\leq$$ 2.5 micrometers (PM2.5) [3]. 

According to this [Wikipedia article](https://en.wikipedia.org/wiki/Particulates), the [International Agency for Research on Cancer](http://www.iarc.fr) and the [World Health Organization](http://www.who.int) designate airborne particulates a Group 1 carcinogen. Particulates are the deadliest form of air pollution[citation needed] due to their ability to penetrate deep into the lungs and blood streams unfiltered, causing permanent DNA mutations, heart attacks, and premature death [1]. In 2013, a study involving 312,944 people in nine European countries revealed that there was no safe level of particulates and that for every increase of 10 $$\mu g / m^3$$ in PM10, the lung cancer rate rose 22%. The smaller PM2.5 were particularly deadly, with a 36% increase in lung cancer per 10 $$\mu g / m^3$$ as it can penetrate deeper into the lungs [1].

Some particulates occur naturally, originating from volcanoes, dust storms, forest and grassland fires, living vegetation, and sea spray [1]. Human activities, such as the burning of fossil fuels in vehicles, power plants and various industrial processes, also generate significant amounts of particulates. Coal combustion in developing countries is the primary method for heating homes and supplying energy. Because salt spray over the oceans is the overwhelmingly most common form of particulate in the atmosphere, anthropogenic aerosols—those made by human activities—currently account for about 10 percent of the total mass of aerosols in our atmosphere [1].

[1]: https://en.wikipedia.org/wiki/Particulates
[2]: https://www.epa.gov/pm-pollution
[3]: https://www.greenfacts.org/en/particulate-matter-pm/level-2/01-presentation.htm

## Situation in Deutschland

Hauptverursacher des anthropogenen Anteils am Feinstaub in Deutschland waren um 2001 (laut Bundesumweltministerium und ergänzenden Quellen):

    Wirtschaft: 74.000 t/Jahr
        Industrie: 60.000 t/Jahr
        Schüttgutumschlag: 8.000 t/Jahr
        Industriefeuerungen: 6.000 t/Jahr

    Verkehr: 64.000 t/Jahr
        Straßenverkehr: 42.000 t/Jahr
            Abgase der
                Otto-Motoren (siehe Direkteinspritzung bei Ottomotoren)
                Diesel-Motoren (siehe: Dieselruß): 29.000 t/Jahr
            Abrieb von
                Fahrzeugkatalysatoren
                Antriebssystemen (Kardanwellen, Dichtungen, Getrieben)
                Bremssystemen, Bremsenabrieb: 7.000 t/Jahr (Ergänzung)
                Reifen, Reifenabrieb (Gummireifen): 6.000 t/Jahr (Ergänzung)
                Straßenbelag, Straßenoberfläche: derzeit keine Angaben verfügbar
            Aufwirbelung von Straßenstaub
        Luftverkehr, Schiffsverkehr und sonstiger Verkehr: 16.000 t/Jahr
            Abgase der
                Turbinen-Antriebe
                Düsen-Antriebe (Raketen-Antriebe)
            Partikel durch verglühende Satelliten und Raketen-Antriebsstufen
        Schienenverkehr: 6.000 t/Jahr
            Abgase der Diesel-Motoren
            Bremssand
            Abrieb Rad-Schiene
            Abrieb Kohleleiste des Stromabnehmers und der Oberleitung
            Zermahlung des Schotters

    Privathaushalte und Kleinverbraucher: 33.000 t/Jahr
        Heizungen
            Öl-Brenner
            Holzheizungen
            andere Heizungen
        sonstiges
            Räucherwerk (vor allem Räucherstäbchen und Räucherkerzen aus Privathaushalten und anderes Räucherwerk aus liturgischen Verbrauchern)
            Silvester-Feuerwerk: 4.000 t/Jahr[16][17]
            Kerzen, Öllampen und andere Leuchtmittel mit Abbrand

    Elektrizitäts- und Fernheizwerke: 19.000 t/Jahr
        Öl-Brenner, Gas-Brenner, Kohle-Brenner
        Filterstäube

    Landwirtschaft: 15.000 t/Jahr
        Tierhaltung: 7.500 t/Jahr
        Sonstige: 7.500 t/Jahr

Dies ergab eine Gesamtzahl von rund 205.000 t/Jahr. Diese Zahl war in vieler Hinsicht unvollständig. Zum Beispiel wurde Feinstaub aus Tagebauen wie dem Braunkohletagebau ignoriert und der Anteil des Straßenverkehrs wurde zunächst nur teilweise berücksichtigt: Der Abrieb von Reifen, Bremsbelägen und Straßenasphalt fehlte. Der Reifenabrieb verursachte grob geschätzt rund 60.000 t/Jahr (davon PM10-Anteil etwa 10 %, also rund 6.000 t/Jahr) und der Bremsabrieb 5.500 bis 8.500 t/Jahr (überwiegend PM10) (Umweltbundesamt 2004). Über Emissionen von der Straßenoberfläche sind keine Schätzungen bekannt.

## EU

Feinstaubbelastung (PM10) in Europa.

In Europa wurden erstmals mit der Richtlinie 80/779/EWG vom 15. Juli 1980 (in deutsches Recht umgesetzt mit der Verordnung über Immissionswerte – 22. Bundes-Immissionsschutzverordnung) Grenzwerte für Feinstaub festgelegt. Diese Richtlinie wurde im Laufe der Jahre weiterentwickelt:

    Seit dem 1. Januar 2005 beträgt der einzuhaltende Tagesmittelwert für PM10 50 µg/m³ bei 35 zugelassenen Überschreitungen im Kalenderjahr. (In Österreich sind von 1. Januar 2005 bis 31. Dezember 2009 nur 30 Überschreitungen/Jahr erlaubt)
    Seit dem Jahr 2005 beträgt der Jahresmittelwert für PM10 40 µg/m³.
    Seit dem 1. Januar 2010 darf der einzuhaltende Tagesmittelwert für PM10 weiterhin 50 µg/m³ betragen, die ursprünglich vorgesehenen nur noch 7 zugelassenen Überschreitungen im Kalenderjahr sind durch Richtlinie 2008/50/EG vom 21. Mai 2008 (Anhang XI) wieder auf die ursprünglich zulässigen 35 Überschreitungen korrigiert worden.
    Seit dem Jahr 2010 sollte der Jahresmittelwert für PM10 nur noch 20 µg/m³ betragen. Auch dies ist durch die Richtlinie 2008/50/EG wieder entschärft worden, so dass seit 2010 weiter der Jahresmittelwert für PM10 40 µg/m³ gilt.[25]


## European Union
European Union


The European Union has established the European emission standards which include limits for particulates in the air:[84]
                PM10        PM2.5
Yearly average 	40 µg/m3 	25 µg/m3

Daily average (24-hour)   50 µg/m3    None
Allowed number of exceedences per year  35  None 


## United States
The United States Environmental Protection Agency (EPA) has set standards for PM10 and PM2.5 concentrations.[93] (See National Ambient Air Quality Standards) 

PM10

daily limit since 1987[94]
annual limit removed in 2006

PM2.5

daily limit since 2007
annual limit since 2012

Yearly average 	None 	12 µg/m3
Daily average (24-hour)

Allowed number of exceedences per year
	150 µg/m3

1
	35 µg/m3

Not applicable (3-year average of annual 98th percentile) 

## Japan

Japan has set limits for particulates in the air:[86][87]
	PM10[88] 	PM2.5

since 21 September 2009
Yearly average 	None 	15 µg/m3
Daily average (24-hour)

Allowed number of exceedences per year
	100 µg/m3

None
	35 µg/m3

None


## WHO

WHO

Die Weltgesundheitsorganisation empfiehlt angesichts der vom Feinstaub ausgehenden Gesundheitsgefahren in ihren WHO-Luftgüte-Richtlinien folgende Grenzwerte für Feinstaub:[41]

    Jahresmittel PM10 20 µg/m³
    Jahresmittel PM2,5 10 µg/m³

    Tagesmittel PM10 50 µg/m³ ohne zulässige Tage, an denen eine Überschreitung möglich ist.
    Tagesmittel PM2,5 25 µg/m³ ohne zulässige Tage, an denen eine Überschreitung möglich ist.

Die Richtwerte der WHO liegen damit deutlich unter den rechtswirksamen Grenzwerten der EU.

## Mailänder Studie

Invernizzi, Giovanni, et al.: Particulate matter from tobacco versus diesel car exhaust: an educational perspective. In: Tobacco Control. Volume 13, Nr. 3, 2004, S. 219–221, doi:10.1136/tc.2003.005975, PMC 1747905 (freier Volltext).

Italienische Wissenschaftler vom nationalen Krebsinstitut in Mailand verglichen 2004 die Feinstaubbelastung eines abgasreduzierten Diesel-PKWs im Leerlauf mit der Belastung durch Zigarettenrauch. Die Forscher betrieben in einer Garage mit 60 m³ Rauminhalt zunächst eine halbe Stunde lang bei geschlossenen Türen und Fenstern einen Ford Mondeo Turbodiesel im Leerlauf und bestimmten währenddessen die Partikelkonzentration. Anschließend wurde die Garage vier Stunden lang gründlich gelüftet und das Experiment mit drei Zigaretten wiederholt, die innerhalb von 30 Minuten abgebrannt wurden. Die Feinstaubbelastung lag im PKW-Experiment bei 36 (PM10), 28 (PM2,5), und 14 (PM1) µg/m³, im Zigaretten-Experiment bei 343 (PM10), 319 (PM2,5), und 168 (PM1) µg/m³. Beide Befunde erwiesen sich als hoch signifikant (p < 0.001). Ihre Untersuchung, so das Fazit der Wissenschaftler, belege die starke Feinstaubbelastung, die von Zigarettenrauch in geschlossenen Räumen ausgehe. Die Autoren weisen in ihrer Studie darauf hin, dass bei einem anderen, vergleichbaren Experiment die Feinstaubemissionen eines nicht abgasreduzierten Dieselmotors selbst im Leerlauf um ein Vielfaches höher lagen (300 µg/m³ bei bereits erfolgter Verdünnung mit 90 % Luft).[59] 



# Sensor
The Nova Fitness SDS011 Dust Sensor using principle of laser scattering and can get the particle concentration between 0.3 to 10µm in the air. It has a digital serial output and built-in fan.

Features

- Accurate and Reliable: laser detection
- Quick response: response time is less than 10 seconds
- Easy integration: UART output (3.3V logic level)
- Fan built-in;
- High resolution of 0.3µg/m3;
- Certification: CE / FCC / RoHS
- Power Supply: 5V

https://www.watterott.com/de/Nova-SDS011-Feinstaub-Sensor

http://aqicn.org/sensor/sds011/ for more details on how the sensor is built.

## Working principle

Using laser scattering principle:
Light scattering can be induced when particles go through the detecting area. The scattered light is transformed into electrical signals and these signals will be amplified and processed. The number and diameter of particles  can  be  obtained  by  analysis because  the  signal  waveform  has certain relations with the particles diameter.

### https://en.wikipedia.org/wiki/Particle_counter
A particle counter is an instrument that detects and counts physical particles.

The light scattering method is capable of detecting smaller-sized particles. This technique is based upon the amount of light that is deflected by a particle passing through the detection area of the particle counter. This deflection is called light scattering. Typical detection sensitivity of the light scattering method is 0.05 micrometre or larger.


### https://en.wikipedia.org/wiki/Laser_diffraction_analysis
Laser diffraction analysis, also known as laser diffraction spectroscopy, is a technology that utilizes diffraction patterns of a laser beam passed through any object ranging from nanometers to millimeters in size[1] to quickly measure geometrical dimensions of a particle. This process does not depend on volumetric flow rate, the amount of particles that passes through a surface over time.[2

Laser diffraction analysis is based on the Fraunhofer diffraction theory, stating that the intensity of light scattered by a particle is directly proportional to the particle size.[4] The angle of the laser beam and particle size have an inversely proportional relationship, where the laser beam angle increases as particle size decreases and vice versa.[5]



# Nova Fitness Co., Ltd.
* small company dedicated to air quality testers and measurement system development
* their main products laser-based sensors for air quality



# My Linux platform
* paul@terminus:~/Repositories/duplys.github.io/_drafts$ python --version
  Python 2.7.12




# The Code 

{% highlight python %}
import serial
import time
import datetime
import json

debug = "no"

t = datetime.datetime.now()
pm25f = './data/' + t.isoformat() + '-PM2.5.csv'
pm10f = './data/' + t.isoformat() + '-PM10.csv'


with serial.Serial('/dev/ttyUSB0', baudrate=9600) as ser:
    while True:
        x = ser.read(10)          # read 10 bytes
        d = x.encode('hex')
        
        if debug == "yes":
            print('RAW:   ' + d)
            print('PM2.5: ' + d[6:8] + d[4:6])
            print('PM10:  ' + d[10:12] + d[8:10])
            
        if d[2:4] == "c0":
            pm25=int(d[6:8] + d[4:6], base=16)/10.0
            pm10=int(d[10:12] + d[8:10], base=16)/10.0
            print("\n[*] PM2.5: %.1f ug/m3" % (pm25))
            print("[*] PM10:  %.1f ug/m3" % (pm10))

            
            with open(pm25f, 'a') as f:
                f.write(str(pm25) + '\n')

            with open(pm10f, 'a') as f:
                f.write(str(pm10) + '\n')

        time.sleep(3)
{% endhighlight %}


# Plotting!!!

The Gnuplot script for my data:

```
set size 1.0, 1.0
set terminal png
set output "test-plot.png"
set yrange [0:20]
plot "data/2018-07-25T21:12:12.158650-PM10.csv" w lines, "data/2018-07-25T21:12:12.158650-PM2.5.csv" w lines
exit
```

Call gnuplot using

```
$ gnuplot plot.gp
```

# A security twist

## Random.org


What's this fuss about true randomness?

Perhaps you have wondered how predictable machines like computers can generate randomness. In reality, most random numbers used in computer programs are pseudo-random, which means they are generated in a predictable fashion using a mathematical formula. This is fine for many purposes, but it may not be random in the way you expect if you're used to dice rolls and lottery drawings.

RANDOM.ORG offers true random numbers to anyone on the Internet. The randomness comes from atmospheric noise, which for many purposes is better than the pseudo-random number algorithms typically used in computer programs. People use RANDOM.ORG for holding drawings, lotteries and sweepstakes, to drive online games, for scientific applications and for art and music. The service has existed since 1998 and was built by Dr Mads Haahr of the School of Computer Science and Statistics at Trinity College, Dublin in Ireland. Today, RANDOM.ORG is operated by Randomness and Integrity Services Ltd.

Also regarding a comparison of TRNG and PRNG, read: https://www.random.org/randomness/

I'm wondering whether you can also build a TRNG based on particle measurement.

Oder detektion von personen im Raum?

[ub-at-pm25]: http://www.umweltbundesamt.at/pm25/
[ub-at-pm10]: http://www.umweltbundesamt.at/umweltsituation/luft/luftschadstoffe/staub/pm10/
[ub-de-fs]: https://www.umweltbundesamt.de/daten/luft/feinstaub-belastung#textpart-1
[ub-de-al]: https://www.umweltbundesamt.de/daten/luftbelastung/aktuelle-luftdaten#/start?s=q64FAA==&_k=2rax3w

[sds-011-spec]: https://www.watterott.com/media/files_public/edcqnbebxe/SDS011.pdf



