import os
import threading
import time
import json
import sys
import pygame
import keyboard
import requests

pygame.init()

def timeStampMS(timenum):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum / 1000)))

class n_api:
    temp_loca = os.getcwd()+"/"
    api_url = "http://cloud-music.pl-fe.cn/"
    api_netease_url = "http://music.163.com/api/"
    wyy_headframe = "http://p1.music.126.net/_f_ggnXfNN-PndOZnahjng==/"
    wyy_outer = "http://music.163.com/song/media/outer/url?id={}.mp3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    api_songsearch = ""
    playing_song_j = None
    songs = []
    autorelease = True
    class isloop:
        a = 0
        b = 1
    class apilist:
        pass

def release_temp():
    try:
        for root, dirs, files in os.walk(n_api.temp_loca):
            for name in files:
                if name.endswith(".mp3"):
                    os.remove(os.path.join(root, name))
    except Exception: pass

def search_song(s_name):
    apihead = n_api.api_url + "search?keywords="
    var = apihead + s_name
    req = requests.get(url=var, headers=n_api.headers)
    return req.text.__str__()

def send_n_back(URL):
    return requests.get(url=URL, headers=n_api.headers).text.__str__()

def player_play():
    songid = n_api.playing_song_j["id"].__str__()
    if not os.path.exists(n_api.temp_loca+"/.temp"+songid+".mp3"):
        r = requests.get(n_api.wyy_outer.format(songid)).content
        with open(n_api.temp_loca+"/.temp"+songid+".mp3", "wb+") as file:
            file.write(r)
            file.flush()
        pygame.mixer.music.load(n_api.temp_loca+"/.temp"+songid+".mp3")
        pygame.mixer.music.play(n_api.isloop.a, n_api.isloop.b)
    else:
        pygame.mixer.music.unpause()

def player_stop():
    pygame.mixer.music.stop()


def on_press():
    start_input()


