import map_func
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from decimal import Decimal
import random


session=dict()
app = Flask(__name__)
giveId = random.randint(244,12000)



img={}
img['dog1.jpg']="https://boygeniusreport.files.wordpress.com/2016/11/puppy-dog.jpg?quality=98&strip=all&w=782"
img['harak.jpg']="https://images1.calcalist.co.il/PicServer2/20122005/531581/21.jpg"
img['risus.jpg']="https://www.gurhadbarot.com/wp-content/uploads/2015/05/%D7%A8%D7%99%D7%A1%D7%95%D7%A1-%D7%9C%D7%91%D7%99%D7%AA.jpg"
img['electric.jpg']="https://img.mako.co.il/2015/11/03/461232_I.jpg"
img['biuv.jpg']="http://www.sewerage.co.il/wp-content/uploads/2019/02/%D7%91%D7%99%D7%95%D7%91%D7%99%D7%AA-%D7%91%D7%A8%D7%9E%D7%AA-%D7%92%D7%9F.jpg"
img['car.jpg']="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Flat_tire_edited_size.jpg/250px-Flat_tire_edited_size.jpg"
img['carecar.jpg']="https://i.imagesup.co/images2/0__05c97522aaf4d2.jpg"
img['sedek.jpg']="https://agalor.co.il/wp-content/uploads/2014/11/%D7%A1%D7%93%D7%A7-%D7%91%D7%A7%D7%99%D7%A8.jpg"
img['cat.jpg']="http://www.bwoman.co.il/forums/attachment.php?attachmentid=37193&d=1555429071"
img['zevel.jpg']="https://img.mako.co.il/2008/08/13/zevel_pic_archive_c.jpg"
img['carezevel.jpg']="https://www.makorrishon.co.il/nrg/images/archive/465x349/1/709/107.jpg"
img['sapa.jpg']="https://www.cleaningsofas.com/f-users/user_107514/website_200829/images/thumbs/W_960_2fdbb198-354b-407b-886f-b1bef152e8a3_010.jpg"
img['zevel12.jpg']="https://besttv232-ynet-images1-prod.cdn.it.best-tv.com/PicServer5/2018/03/11/8398534/839852801000100640360no.jpg"
img['zevel45.jpg']="https://besttv232-ynet-images1-prod.cdn.it.best-tv.com/PicServer5/2018/03/11/8398532/839852701000100640360no.jpg"

