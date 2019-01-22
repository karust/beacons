import subprocess as sb

#                      Interface
common = ["hcitool", "-i", "hci0", "cmd", "0x08", "0x0008"]


def eddystone():
  txPower = "e7"
  namespaceID = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
  instanceID =  [ "01", "02", "03", "04", "05", "06"]
  
  sb.run(common+["1e", "02", "01", "06", "03", "03", "aa", "fe", "15", "16", "aa", "fe", "00", txPower]
         + namespaceID + instanceID)
  print("Eddystone is running")


def ibeacon():
  sb.run(common+["1E", "02", "01", "1A", "1A", "FF", "4C", "00",
          "02", "15", "FB", "0B", "57", "A2", "82", "28", "44", "CD", "91", "3A", "94", "A1", "22", "BA", "12",
          "06", "00", "01", "00", "02", "D1", "00"]) 
  print("IBeacon is running")


def altbeacon():
  adFlags = ["02", "01", "1a"]
  advert = ["1b", "ff", "18", "01", "be", "ac", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00",
            "00", "00", "00", "00", "00", "00", "01", "00", "01", "c5", "01"]
  adLen = [str(hex(len(adFlags+advert))[2:])]

  sb.run(common + adLen + adFlags + advert) 
  print("AltBeacon is running")


if __name__ == "__main__":
  while True:
    print("""Chose beacon: 1) Eddystone; 2) IBeacon; 3) AltBeacon""")
    raw = input(">>")
    if "1" in raw:
      eddystone()
    elif "2" in raw:
      ibeacon()
    elif "3" in raw:
      altbeacon()
  
