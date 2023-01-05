import os
import threading
import time
import json
import pyglet
import requests

# 别问，实在太害怕代码档掉采用的这么多try except QWQ


pyglet.options['audio'] = ("openal", "directsound", "silent")
pyglet.options['search_local_libs'] = True


def timeStampMS(timenum):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum / 1000)))


resources_player = pyglet.media.Player()


class n_api:
    temp_loca = os.getcwd() + "/"
    api_url = "http://cloud-music.pl-fe.cn/"
    api_netease_url = "http://music.163.com/api/"
    wyy_headframe = "http://p1.music.126.net/_f_ggnXfNN-PndOZnahjng==/"
    wyy_outer = "http://music.163.com/song/media/outer/url?id={}.mp3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"
    }
    api_songsearch = ""
    playing_song_j = None
    songs = {}
    autorelease = True
    music_obj = None

    class isloop:
        a = 0
        b = 1

    class apilist:
        pass


def release_temp():
    try:
        resources_player.delete()
        for root, dirs, files in os.walk(n_api.temp_loca):
            for name in files:
                if name.endswith(".mp3"):
                    os.remove(os.path.join(root, name))
    except Exception:
        pass

def searcher(s_name, s_type):
    if s_type == "song":
        # apihead = n_api.api_url + "search?keywords="
        # var = apihead + s_name
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1&offset=0&total=true&limit=20"
    elif s_type == "album":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=10&offset=0&total=true&limit=20"
    elif s_type == "singer":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=100&offset=0&total=true&limit=20"
    elif s_type == "songlist":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1000&offset=0&total=true&limit=20"
    elif s_type == "user":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1002&offset=0&total=true&limit=20"
    elif s_type == "mv":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1004&offset=0&total=true&limit=20"
    elif s_type == "lyric":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1006&offset=0&total=true&limit=20"
    elif s_type == "djradio":
        var = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=" + s_name + "&type=1009&offset=0&total=true&limit=20"
    else:
        print("错误的搜索类型")
    req = requests.get(url=var, headers=n_api.headers)
    return req.text.__str__()

def send_n_back(URL):
    return requests.get(url=URL, headers=n_api.headers).text.__str__()


def downloader(songid):
    try:
        r = requests.get(n_api.wyy_outer.format(songid)).content
        with open(n_api.temp_loca + "/.temp" + songid + ".mp3", "wb+") as file:
            file.write(r)
            file.flush()
    except Exception:
        pass


def player_play():
    try:
        songid = n_api.playing_song_j["id"].__str__()
        if not os.path.exists(n_api.temp_loca + "/.temp" + songid + ".mp3"):
            downloader(songid)
            resources_player.queue(pyglet.media.load(n_api.temp_loca + "/.temp" + songid + ".mp3"))
            # resources_player.queue(load(n_api.wyy_outer.format(songid)))
            resources_player.play()
        else:
            resources_player.play()
    except Exception:
        print("资源加载错误或者事付费曲")


def player_resume():
    try:
        resources_player.play()
    except Exception:
        print("ERROR")


def player_stop():
    try:
        resources_player.delete()
    except Exception:
        print("无法释放资源")


def on_press():
    start_input()


def getsong_info(songs):
    try:
        print("歌曲名: " + songs["name"] + " | 歌曲ID: " + songs["id"].__str__())
        # 歌曲详情 & 专辑详情:
        req = n_api.api_netease_url + "song/detail/?id=" + songs["id"].__str__() + "&ids=%5B" + songs[
            "id"].__str__() + "%5D"
        songinfo_j = json.loads(send_n_back(req))["songs"][0]
        print("Disc: " + songinfo_j["disc"].__str__() + " | No. " + songinfo_j["no"].__str__())
        print("星标音乐: " + songinfo_j["starred"].__str__() + " | 热门度: " + songinfo_j["popularity"].__str__()[:-2].join("%") + " | 分数(和热门度差不了多少意思): " + songinfo_j["score"].__str__())
        print("星标数量: " + songinfo_j["starredNum"].__str__() + " | 播放次数: " + songinfo_j["playedNum"].__str__() + " | 日播放次数: " + songinfo_j["dayPlays"].__str__() + " | 播放时长: " +songinfo_j["hearTime"].__str__())
        print("歌曲译名: " + songinfo_j["transName"].__str__() + " | 歌曲别名: " + songinfo_j["alias"].__str__().replace("[]", "无"))
        for artists in range(0, len(songs["artists"])):
            artist_ = songs["artists"][artists]
            print("参演艺术家 (" + (artists + 1).__str__() + ") : " + artist_["name"].__str__() + " | ID: " + artist_["id"].__str__() + " | 个人头像: " + artist_["img1v1Url"] + " | 粉丝团: " + artist_["fansGroup"].__str__().replace("None","无") + " | 歌手别名: " + artist_["alias"].__str__().replace("[]", "无"))
        album__ = songinfo_j["album"]
        album_ = songs["album"]
        print("歌曲专辑: " + album_["name"] + " | 专辑ID: " + album_["id"].__str__() + " | 发行时间: " + timeStampMS(album_["publishTime"]).__str__())
        print("专辑图片: " + album__["picUrl"].__str__() + " | 专辑类型: " + album__["type"] + " | 发行公司/厂牌: " +album__["company"].__str__().replace("None", "无") + " (" + album__["companyId"].__str__() + ")")
        print("专辑类型: " + album__["subType"].__str__() + " | 是否售卖(打折): " + album__["onSale"].__str__().replace("False", "否").replace("True", "是") + " | 杜比音频: " + album__["dolbyMark"].__str__().replace("0","不支持").replace("1", "支持"))
    except Exception:
        print("获取详情信息失败")

