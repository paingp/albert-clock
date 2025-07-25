import time
import pigpio
from ir_hasher import hasher

def cbfunc(hash):
    global hashes
    button = "UNKNOWN"
    if (hash in hashes):
        button = hashes[hash]

    print(f"key={button}      hash={hash}")
    

if __name__ == '__main__':
    gpio_ir = 17

    hashes = {
      142650387: '2',       244341844: 'menu',    262513468: 'vol-',
      272048826: '5',       345069212: '6',       363685443: 'prev.ch',
      434191356: '1',       492745084: 'OK',      549497027: 'mute',
      603729091: 'text',    646476378: 'chan-',   832916949: 'home',
      923778138: 'power',   938165610: 'power',   953243510: 'forward',
      1009731980:'1',       1018231875:'TV',      1142888517:'c-up',
      1151589683:'chan+',   1344018636:'OK',      1348032067:'chan+',
      1367109971:'prev.ch', 1370712102:'c-left',  1438405361:'rewind',
      1452589043:'pause',   1518578730:'chan-',   1554432645:'8',
      1583569525:'0',       1629745313:'rewind',  1666513749:'record',
      1677653754:'c-down',  1825951717:'c-right', 1852412236:'6',
      1894279468:'9',       1904895749:'vol+',    1941947509:'ff',
      2076573637:'0',       2104823531:'back',    2141641957:'home',
      2160787557:'record',  2398525299:'7',       2468117013:'8',
      2476712746:'play',    2574308838:'forward', 2577952149:'4',
      2706654902:'stop',    2829002741:'c-up',    2956097083:'back',
      3112717386:'5',       3263244773:'ff',      3286088195:'pause',
      3363767978:'c-down',  3468076364:'vol-',    3491068358:'stop',
      3593710134:'c-left',  3708232515:'3',       3734134565:'back',
      3766109107:'TV',      3798010010:'play',    3869937700:'menu',
      3872715523:'7',       3885097091:'2',       3895301587:'text',
      3931058739:'mute',    3983900853:'c-right', 4032250885:'4',
      4041913909:'vol+',    4207017660:'9',       4227138677:'back',
      4294027955:'3'
    }

    pi = pigpio.pi()
    if not pi.connected:
        print(f"ERROR: pigpio not connected")
        exit()

    ir = hasher(pi, gpio_ir, cbfunc)

    print("ctrl c to exit");

    time.sleep(300)

    pi.stop()


