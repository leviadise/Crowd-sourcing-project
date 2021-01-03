
function myMap()
        {
        //init map
          var bound = new google.maps.LatLngBounds(new google.maps.LatLng(32.035249, 34.743347), new google.maps.LatLng(32.140813, 34.812964));
          var maprestriction= {strictBounds: true, latLngBounds: bound };
          var myLatlng = new google.maps.LatLng(32.070340, 34.775972);
          var mapProp= {center:myLatlng, zoom:15, restriction: maprestriction};
          var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
      }

