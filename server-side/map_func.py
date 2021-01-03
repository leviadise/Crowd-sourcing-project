import numpy
import math
import pymysql
from flask import Flask, render_template, request, redirect, url_for
iconBase ='https://developers.google.com/maps/documentation/javascript/examples/full/images/';


def calDistance(lat1,lat2,long1,long2):
    theta = long1 - long2;
    distance = numpy.sin(numpy.deg2rad(lat1)) * numpy.sin(numpy.deg2rad(lat2)) + numpy.cos(
        numpy.deg2rad(lat1)) * numpy.cos(numpy.deg2rad(lat2)) * numpy.cos(numpy.deg2rad(theta))
    distance = math.acos(distance)
    distance = numpy.rad2deg(distance)
    distance = distance * 60 * 1.1515
    distance = distance * 1.609344
    distance = round(distance, 2)
    if (distance<0.1):
        return True

def validToSay(user):
    conn=connect()
    cur = conn.cursor()
    sql = "SELECT alert_counter FROM Users WHERE user_id=%s"
    cur.execute(sql, user)
    temp = cur.fetchone()
    count = temp['alert_counter']
    cur.close()
    if count >4:
        return False
    else:
        return True

def setTypeAndPrice(alert_name):
    if alert_name == "חיה זקוקה לעזרה":
        alert_type='animal'
        alert_price=2
    elif alert_name == "נפילת מתח חשמל":
        alert_type='electric'
        alert_price=0
    elif alert_name == "חרקים":
        alert_type='insect'
        alert_price=5
    elif alert_name == "זבל":
        alert_type='junk'
        alert_price=5
    elif alert_name == "כביש":
        alert_type='road'
        alert_price=0
    elif alert_name == "ביוב":
        alert_type='sewadge'
        alert_price=10
    elif alert_name == "רכב":
        alert_type='tow'
        alert_price=10
    else:
        alert_type='other'
        alert_price=0

    return alert_type,alert_price

def connect():
    return pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', password = 'tova2020',
                           database = "crowdSourcing", charset = 'utf8mb4',
                           cursorclass = pymysql.cursors.DictCursor)

def getIcon(alert_name):
    if alert_name == "חיה זקוקה לעזרה":
        iconBase="https://img.icons8.com/android/24/000000/cat-footprint.png"
    elif alert_name == "נפילת מתח חשמל":
        iconBase="https://img.icons8.com/officexs/16/000000/high-risk.png"
    elif alert_name == "זבל":
        iconBase="https://img.icons8.com/metro/26/000000/trash.png"
    elif alert_name == "כביש":
        iconBase="http://maps.google.com/mapfiles/kml/shapes/caution.png"
    elif alert_name == "ביוב":
        iconBase="https://img.icons8.com/ios-filled/50/000000/water-pipe.png"
    elif alert_name == "רכב":
        iconBase="https://img.icons8.com/android/24/000000/tow-truck.png"
    else:
        iconBase="https://img.icons8.com/officexs/40/000000/map-pin.png"

    return iconBase
