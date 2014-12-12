"use strict";

$(document).ready(function() {

    var geocoder = new google.maps.Geocoder();

    var area_bound = $('#my-data').data('bound');
    var area_name = $('#my-data').data('name');

    var addr = area_name + ', Chicago, IL';
    var coords;
    geocoder.geocode({address: addr}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            // results is an array of possible matches
            // coordinates for each are in geometry.location;
            coords = results[0].geometry.location;
        }

        var center = [coords.lat(), coords.lng()];

        var map = L.map('map').setView(center, 12);

        L.tileLayer('http://{s}.tiles.mapbox.com/v3/emnetag.kf9mpi42/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; [...]',
            maxZoom: 12
        }).addTo(map);

        L.geoJson(area_bound.features).addTo(map);
    });


});