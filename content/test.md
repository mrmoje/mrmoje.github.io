Title: TEST
Tags: testing
Slug: testing
Category: TEST
Author: James Nzomo
Summary: TEST SUMMARY

<center>
![PM5544](https://upload.wikimedia.org/wikipedia/commons/c/c4/PM5544_with_non-PAL_signals.png)
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
// osc.stop();
</script>