def start_input():
    while 1:
        inp = input("")
        j = []
        var_s = []
        var_t = ""
        for i in range(0, len(inp)):
            var_s.append(inp[i])
            var_t += inp[i]
        if ':' in var_s:
            var_t = var_t.split()
            j = var_s
            if j[0] == ":":
                j.pop(0)
                if var_t == "" or var_t == None:
                    if 'p' in j:
                        player_play()
                    if 's' in j:
                        player_stop()
                    if 'q' in j:
                        raise SystemExit
                else:
                    if ":play" in var_t:
                        player_play()
                    if ":stop" in var_t:
                        player_stop()
                    if ":quit" in var_t:
                        raise SystemExit
                    if ":search" in var_t:
                        if "byname" == var_t[1]:
                            whatisearched = ""
                            if len(var_t) > 2:
                                for k in range(2, len(var_t)):
                                    whatisearched += " " + var_t[k]
                            else:
                                whatisearched = var_t[1]
                            n_api.api_songsearch = json.loads(search_song(whatisearched))
                            n_api.songs = n_api.api_songsearch["result"]["songs"]
                            #n_api.api_songsearch = json.loads(open('shit.json', 'r').read())
                        if "list" == var_t[1]:
                            if len(var_t) > 2:
                                if "o" == var_t[2] or "original" == var_t[2]:
                                    print(n_api.api_songsearch["result"])
                            else:
                                songs = n_api.api_songsearch["result"]["songs"]
                                for name in range(0, len(songs)):
                                    songs_author = ""
                                    for j in range(0, len(songs[name]["artists"])):
                                        songs_author += songs[name]["artists"][j]["name"].__str__()+" & "
                                    print((name+1).__str__() + (5 - len(name.__str__())) * " " + "| "+songs[name]["name"].__str__()+" | "+songs_author.__str__()[:-2]+" ???"+songs[name]["album"]["name"].__str__()+"??? "+songs[name]["duration"].__str__())
                    if ":proxy" in var_t:
                        if "set" == var_t[1]:
                            if not None == var_t[2] or not "" == var_t[2]:
                                n_api.api_url = var_t[2]
                        if "show" == var_t[1]:
                            print(n_api.api_url)
                    if ":select" in var_t:
                        try:
                            n_api.playing_song_j = n_api.songs[int(var_t[1])-1]
                        except Exception:
                            print("ERROR")
                    if ":pause" in var_t:
                        pygame.mixer.music.pause()
                    if ":player" in var_t:
                        if "loop" in var_t[1]:
                            n_api.isloop.a = 1
                            n_api.isloop.b = 1
                        if "unloop" in var_t[1]:
                            n_api.isloop.a = 0
                            n_api.isloop.b = 1
                        if "init" == var_t[1]:
                            if "IKNOWWHATIDOTHAT" == var_t[2]:
                                pygame.init()
                                pygame.mixer.music.unload()
                        if "release" == var_t[1]:
                            try:
                                release_temp()
                                os.system("start del /s /q *.mp3")
                                os.system("start rm -rf *.mp3")
                            except Exception: pass
                    if ":info" in var_t:
                        if len(var_t) >= 2:
                            if var_t[1] == "play":
                                songs = n_api.playing_song_j
                                print("\n")
                                print("?????????: " + songs["name"] + " | ??????ID: " + songs["id"].__str__())
                                # ???????????? & ????????????:
                                req = n_api.api_netease_url+"song/detail/?id="+songs["id"].__str__()+"&ids=%5B"+songs["id"].__str__()+"%5D"
                                songinfo_j = json.loads(send_n_back(req))["songs"][0]
                                print("Disc: "+songinfo_j["disc"].__str__()+" | No. "+songinfo_j["no"].__str__())
                                print("????????????: "+songinfo_j["starred"].__str__() + " | ?????????: "+songinfo_j["popularity"].__str__() + " | ??????(?????????????????????????????????): "+songinfo_j["score"].__str__())
                                print("????????????: "+songinfo_j["starredNum"].__str__() + " | ????????????: "+songinfo_j["playedNum"].__str__() + " | ???????????????: "+songinfo_j["dayPlays"].__str__() + " | ????????????: "+songinfo_j["hearTime"].__str__())
                                print("????????????: "+songinfo_j["transName"].__str__()+ " | ????????????: "+songinfo_j["alias"])
                                for artists in range(0, len(songs["artists"])):
                                    artist_ = songs["artists"][artists]
                                    print("??????????????? (" + (artists + 1).__str__() + ") : " + artist_[
                                        "name"].__str__() + " | ID: " + artist_["id"].__str__() + " | ????????????: " +
                                          artist_["img1v1Url"] + " | ?????????: " + artist_["fansGroup"].__str__().replace("None", "???") + " | ????????????: "+artist_["alias"].__str__())
                                album__ = songinfo_j["album"]
                                album_ = songs["album"]
                                print("????????????: " + album_["name"] + " | ??????ID: " + album_["id"].__str__() + " | ????????????: " + timeStampMS(album_["publishTime"]).__str__())
                                print("????????????: " + album__["picUrl"].__str__() + " | ????????????: "+album__["type"] + " | ????????????/??????: "+album__["company"].__str__().replace("None", "???")+" ("+album__["companyId"].__str__()+")")
                                print("????????????: "+album__["subType"].__str__() + " | ????????????(??????): "+album__["onSale"].__str__().replace("False", "???").replace("True", "???") + " | ????????????: "+album__["dolbyMark"].__str__().replace("0", "?????????").replace("1", "??????"))
                                print("\n")
                            elif var_t[1] == "singer" or var_t[1] == "user":
                                usngr_j = json.loads(requests.get(url=n_api.api_netease_url + "artist/albums/" + var_t[2] + "?id=" + var_t[2] + "&offset=0&total=true&limit=10", headers=n_api.headers).text)["artist"]
                                print("????????????: " + usngr_j["name"] + " | ????????????: " + usngr_j["alias"].__str__())
                                print(
                                    "?????????: " + usngr_j["followed"].__str__().replace("False", "??").replace("True",
                                                                                                             "???") + " | ????????????: " +
                                    usngr_j["albumSize"].__str__() + " | ????????????: " + usngr_j[
                                        "musicSize"].__str__())
                                print("\n")
                            else:
                                try:
                                    print(n_api.songs[int(var_t[1])-1])
                                except Exception: pass
                break
        else:
            if '@' in var_s:
                j = inp.split()
                if "@search" in j:
                    n_api.api_songsearch = search_song(j[1])
                if "@proxy" in j:
                    if "set" == j[1]:
                        if not None == j[2] or not "" == j[2]:
                            n_api.api_url = j[2]
                    if "show" == j[1]:
                        print(n_api.api_url)
        break


if __name__ == "__main__":
    while 1:
        keyboard.add_hotkey("esc", on_press)
        keyboard.wait()
        raise SystemExit
    # thr_input = threading.Thread(target=on_press)
    # thr_input.start()

