"use strict";

$(document).ready(function() {

    var polygon = $('#my-data').data('bound');
    console.log(polygon);

    var map;

    function createMap(center, zoom) {

        var mapElem = document.getElementById('map');

        map = new google.maps.Map(mapElem, {
            center: center,
            zoom: zoom
        });

        $(window).resize(function() {
            $('#map').css('height', $(window).height - $('#map').position().top - 20);
        });

        map.data.addGeoJson(polygon);

        map.data.setStyle({
            fillColor: 'green',
            strokeWeight: 1
        });
    }

    var areaCoords = {
        lat: 41.8,
        lng: -87.6
    };

    function loadGeoJsonString(geoString) {
        var geojson = JSON.parse(geoString);
        map.data.addGeoJson(geojson);
    }

    createMap(areaCoords, 9);

});