@app.route('/')
def start():
        return render_template("page1.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        password = request.form['pass']

        conn = map_func.connect()
        cur = conn.cursor()
        sql="SELECT COUNT(*) FROM Users WHERE user_id=%s AND user_password=%s"
        cur.execute(sql,(user,password))
        a = cur.fetchone()
        count = a['COUNT(*)']
        cur.close()
        if count == 0:
            session['is_logged_in'] = '0'
            return render_template('page1.html', msg = 'שם משתמש או סיסמא אינם נכונים')

        else:
            session['is_logged_in'] = '1'
            session['user_name'] = user
            return redirect(url_for('map_start'))

@app.route('/map_start')
def map_start():
    conn = map_func.connect()
    cur = conn.cursor()

    res = []
    id = []
    open = []
    takecare = []
    check = []
    wait = []
    p = []

    sql = "SELECT * FROM alerts WHERE alert_id  IN (SELECT alert_id FROM alerts_users WHERE user_id=%s)"
    cur.execute(sql, session['user_name'])

    for row in cur:
        res.append(row['alert_id'])
        id.append(float(row['location_lat']))
        id.append(float(row['location_lng']))

    cur.execute("SELECT * FROM Alerts WHERE alert_counter >2")
    for row in cur:
        if row['alert_id'] not in res:
            if row['alert_status'] == "פתוחה":
                open.append(float(row['location_lat']))
                open.append(float(row['location_lng']))

            elif row['alert_status'] == "בטיפול":
                takecare.append(float(row['location_lat']))
                takecare.append(float(row['location_lng']))

            elif row['alert_status'] == "טופל":
                check.append(float(row['location_lat']))
                check.append(float(row['location_lng']))
            else:
                wait.append(float(row['location_lat']))
                wait.append(float(row['location_lng']))

    cur.close()
    return render_template('map.html', ids = id, open = open, takecare = takecare, check = check, wait = wait)

@app.route('/checkAround',methods=['POST'])
def checkAround():
        if request.method == 'POST':
            if (map_func.validToSay(session['user_name'])==False):
                h1="מצטערים, אינך יכול להתריע"
                p= "מספר ההתראות מוגבל לחמש ביום"
                return render_template('page6.html', type = "page10",goto_url = 'map_start',h1=h1,p=p)
            else:
                ln = request.form['lng']
                la = request.form['lat']
                laa = la[0:10]
                lnn = ln[0:10]
                lat = float(laa)
                lng = float(lnn)

                length = 0
                alerts = []
                res = []

                conn = map_func.connect()
                cur = conn.cursor()
                cur.execute("SELECT * FROM Alerts WHERE alert_status='פתוחה';")

                for row in cur:
                    if length < 3:
                        lat2 = row['location_lat']
                        lng2 = row['location_lng']
                        lat2 = float(lat2)
                        lng2 = float(lng2)
                        if (map_func.calDistance(lat, lat2, lng, lng2) == True):
                            alert = {}
                            alert['id'] = row['alert_id']
                            alert['name'] = row['alert_name']
                            alert['text'] = row['alert_text']
                            alert['pic'] = row['alert_picture']
                            alerts.append(alert)
                            length = length + 1

                cur = conn.cursor()
                sql = "SELECT alert_id FROM Alerts_users WHERE user_id=%s;"
                cur.execute(sql, session['user_name'])
                for alert in cur:
                    res.append(int(alert['alert_id']))

                cur.close()
                if length > 0:
                    return render_template('map_resault.html', length = length, alerts = alerts, reportAlerts = res,lng=lng,lat=lat)
                else:
                    return render_template('page2.html', lng = lng, lat = lat)

@app.route('/page2_start', methods = ['POST'])
def page2_():
    lng = request.form['lng']
    lat= request.form['lat']
    return render_template('page2.html', lng = lng, lat = lat)


@app.route('/page2', methods = ['POST'])
def page2_start():
    location_lng = request.form['lng']
    location_lat= request.form['lat']
    alert_name= request.form['name']
    alert_text= request.form['subject']
    pic= request.form['pic']
    if pic == "":
        alert_picture="https://www.scott-sports.com/_ui/responsive/common/images/no-product-image-available.png"
    else:
        alert_picture=img[pic]
    global giveId
    alert_id = int(giveId)
    giveId = random.randint(244, 12000)
    alert_status='פתוחה'
    alert_counter=1

    alert_type,alert_price= map_func.setTypeAndPrice(alert_name)

    conn = map_func.connect()
    cur = conn.cursor()

    # INSERT INTO ALERTS
    sql = "INSERT INTO Alerts(alert_id,alert_type,alert_name,location_lat,location_lng,alert_text,alert_status,alert_counter,alert_price,alert_picture) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sqll = "INSERT INTO Alerts(alert_id,alert_type,alert_name,location_lat,location_lng,alert_text,alert_status,alert_counter,alert_price,alert_picture) VALUES "
    cur.execute(sql, (alert_id,alert_type,alert_name,location_lat,location_lng,alert_text,alert_status,alert_counter,alert_price,alert_picture))
    conn.commit()

    # UPDATE COUNTER OF USER TO COUNTER+1
    sql = "SELECT alert_counter FROM Users WHERE user_id=%s;"
    cur.execute(sql, session['user_name'])
    a = cur.fetchone()
    count = a['alert_counter'] + 1
    sql = "UPDATE Users SET alert_counter=%s WHERE user_id=%s;"
    cur.execute(sql, (count, session['user_name']))
    conn.commit()

    # UPDATE ALERTS_USERS
    sql = "INSERT INTO Alerts_users VALUES (%s,%s);"
    sqll= "INSERT INTO Alerts_users VALUES "
    cur.execute(sql, (alert_id, session['user_name']))
    conn.commit()

    cur.close()
    h1 = "תודה לך על הדיווח"
    p = "בעוד כמה שניות תועבר למפה"
    return render_template('page6.html', type = "page10", goto_url = 'map_start', h1 = h1, p = p)

@app.route('/page3_start',methods=['POST'])
def page3_start():
    id= request.form['id']
    return render_template('page3.html', id=id)

@app.route('/page3',methods=['POST'])
def page3():

        text = request.form['subject']
        id = int(request.form['id'])
        alert_picture = request.form['pic']
        if alert_picture == "":
            pic="https://www.scott-sports.com/_ui/responsive/common/images/no-product-image-available.png"
        else:
            pic = img[alert_picture]

        conn = map_func.connect()
        cur = conn.cursor()

        #UPDATE COUNTER OF ALERT TO COUNTER+1
        sql = "SELECT alert_counter FROM Alerts WHERE alert_id=%s;"
        cur.execute(sql, id)
        a = cur.fetchone()
        count = a['alert_counter'] + 1
        sql = "UPDATE Alerts SET alert_text=%s,alert_picture=%s,alert_counter=%s WHERE alert_id=%s;"
        cur.execute(sql, (text, pic, count, id))
        conn.commit()

        #UPDATE COUNTER OF USER TO COUNTER+1
        sql = "SELECT alert_counter FROM Users WHERE user_id=%s;"
        cur.execute(sql, session['user_name'])
        a = cur.fetchone()
        count = a['alert_counter'] + 1
        sql = "UPDATE Users SET alert_counter=%s WHERE user_id=%s;"
        cur.execute(sql, (count,session['user_name']))
        conn.commit()

        #UPDATE ALERTS_USERS
        sql = "INSERT INTO Alerts_users VALUES (%s,%s);"
        cur.execute(sql,(id,session['user_name']))
        conn.commit()

        cur.close()
        h1 = "תודה לך על הדיווח"
        p = "בעוד כמה שניות תועבר למפה"
        return render_template('page6.html', type = "page10", goto_url = 'map_start', h1 = h1, p = p)



@app.route('/existAlert',methods=['POST'])
def existAlert():
    if request.method == 'POST':
        ln = request.form['lng']
        la = request.form['lat']
        laa = la[0:10]
        lnn = ln[0:10]
        lat= Decimal(laa)
        lng= Decimal(lnn)

        conn = map_func.connect()
        cur = conn.cursor()

        #GET THE ALERT WITH THIS LOCATION
        sql= "SELECT * FROM Alerts WHERE location_lat=%s and location_lng=%s;"
        cur.execute(sql,(lat,lng))
        a = cur.fetchone()
        alert_id = a['alert_id']
        alert_status = a['alert_status']
        alert_picture = a['alert_picture']
        alert_name= a['alert_name']
        alert_price= a['alert_price']
        alert_text= a['alert_text']

        res=[]


        #GET ALL ALERTS OF THIS USER
        sql = "SELECT alert_id FROM Alerts_users WHERE user_id=%s;"
        cur.execute(sql, session['user_name'])
        for alert in cur:
            res.append(int(alert['alert_id']))
        if alert_id in res:
            userKnowAlert=True
        else:
            userKnowAlert=False


        #GET NUMBER OF ALERTS OF THIS USER
        sql = "SELECT alert_counter FROM Users WHERE user_id=%s;"
        cur.execute(sql, session['user_name'])
        a = cur.fetchone()
        count = a['alert_counter']
        if count >4:
            userReport5= True
        else:
            userReport5= False

        cur.close()

        return render_template('exist.html',alert_text=alert_text,alert_price=alert_price,userKnowAlert=userKnowAlert,userReport5=userReport5,alert_name=alert_name,alert_id=alert_id, alert_status=alert_status,alert_picture=alert_picture)


@app.route('/page5',methods=['POST'])
def page5():
    id=request.form['id']
    name=request.form['name']
    price=request.form['price']
    text=request.form['name']
    return render_template('page5.html',text=text,id=id,name=name,price=price)

@app.route('/page8',methods=['POST'])
def page8():
    id=request.form['id']
    name=request.form['name']
    return render_template('page8.html',name=name,id=id)

@app.route('/page9',methods=['POST'])
def page9():
    id=request.form['id']
    pic=request.form['pic']
    pic=img[pic]

    conn = map_func.connect()
    cur = conn.cursor()


    sql = "UPDATE Alerts SET tookCare_pic=%s , alert_status=%s , alert_tookCare=%s WHERE alert_id=%s;"
    cur.execute(sql, (pic,'טופל',session['user_name'],id))
    conn.commit()

    cur.close()
    return render_template('page9.html')

@app.route('/page9_start')
def page9_sttart():
    return render_template('page9.html')


@app.route('/page4_start',methods=['POST'])
def page4_start():
    id= request.form['id']
    conn = map_func.connect()
    cur = conn.cursor()
    sql="SELECT * FROM Alerts WHERE alert_id=%s;"
    cur.execute(sql,id)
    a = cur.fetchone()
    pic = a['tookCare_pic']
    lng = a['location_lng']
    lat = a['location_lat']

    cur.close()
    return render_template('page4.html',id=id,pic=pic,lng=lng,lat=lat)

@app.route('/page7_start',methods=['POST'])
def page7():
    id=request.form['id']
    conn = map_func.connect()
    cur = conn.cursor()
    sql = "UPDATE Alerts SET alert_status=%s WHERE alert_id=%s;"
    cur.execute(sql, ('בבדיקה',id))
    conn.commit()

    cur.close()
    return render_template('page7.html')



@app.route('/methoddd', methods = ['POST'])
def mathoddd():
    lng=request.form['lng']
    lat1=request.form['lat']
    lat= float(lat1)
    lat= lat-0.0000001
    return render_template('page2.html', lng = lng, lat = lat)




if __name__ == "__main__":
    app.run(port="8888", debug=True)
