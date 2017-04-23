#Title: Toggling desklamps via twitter with Python at NTW (Part 1)
Date: 2017-03-25 18:54:00
Tags: IoT, micropython
Slug: twitter_desklamps_ntw_workshop_part1
Author: James Nzomo
Summary: This is a story about Electrical Extension Cords that run python, feature WiFi and allow toggling outlets via tweets!
email: james@tdt.rocks
about_author: I dedicate my mind to thoughts and deeds on tech:- software and hardware development.

#Intro
The extension cords in the image below run Python and feature WiFi. You can
toggle the lamps connected to the ports on and off just by tweeting (with
specific hashtags):-
![PY_WIFI_EXT_CORD][PY_WIFI_EXT_CORD]
***fig.1 The shiznit!***

#First, some background,
Few weeks ago, at work, our head of engineering tasked us to come up with
content for a workshop at the [2017 Nairobi Tech Week][NTW] where we would
demo mob programming.

Challenge accepted and so we decided to "adapt" [a previous micropython presentation
I gave at moringa][moringa_uPy_IoT] where I had demo'd toggling 6 desklamps
from a Python [REPL][uPyREPL].

The hardware was composed of a esp8266 dev board [(flashed with uPy)][uPyESP],
afew relays and one 6-port electrical extension cord but it was abit
"untidy" with wires looping all over the components and was thus unsuitable
for this workshop. So this time round I would scale down the setup to a 3 port
extension and have all the extras packaged inside the extension's housing.

I'd then replicate the setup twice so we could group the workshop attendees
around each so they could sort of compete in mob-programing challenges we
would give.

Thus our BOM for each:-
- 1 x 3 port socket with USB ports (supplies 5V for the low power side)
- 3 x Omron G3MB-202P Solid State Relays to toggle the ports switch[NEROKAS][NEROKAS]
- 3 x BC547 Transistors for logic level converion (ESP's 3.3v to the SSR's 5v)[NEROKAS][NEROKAS] [WAREFAB][WAREFAB]
- 1 x ESP-12 - The brains behind the business [WAREFAB][WAREFAB]
- 2 meters of 16 AWG Wire (RED)[NEROKAS][NEROKAS]
- Crapton of 1KΩ resistors[NEROKAS][NEROKAS] [WAREFAB][WAREFAB]

How to put all these to work? Lets work backwords
[ADD EE UNQUALIFICATION DISCLAIMER]

#[WIP]Extension Cord and Power Supply


#[WIP]Controlling mains - The SSR
![MAINS_IS_HATARI][MAINS_IS_HATARI]
I decided to go with the first capable (and affordable) SSR I could find on Nerokas
the [G3MB-202P][G3MB-202P]. It was more than good enough for the job since we were
only going to switch 3Watt LED lamps with it. It provided isolation out of the box
and all it asked for was 5V to power its IR LED and it would handle the rest.

#[WIP]Logic level conv - BC547 ESP to SSR
SSR's IR LED draws 10mA at 5V, well below the BC547's Ic(max) of 0.1 A and Vceo(max) of 45V.

Also, the ESP8266 can supply max 12mA of current, which is more than the 1mA the BC547
requires for `Ib` in order to supply the SSR with the 10mA it needs:- `(Ib = Ic/10 = 1mA)`

For good measure, lets "cap" the current a 2.5mA. When `Ic = 10mA`, `Vbe(sat) = .72V`
and with the ESP supplying 3.3V on each GPIO pin we need to drop 2.58V with a resistor
whose value will be `R = V/I = 2.58V/0.0025A = 1032Ω`.
(lets just go with a 1KΩ resistor - Brown-Black-Red and hopefully the 5%-Gold will take
care of the 32Ω change)

#[WIP]ESP-12 (ESP8266)




[NTW]: http://nairobitechweek.com/
[uPy]: https://micropython.org/
[uPyREPL]: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/repl.html
[uPyESP]: https://micropython.org/download#esp8266
[G3MB-202P]: https://store.nerokas.co.ke/index.php?route=product/product&product_id=1005