def lyrisFormater(songs):
    try:
        # https://music.163.com/api/song/lyric?id={歌曲ID}&lv=1&kv=1&tv=-1
        req = n_api.api_netease_url + ""
        songs
    except Exception: pass

def aa(var_t):
    whatisearched = ""
    if len(var_t) > 2:
        for k in range(2, len(var_t)):
            whatisearched += " " + var_t[k]
    else:
        whatisearched = var_t[1]
    return whatisearched

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
                        if "songs" == var_t[1] or "song" == var_t[1] or "sng" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "song"))
                            n_api.songs = n_api.api_songsearch["result"]["songs"]
                            # n_api.api_songsearch = json.loads(open('shit.json', 'r').read())
                        if "albums" == var_t[1] or "album" == var_t[1] or "abm" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "album"))
                            print(searcher(aa(var_t), "album"))
                        if "singers" == var_t[1] or "singer" == var_t[1] or "sgr" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "singer"))
                            print(n_api.api_songsearch)
                        if "songlists" == var_t[1] or "songlist" == var_t[1] or "slt" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "songlist"))
                            print(n_api.api_songsearch)
                        if "users" == var_t[1] or "user" == var_t[1] or "usr" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "user"))
                            print(n_api.api_songsearch)
                        if "mvs" == var_t[1] or "mv" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "mv"))
                            print(n_api.api_songsearch)
                        if "lyrics" == var_t[1] or "lyric" == var_t[1] or "lyc" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "lyric"))
                            print(n_api.api_songsearch)
                        if "djradios" == var_t[1] or "djradio" == var_t[1] or "rdo" == var_t[1] or "radio" == var_t[1] or "radios" == var_t[1]:
                            n_api.api_songsearch = json.loads(searcher(aa(var_t), "djradio"))
                            print(n_api.api_songsearch)

                        if "list" == var_t[1]:
                            if len(var_t) > 2:
                                if "o" == var_t[2] or "original" == var_t[2]:
                                    print(n_api.api_songsearch["result"])
                            else:
                                songs = n_api.api_songsearch["result"]["songs"]
                                for name in range(0, len(songs)):
                                    songs_author = ""
                                    for j in range(0, len(songs[name]["artists"])):
                                        songs_author += songs[name]["artists"][j]["name"].__str__() + " & "
                                    print((name + 1).__str__() + (5 - len(name.__str__())) * " " + "| " + songs[name][
                                        "name"].__str__() + " | " + songs_author.__str__()[:-2] + " 《" +
                                          songs[name]["album"]["name"].__str__() + "》 " + songs[name][
                                              "duration"].__str__())
                    if ":proxy" in var_t:
                        if "set" == var_t[1]:
                            if not None == var_t[2] or not "" == var_t[2]:
                                n_api.api_url = var_t[2]
                        if "show" == var_t[1]:
                            print(n_api.api_url)
                    if ":select" in var_t:
                        try:
                            n_api.playing_song_j = n_api.songs[int(var_t[1]) - 1]
                        except Exception:
                            print("ERROR")
                    if ":pause" in var_t:
                        resources_player.pause()
                    if ":player" in var_t:
                        if "loop" in var_t[1]:
                            n_api.isloop.a = 1
                            n_api.isloop.b = 1
                        if "unloop" in var_t[1]:
                            n_api.isloop.a = 0
                            n_api.isloop.b = 1
                        if "init" == var_t[1]:
                            if "IKNOWWHATIDOTHAT" == var_t[2]:
                                resources_player.delete()
                        if "release" == var_t[1]:
                            try:
                                release_temp()
                                os.system("start del /s /q *.mp3")
                                os.system("start rm -rf *.mp3")
                            except Exception:
                                pass
                    if ":info" in var_t:
                        if len(var_t) >= 2:
                            if var_t[1] == "play":
                                getsong_info(n_api.playing_song_j)
                            elif var_t[1] == "singer" or var_t[1] == "user":
                                usngr_j = json.loads(requests.get(
                                    url=n_api.api_netease_url + "artist/albums/" + var_t[2] + "?id=" + var_t[
                                        2] + "&offset=0&total=true&limit=10", headers=n_api.headers).text)["artist"]
                                print("艺人名字: " + usngr_j["name"] + " | 艺人别名: " + usngr_j["alias"].__str__())
                                print(
                                    "已关注: " + usngr_j["followed"].__str__().replace("False", "×").replace("True",
                                                                                                             "√") + " | 专辑数量: " +
                                    usngr_j["albumSize"].__str__() + " | 歌曲数量: " + usngr_j[
                                        "musicSize"].__str__())
                                print("\n")
                            else:
                                try:
                                    getsong_info(n_api.songs[int(var_t[1]) - 1])
                                except Exception:
                                    pass
                    if ":resume" in var_t: player_resume()
                    if ":next" in var_t:
                        if len(var_t) > 1:
                            j = var_t
                            j.pop(0)
                            tmp = j
                            try:
                                for i in range(0, len(tmp)):
                                    song = n_api.songs[int(tmp[i]) - 1]["id"].__str__()
                                    downloader(song)
                                    resources_player.queue(pyglet.media.load(n_api.temp_loca + "/.temp" + song + ".mp3"))
                                print("% next posted")
                            except Exception:
                                print("ERROR: \ntmp:" + tmp.__str__() + "\nvar_t:" + var_t.__str__())
                break


def waitfor():
    while 1:
        # keyboard.add_hotkey("esc", on_press)
        # keyboard.wait()
        # raise SystemExit
        on_press()


if __name__ == "__main__":
    aaff = threading.Thread(target=waitfor)
    aaff.start()
    pyglet.app.run()

    # thr_input = threading.Thread(target=on_press)
    # thr_input.start()
