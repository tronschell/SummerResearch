from sec_edgar_downloader import Downloader


# Open the ANNCRSPcik210411.txt file and read all of the lines
with open("ANNCRSPcik210411.txt", "r") as f:
    lines = f.readlines()

print(len(lines))

# Create an instance of the downloader and make it download directly the the project folder
dl = Downloader()

# For every line in the lines list, get the 10-K in 2020
for line in lines:
    try:
        dl.get("10-K", str(line).zfill(11), after="2020-03-31", before="2021-03-31")
        print("Found and downloaded", line) 
    except:
        pass



