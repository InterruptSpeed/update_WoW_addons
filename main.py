from urllib.request import urlopen
import zipfile
import shutil
import os
import sys

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def download_to_file(src_url, dest_filepath):
    response = urlopen(src_url)
    data = response.read()

    # Write data to file
    file_ = open(dest_filepath, 'wb')
    file_.write(data)
    file_.close()

def unzip_file(src_filepath, dest_filepath):
    zip_ref = zipfile.ZipFile(src_filepath, 'r')
    zip_ref.extractall(dest_filepath)
    zip_ref.close()

if __name__ == '__main__':
    if not "WOW_HOME" in os.environ:
        sys.exit("Set WOW_HOME environment variable to the location of your World of Warcraft directory.")
    
    addon_home = os.environ['WOW_HOME'] + "/Interface/AddOns"
    print("Updating " + addon_home)

    tmp_path = "tmp/"

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path, 755)

    # obviously this should be loaded from a file and looped over and/or done concurrently
    download_to_file("https://addon.theunderminejournal.com/TheUndermineJournal.zip", tmp_path + "/TheUndermineJournal.zip")
    unzip_file(tmp_path + "/TheUndermineJournal.zip", tmp_path)
    copy_and_overwrite(tmp_path + "/TheUndermineJournal", addon_home + "/Interface/AddOns/TheUndermineJournal")
    print(addon_home + "/TheUndermineJournal updated!")

    download_to_file("https://www.curseforge.com/wow/addons/auctionator/download/2609812/file", tmp_path + "/Auctionator.zip")
    unzip_file(tmp_path + "/Auctionator.zip", tmp_path)
    copy_and_overwrite(tmp_path + "/Auctionator", addon_home + "/Auctionator")
    print(addon_home + "/Auctionator updated!")

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)