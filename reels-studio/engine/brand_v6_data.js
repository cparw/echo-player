const A = '../brand/round6/ai/';
window.DATA = {
  sub: 'Reply with a number. Mix and match is fine.',
  bio: 'The GTA 6 details you missed. Every big game next.',
  items: [
    { name: 'missed', flat: 'm', star: true, line: 'The m hides a ! That is the detail you missed.' },
    { name: 'missed', img: A + 'glass_m.jpg', line: 'The same mark in glass.' },
    { name: 'missed', img: A + '13_rewind.jpg', line: 'Missed it? Rewind.' },
    { name: 'noticed', flat: 'badge', line: 'Reads as an unread notification. Hard not to tap.' },
    { name: 'noticed', img: A + '01_alert.jpg', line: 'The alert when something gets noticed.' },
    { name: 'glimpse', img: A + '09_keyhole.jpg', line: 'A look through the keyhole.' },
    { name: 'glimpse', img: A + '07_sliver.jpg', line: 'A door open just a crack.' },
    { name: 'blinked', flat: 'blink', line: 'It happened while you blinked.' },
    { name: 'decoded', flat: 'morse', line: 'Dash dot dot: the letter d in Morse code.' },
    { name: 'overlooked', flat: 'eyes', line: 'Everyone looks the wrong way. It is right there.' },
    { name: 'infrared', img: A + '03_thermal.jpg', line: 'Sees what the eye cannot.' },
    { name: 'blacklight', img: A + '04_uv.jpg', line: 'The light that shows hidden marks.' },
    { name: 'detected', img: A + '00_eye.jpg', line: 'The stealth game alert: you have been seen.' },
    { name: 'hush', img: A + '14_hush.jpg', line: 'A secret, quietly shared.' },
    { name: 'iceberg', img: A + '08_iceberg.jpg', line: 'You have only seen the tip.' },
  ],
  top: [1, 6, 4],
  why: {
    1: 'Your own words: "something that I missed". The m hides an exclamation mark, so the logo itself is a hidden detail.',
    6: 'Curiosity in one picture: everyone wants to look through a keyhole.',
    4: 'Looks like an unread notification, the one thing nobody can leave untapped.',
  },
};
