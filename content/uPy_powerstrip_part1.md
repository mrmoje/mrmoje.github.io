Title: MicroPython PowerStrip
Category: Hardware
Tags: Hardware, MicroPython, ESP8266, electronics,
Slug: uPy_powerstrip
Author: James Nzomo
Summary: A powerstrip that runs python and feature IEEE 802.11 b/g/n Wi-Fi.
email: james@tdt.rocks
about_author: I dedicate my mind to thoughts and deeds on tech:- software and hardware development.

#INTRO

![THE SETUP][THE_SHIZNIT]
The powerstrip pictured above runs Python 3 and features IEEE 802.11 b/g/n Wi-Fi.
With the right python script(s) loaded, you can toggle each port over the Internet
and with the right networking setup, from anywhere in the world
<img class="emoji" alt="sunglasses" height="20" width="20" src="https://github.githubassets.com/images/icons/emoji/unicode/1f60e.png">!

# Prelude
Sometime late 2016, our Head of Dept put out an RFP for a python related
presentation/workshop we were tasked to come up with.
Having hobbied a bit with MicroPython on SoCs, I thought we would field something
on the topic and we came up with a lightshow of desklamps toggled by rudimentary
prototype-esque hardware all controlled by Python. After taking them through MicroPython
internals, the participants had abit of fun scripting arbitrary light patterns.

Few months later, we ran a remix of the session for our [MOB Programming Workshop][JUMONTW2017]
at [Nairobi Tech Week 2017][NTW2017], toggling connected desklamps by tweeted hashtags and
again 2 years later, for one of our [Python-Nairobi Meetups][PYNBO_180519] with refined hardware
(Pictured in the [Intro][#INTRO]), the making of which i'll discuss here.

# Some words of caution
- This project involves working with mains electricity. This can be fatal! - Replicate at your own risk!
- Though I hobby in the field, I am not an afficianado on electronics! - Take nothing here as pure gospel!
- Some ideas here have been run by experts but not all of them have been fully thought through - I encourage you to verify and point out any errs in the comments bellow.

Now that that's out of the way, lets talk about the thing from the heart of it all the way up to the mains.

# The Heart of it - ESP12
The [ESP12][ESP12] is really a ESP8266 nicely soldered onto a 24x16mm breakout board with a
PCB trace WiFi antenna, oscillator, SPI flash memory and afew passives all tucked away under
a nice square FCC approved RFI sheild. I got the AI-Thinker ones. [Checkout their datasheet][ESP12_DATASHEET]

At the core of it is the mentioned [ESP8266][ESPRESSIF], a system-on-chip (SoC) that integrates (among other things):-
- a Tensilica L106 32-bit RISC processor clocked at 80MHz (or up to 160MHz if it left the factory defect free)
- 80kB of ram but you only get to work with max 50kB for your data.
- a 2.4 GHz transceiver radio for Wi-Fi
For more specs, [checkout the datasheet][ESP8266_DATASHEET].

Meager as it sounds, this SoC is beefy enough to run its own [MicroPython][MICROPYTHON] port
that provides a python3 interface to all the features within including Wi-Fi and all usable
11 GPIO pins, 4 of which we will use to control each outlet on our powerstrip but via a proxy
component that can handle load amperes at mains voltage.
For this, we choose a Solid State Relay - SSR for short.

# Controlling mains - The OMRONSSR
While there are plenty of ways to control higher mains voltage from low power devices,
- 4x Electromechanical Relays (though generally better for high AMPs) take up space (even without supporting components).
- 4x dual-MOSFETs/transistors or single TRIACs with supporting components = more footprints = routing mission and less PCB space to work with.

The clear winner for me was a compact SSR. Reason?:- they have all the things they need
to do the business in one small (high & low voltage opto-isolation included).
All this exposed to 4 PADs in a small footprint. 2 for mains, 2 for DC control

So I decided to go with the first capable (and affordable) SSR I could find on Nerokas
the [G3MB-202P][G3MB-202P]. Comming in a 20x24.5x5.5mm size package and capable of max
2Amps thru the high voltage side, It was more than good enough for the job since we were
only going to switch 3Watt LED lamps with it. As mentioned it provides opto isolation
out of the box and all it asked for was 5V to power its IR LED and it would handle the rest.

Problem is, our ESP12 will only put out 3.3V from any of the 4 GPIO pins which is Insufficient
to switch on our SSR. When any of those pins go high at 3.3, we need to convert that to a 5V
input for the SSR. A logic level converter of sorts!

#[WIP]Logic level conv - ESP12 => BC547 => SSR
To carry out the 3.3v to 5v conversion, I chose a NPN transistor as a low side switch
and I settled on the BC547 because I had plenty at home but also quite a capable
component.
And just to show it was a good fit, the chosen SSR's IR LED draws 10mA at 5V,
which is well below the BC547's Ic(max) of 0.1 A and Vceo(max) of 45V.
Also, the ESP8266 can supply max 12mA of current, which is more than
the 1mA the BC547 requires for `Ib` in order to supply the SSR's LED with the 10mA it needs:-
`(Ib = Ic/10 = 1mA)`.

For good measure, I "capped" that current a 2.5mA like so:- When `Ic = 10mA`, `Vbe(sat) = .72V`
and with the ESP supplying 3.3V on each GPIO pin we drop 2.58V with a resistor whose value will
be `R = V/I = 2.58V/0.0025A = 1032Ω`.
To make things simple, 1KΩ resistor would suffice - Brown-Black-Red and hopefully the 5%-Gold will take
care of the 32Ω change.


#[WIP] The Enclosure
One of the goals of this project was to have everything neatly tucked powerstrip enclosure.
At a local supermarket, i stumbled upon a ![Solatek MG-4U][MG4U] - a 4 port power strip
with enough room for a 2x3x0.8 inch and change PCB and components (once you yank out the 3 MoV PCB in it)

Whats also good about this is you can cut the live rail into 4 and there's still enough plastic standoff to hold each piece well



### Resources, Refs & google juice:-
  - [esp8266.net][ESP8266.NET]
  - [The creators][ESPRESSIF]

[THE_SHIZNIT]: img/uPy_powerstrip/pwnt_pcb.jpg "THE SHIZNIT"
[JUMONTW2017]: https://twitter.com/nairobitechweek/status/844512757219295233
[NTW2017]: http://nairobitechweek.com/
[PYNBO_180519]:https://www.meetup.com/Python-Nairobi/events/cqbkrqyzhbxb/
[ESP12]: https://www.esp8266.com/wiki/doku.php?id=esp8266-module-family#esp-12
[ESP12_DATASHEET]: https://wiki.ai-thinker.com/_media/esp8266/a014ps01.pdf
[ESPRESSIF]: https://www.espressif.com/products/hardware/esp8266ex/overview/
[ESP8266_DATASHEET]: https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf
[MICROPYTHON]: https://micropython.org
[NEROKAS]: https://store.nerokas.co.ke
