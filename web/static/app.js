"use strict";

$(document).ready(function() {

    var polygon = $('#my-data').data('bound');
    console.log(polygon.type);

    function createMap(center, zoom) {

        var mapElem = document.getElementById('map');

        var map = new google.maps.Map(mapElem, {
            center: center,
            zoom: zoom
        });

        $(window).resize(function() {
            $('#map').css('height', $(window).height - $('#map').position().top - 20);
        });
    }

    var areaCoords = {
        lat: 41.8,
        lng: -87.6
    };

    createMap(areaCoords, 12);

});