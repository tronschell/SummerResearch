from sec_edgar_downloader import Downloader

try:
    # Open the ANNCRSPcik210411.txt file and read all of the lines
    with open("ANNCRSPcik210411.txt", "r") as f:
        lines = f.readlines()

    print(len(lines))

    # Create an instance of the downloader and make it download directly the the project folder
    dl = Downloader()

    # For every line in the lines list, get the 10-K in 2020
    for line in lines:
        dl.get("10-K", str(line).zfill(11), after="2020-01-01", before="2020-12-30")
        print("Found and downloaded", line)

except:
    print("Cannot find CIK, moving on...")
    pass

