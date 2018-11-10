<html>
    <head>
        <style>
           #map {
            width: 600px;
            height: 400px;
          }
        </style>
        <title>Lion -  Trajectories </title>
    </head>
    <body>
        <div id="map"></div>
        <script>
        var cnt = 1;
          function initMap() {
            var lat = -1.227;
            var lng = 35.10476;
            var markers = [];
            var mapDiv = document.getElementById('map');
            var map = new google.maps.Map(mapDiv, {
                center: {lat: -1.227, lng: 35.10476},
                zoom: 8
            });

            // seed initial conditions
            var markers = [
                    ['lion1', -1.22738, 35.1048],
                    ['lion2', -2.22738, 35.1048],
                    ['lion31', -1.22738, 35.1048],
                    ['lion32', -1.22738, 34.1048],
                    ['lion33', -1.22738, 35.1048],
                    ['lion34', -2.22738, 35.1048],
                    ['lion35', -2.22738, 35.1048],
                    ['lion36', -1.22738, 35.1048],
                    ['lion37', -1.22738, 34.1048],
                    ['lion38', -1.22738, 35.1048],
                    ['lion39', -1.22738, 35.1048],
                    ['lion40', -2.22738, 35.1048],
                    ['lion41', -1.22738, 35.1048],
                    ['lion42', -1.22738, 35.1048],
            ];

            var gmarkers = [];
            for( i = 0; i < markers.length; i++ ) {
                var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
                //bounds.extend(position);
                marker = new google.maps.Marker({
                    position: position,
                    map: map,
                    title: markers[i][0],
                    icon: '/static/lion-icon.png'
                    });
                    gmarkers.push(marker);
                }
                gmarkers[0].setMap(map);
                var startTime = new Date().getTime();

                for (j = 0; j < gmarkers.length; j++) // move each marker sequentially
                {
                    moveMarker(map, gmarkers[j], lat, lng, startTime);
                }
            } 

            function moveMarker( map, marker, lat, lng, limit) 
            {    
                setInterval( function(){ 
                     lat = lat + (Math.random()/100);
                     lng = lng + (Math.random()/100);
                     marker.setPosition(new google.maps.LatLng(lat, lng));
                     self.cnt += 1;
                 }, 1000 );
            };
         </script>
         <script async defer
             src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA7FuiuBWpIFKQNdUAE0aBAjRsPpTsZqC8&callback=initMap">
         </script>
    </body>
</html>
