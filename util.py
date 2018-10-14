def convert_ms(ms):
     seconds = (ms / 1000) % 60
     minutes = (ms / (1000 * 60)) % 60
     hours = (ms / (1000 * 60 * 60)) % 24
     return ms, seconds, minutes, hours

