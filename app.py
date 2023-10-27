from flask import Flask, render_template, request, flash
import requests
import json
import folium
app = Flask(__name__)


@app.route('/', methods=['GET']) #初めにURLがクリックされた時
def get():
	return render_template('index.html',location='',value='')


@app.route('/', methods=['POST'])
def post():
    location = request.form.get('location')
    url='https://api.aoikujira.com/tenki/week.php?fmt=json'
    tenki_data = requests.get(url).json()
    value = tenki_data[location] #日にちごとのリスト、1つの要素は辞書で構成されている
    loc_tup = loc(location)
    loc_lat = loc_tup[0]
    loc_lng = loc_tup[1]

    # 地図生成
    folium_map = folium.Map(location=[loc_lat, loc_lng], zoom_start=5)
    folium.Marker(location=[loc_lat, loc_lng]).add_to(folium_map)
    folium_map = folium_map._repr_html_()

    
    return render_template('index.html',location=location,value=value, map=folium_map) 

def loc(location):
    #都道府県の緯度経度データ
    prefectures =  [
    {"pref":"札幌","lat":43.064301,"lng":141.346874},
    {"pref":"旭川","lat":43.7706,"lng":142.3648},
    {"pref":"釧路","lat":42.9848,"lng":144.3813},
    {"pref":"青森","lat":40.824622,"lng":140.740598},
    {"pref":"仙台","lat":38.268812,"lng":140.872082},
    {"pref":"秋田","lat":39.718611,"lng":140.102401},
    {"pref":"宇都宮","lat":36.566672,"lng":139.883093},
    {"pref":"東京","lat":35.689753,"lng":139.691731},
    {"pref":"新潟","lat":37.902419,"lng":139.023225},
    {"pref":"金沢","lat":36.59473,"lng":136.625582},
    {"pref":"長野","lat":36.651296,"lng":138.181239},
    {"pref":"名古屋","lat":35.180344,"lng":136.906632},
    {"pref":"大阪","lat":34.686555,"lng":135.519474},
    {"pref":"松江","lat":35.472324,"lng":133.05052},
    {"pref":"広島","lat":34.396603,"lng":132.459621},
    {"pref":"高松","lat":34.340045,"lng":134.043369},
    {"pref":"高知","lat":33.5597,"lng":133.531096},
    {"pref":"福岡","lat":33.606781,"lng":130.418307},
    {"pref":"鹿児島","lat":31.560166,"lng":130.557994},
    {"pref":"奄美","lat":26.2064,"lng":127.6465},
    {"pref":"石垣","lat":13.4443,"lng":144.7937},
    {"pref":"那覇","lat":26.212418,"lng":127.680895}
    ]
    loc_lat = [ item['lat'] for item in prefectures if item['pref'] == location][0]
    loc_lng = [ item['lng'] for item in prefectures if item['pref'] == location][0]

    return loc_lat, loc_lng




if __name__ == "__main__":
    app.run()