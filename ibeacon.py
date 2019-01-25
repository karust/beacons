import subprocess as sb

#                      Interface
common = ["hcitool", "-i", "hci0", "cmd", 
"0x08",       # OGF = Operation Group Field = Bluetooth Command Group = 0x08
"0x0008"]     # OCF = Operation Command Field = HCI_LE_Set_Advertising_Data = 0x0008


def parseUrl(url):
  if '.' not in url:
    return False
  sep = url.split(".")

  url= ["02"] # URL Scheme (http:// = 0x02),
  i = 0
  for c in sep[0]:
    url += [hex(ord(c))[2:]]
    i+=1
    if i >= 18:
      return False

  if [1] == "org":
    url += ["08"] #.org
  else:
    url += ["07"] # ?
  i+=1

  while i<18:
    url += ["00"]
    i+=1
  return url


def eddystone(url):

  namespaceID = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
  instanceID =  [ "01", "02", "03", "04", "05", "06"]

  sb.run(common+["1e", 
  "02", # Length
  "01", # Flags data type value
  "1a", # Flags data
  "03", # Length
  "03", # Complete list of 16-bit Service UUIDs data type value
  "aa", # 16-bit Eddystone UUID
  "fe", # 16-bit Eddystone UUID
  "15", # Length
  "16", # Service Data data type value
  "aa", # 16-bit Eddystone UUID
  "fe", # 16-bit Eddystone UUID
  "10", # Frame Type = URL(0x10), IDs(0x00)
  "d1"] # txPower
  + url
  #       + namespaceID
  #       + instanceID
         )
  print("Eddystone is running")


def ibeacon():

  proximityUUID = ["FB", "0B", "57", "A2", "82", "28", "44", "CD", "91", "3A", 
  "94", "A1", "22", "BA", "12", "06"]

  sb.run(common+["1E",
  "02",       # Length
  "01",       # Type (Flags)
  "1A",       # Value (Typical Flags) 
  "1A",       # Length БЦ Манхеттен
  "FF",       # Type (Custom Manufacturer Packet)
  "4C", "00", # Manufacturer ID
  "02",       # SubType (iBeacon)
  "15",       # SubType Length
  ] + proximityUUID + [
  "00", "01", # Major
  "00", "02", # Minor
  "D1", "00"])# Signal Power      
  print("IBeacon is running")


def altbeacon():

  beaconID = ["00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00",
            "00", "00", "00", "00", "00", "00", "01", "00", "01",]

  adFlags = ["02", "01", "1a"]
  advert = ["1b",  # AD LENGTH 
  "ff",            # AD TYPE 
  "18", "01",      # MFG ID
  "be", "ac",      # BEACON CODE
  ] + beaconID + [
  "c5",            # REFERENCE RSSI
  "01"]            # MFG RESERVED
  adLen = [str(hex(len(adFlags+advert))[2:])]

  sb.run(common + adLen + adFlags + advert) 
  print("AltBeacon is running")


if __name__ == "__main__":
  
  # Should be run as root
  sb.run(["hciconfig", "hci0", "up"]) 
  sb.run(["hciconfig", "hci0", "leadv", "3"]) 
  sb.run(["hciconfig", "hci0", "noscan"]) 
  
  while True:
    print("""Chose beacon: 1) Eddystone; 2) IBeacon; 3) AltBeacon""")
    raw = input(">>")
    if "1" in raw:
      url = input("Enter URL: ")
      if len(url) == 0:
        url = "sne.life"

      res = parseUrl(url=url)
      if not res:
        print("Incorrect URL or message is long")
        break
      eddystone(url=res)

    elif "2" in raw:
      ibeacon()
    elif "3" in raw:
      altbeacon()