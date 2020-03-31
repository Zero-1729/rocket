import os
import wallice


def no_dash(dir):
    return dir if dir != '-' else ''


raw_parentfolders = ['./tutorials/'+parent if (parent[0] != '.' and '.py' not in parent) else '-' for parent in os.listdir('./tutorials')]
parentfolders = [parent for parent in filter(no_dash, raw_parentfolders)]

for currentparent in parentfolders:
    for foldername, subfolders, filenames in os.walk(currentparent):
        # We don't need the './tutorials' part anymore
        tparentfolder = foldername
        foldername = foldername.split("/")[-1]

        for subfolder in subfolders:
            if (subfolder == "loops"):
                continue

            cmd = f"python ../stellar/tools/wallace.py -r stellar.sh {foldername}/{subfolder} .Wallace/{foldername}/{subfolder} 0.8"

            targetFolder = f"{tparentfolder}/{subfolder}/"
            folder = f"./tutorials/.Wallice/{foldername}/{subfolder}/"

            wallice.checkScripts("stellar.sh", targetFolder, folder, 1)
