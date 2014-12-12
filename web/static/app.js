"use strict";

$(document).ready(function() {

    var area_name = $('#my-data').data('name');
    var map;

    console.log(area_name);

    function createMap(mapOptions) {

        var mapElem = document.getElementById('map');

        map = new google.maps.Map(mapElem, mapOptions);

        $(window).resize(function() {
            $('#map').css('height', $(window).height - $('#map').position().top - 20);
        });

        var marker = new google.maps.Marker({
            position: mapOptions.center,
            title: area_name,
            map: map,
            animation: google.maps.Animation.DROP
        });

        var area_bound = $('#my-data').data('bound');

        console.log(area_bound);

        map.data.addGeoJson(JSON.parse(area_bound));

        var featureStyle = {
            fillColor: 'green',
            strokeWeight: 1
        };




//        var i;
//
//        var polygonPath = [];
//
//        for (var idx = 0; idx < coordArray.length; ++idx) {
//            var lat = coordArray[idx][1].toFixed(6);
//            var lng = coordArray[idx][0].toFixed(6);
//            var latLng = new google.maps.LatLng(lat, lng);
//            polygonPath.push(latLng);
//        }
//
//        var boundaryPolygon = new google.maps.Polygon({
//            paths: polygonPath,
//            strokeColor: '#FF0000',
//            strokeOpacity: 0.8,
//            strokeWeight: 2,
//            fillColor: '#FF0000',
//            fillOpacity: 0.35
//        });
//
//        boundaryPolygon.setMap(map);
    }

    var geocoder = new google.maps.Geocoder();

    var addr = area_name + ', Chicago, IL';

    geocoder.geocode({address: addr}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            // results is an array of possible matches
            // coordinates for each are in geometry.location;
            var coords = results[0].geometry.location;
        }

        var mapOptions = {
            center: coords,
            zoom: 12
        };

        createMap(mapOptions);
    });

});
