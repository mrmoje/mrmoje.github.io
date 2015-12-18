Title: TEST POST
Tags: testing
Slug: testing
Category: TEST
Author: James Nzomo
Summary: A simple test post...complete with a PAL test pattern and an annoying complementary 1KHz tone - just for your ears.

<center>
![PM5544](https://upload.wikimedia.org/wikipedia/commons/c/c4/PM5544_with_non-PAL_signals.png)


##Problem? &rarr; <button onclick=osc.stop()>STFU!</button>
</center>
<script type="text/javascript">
var context = new AudioContext();
var osc = context.createOscillator();
var vol = context.createGain();
osc.frequency.value = 1000;
vol.gain.value = 0.1;
osc.connect(vol);
vol.connect(context.destination);
osc.start(0);
// Problem?
osc.stop();
</script>

<hr>

#TEST CONTENT
with placeholder text generated at [Samuel L. Ipsum](http://slipsum.com/)

# H1
## H2
### H3
#### H4
##### H5
###### H6

Underline-H1
======

Underline-H2
------

### Formatting
Asterisks -> *Italic*, **bold**, ***bold italic***  
Underscores -> _Italic_, __bold__, ___bold italic___  
`monospace`  
~~~strikethrough text~~~


### Paragraph one
Now that there is the Tec-9, a crappy spray gun from South Miami. This gun is
advertised as the most popular gun in American crime. Do you believe that shit?
It actually says that in the little book that comes with it: the most popular
gun in American crime. Like they're actually proud of that shit.


    #!c
    //function sets
    void set_portAbit(unsigned char bt, bool val)
    {
        val ? ( sPORTA |= 1 << bt ) : ( sPORTA &= ~(1 << bt) );
        PORTA = sPORTA;
    }

### Paragraph two
Well, the way they make shows is, they make one show. That show's called a pilot.
Then they show that show to the people who make shows, and on the strength of
that one show they decide if they're going to make more shows. Some pilots get
picked and become television programs. Some don't, become nothing.
She starred in one of the ones that became nothing.

### Paragraph three block quotes
> Your bones don't break, mine do. That's clear. Your cells react to bacteria and
> viruses differently than mine. You don't get sick, I do. That's also clear. But
> for some reason, you and I react the exact same way to water. We swallow it too
> fast, we choke. We get some in our lungs, we drown. However unreal it may seem,
> we are connected, you and I. We're on the same curve, just on opposite ends.

### Longer Code block

    #!c
    #include <xc.h>
    #include <stdio.h>
    #include <stdbool.h>
    #include <string.h>
    #include <ctype.h>

    // #pragma config statements should precede project file includes.
    // Use project enums instead of #define for ON and OFF.

    // CONFIG
    #pragma config FOSC = INTOSCIO  // Oscillator Selection bits (INTOSC oscillator: I/O function on RA6/OSC2/CLKOUT pin, I/O function on RA7/OSC1/CLKIN)
    #pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
    #pragma config PWRTE = ON       // Power-up Timer Enable bit (PWRT enabled)
    #pragma config MCLRE = ON       // RA5/MCLR/VPP Pin Function Select bit (RA5/MCLR/VPP pin function is MCLR)
    #pragma config BOREN = ON       // Brown-out Detect Enable bit (BOD enabled)
    #pragma config LVP = OFF        // Low-Voltage Programming Enable bit (RB4/PGM pin has digital I/O function, HV on MCLR must be used for programming)
    #pragma config CPD = OFF        // Data EE Memory Code Protection bit (Data memory code protection off)
    #pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)

    #define DEBUG

    #define _XTAL_FREQ   4000000 // needed by some macros
    #define FCY _XTAL_FREQ/4

    // Comm Setup
    #define BAUDRATE 1200


    #define BUZZER_PIN RB5
    #define TOGGLE_BUZZER_PIN BUZZER_PIN = ~BUZZER_PIN;

    //Globals
    unsigned char 
        receive_buffer[5], //cmd reveive buffer
        sPORTA; //PORTA Shadow register


    //Prototypes
    void
        BOARD_init(void),
        USART_putc(unsigned char),
        buzz_ok(void),
        buzz_error(void),
        set_portAbit(unsigned char bt, bool val);
    void interrupt ISR(void);
    unsigned char USART_getc(void);

    // Main function
    void main()
    {
        BOARD_init();
        printf("INIT!\r\n");
        buzz_ok();
        while(1);
    }

---
List of Links:

  * [TDT][1]
  * [KILI][2]
  * [NLUG][3]

---
Numbered list of links:

 1. [Openstack Nairobi](http://www.meetup.com/OpenStack-Nairobi/)
 2. [Python Nairobi](http://www.meetup.com/Python-Nairobi/)
---
Nested list:

 1. Openstack Nairobi

      - http://www.meetup.com/OpenStack-Nairobi
      - https://wiki.openstack.org/wiki/Main_Page

 2. Python Nairobi

      - http://www.meetup.com/Python-Nairobi
      - https://github.com/Python-Nairobi


[1]: http://tdt.rocks
[2]: http://kili.io
[3]: http://nairobilug.or.ke
