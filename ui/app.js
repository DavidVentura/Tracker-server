const CLOCK = 'icons/clock.png';
const NOW = 'icons/icons8-Realtime Protection-15.png';
const getData = (url) => {
    return fetch(url).then(
        res => {
            if (res.ok) {
                return res.json();
            }
        }
    )
}
const userConfig = [
    {
        icon: 'icons/blue-icon.png',
        colors: [ '#0C3E89', '#C6DDFF' ],
    },
    {
        icon: 'icons/pink-icon.png',
        colors: [ '#754668', '#C0AABA' ],
    },
];

const formatTime = timestamp => {
    let offset = new Date().getTimezoneOffset()*60*1000;
    let date = new Date(timestamp*1000 - offset);
    let hours = date.getHours();
    let minutes = "0" + date.getMinutes();
    return `${hours}:${minutes.substr(-2)}`;
    //return date;
}

const generateColors = (steps, color) => {
    let rainbow = new Rainbow();
    rainbow.setNumberRange(0, steps);
    rainbow.setSpectrum(color[0], color[1]);
    return rainbow;
}

const img = (src, cssClass = 'tracker_clock') => `<img src="${CLOCK}" class="${cssClass}">`;

const generatePoint = (pt, color) => {
    let point = L.circleMarker(pt, {
        color: `#${color}`,
        weight: 1,
        fillColor: `#${color}`,
        fillOpacity: 1,
        radius: 5,
    });
    point.addTo(mymap);
    point.bindPopup(`<p>${img(CLOCK)}: ${formatTime(pt[2])}</p>`)
}

const drawPath = (ls, config) => {
    let rainbow = generateColors(ls.length, config.colors);
    let icon = L.icon({ iconUrl: config.icon, iconSize: [30, 45], iconAnchor: [15, 45] });
    L.polyline(ls, { color: config.colors[1] }).addTo(mymap);
    ls.forEach((pt, idx) => {
        generatePoint(pt, rainbow.colorAt(idx))
    })
    let marker = L.marker(ls[0], {icon: icon}); 
    marker.addTo(mymap);
    marker.bindPopup(`<p>${img(NOW)}: ${formatTime(ls[0][2])}</p>`)
}


var mymap = L.map('mapid').setView([-34.590, -58.432], 15);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    id: 'mapbox.streets'
}).addTo(mymap);

const urls = [
    "https://tracker.davidventura.com.ar/track/ce756f3b-475d-4c60-845b-6313c3d9869a",
    "https://tracker.davidventura.com.ar/track/b4bc2e49-9050-4d28-8f39-087ed5360a3d",
    //"https://tracker.davidventura.com.ar/track/7311fb27-98ba-40a7-b0ce-6eb9783b0060"
];
const colors = ['#0000bb', '#bb0000', '#000000'];

let rainbow = new Rainbow();
console.log(rainbow);
rainbow.set
for(let idx in urls) {
    url = urls[idx];
    getData(url).then(res => {
        console.log(res);
        if (res.ls.length > 0) {
            drawPath(res.ls, userConfig[idx]);
        }
        // L.polyline(res.ls, { color: colors[idx] }).addTo(mymap);
        // L.marker(res.ls[0]).addTo(mymap);
        // for(let item of res.ls){
        //     L.circleMarker(item, {
        //         color: colors[idx],
        //         fillColor: colors[idx],
        //         fillOpacity: 0.5,
        //         radius: 5
        //     }).addTo(mymap);
        // }
    })
}
