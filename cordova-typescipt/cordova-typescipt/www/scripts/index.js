// For an introduction to the Blank template, see the following documentation:
// http://go.microsoft.com/fwlink/?LinkID=397704
// To debug code on page load in cordova-simulate or on Android devices/emulators: launch your app, set breakpoints, 
// and then run "window.location.reload()" in the JavaScript Console.
(function () {
    "use strict";

    document.addEventListener( 'deviceready', onDeviceReady.bind( this ), false );

    var paired = false;
    var paired_device_id = "";
    var pass = "";

    //Setup Buttons
    var grid_x = 3;
    var grid_y = 5;

    var buttons = null;

    function onDeviceReady() {
        // Handle the Cordova pause and resume events
        document.addEventListener('pause', onPause.bind(this), false);
        document.addEventListener('resume', onResume.bind(this), false);

        var storage = window.localStorage;

        paired = storage.getItem("paired");
        if (paired == null || paired == "false") {
            paired = false;
        } else {
            paired = true;
        }

        paired_device_id = storage.getItem("paired_device_id");
        if (paired_device_id == null) {
            paired_device_id = "";
        }
        pass = storage.getItem("pass");
        if (pass == null) {
            pass = "";
        }
        grid_x = storage.getItem("grid_x");
        if (grid_x == null) {
            grid_x = 3;
        }
        grid_y = storage.getItem("grid_y");
        if (grid_y == null) {
            grid_y = 5;
        }

        storage.setItem("paired", "true");
        paired = true;
        paired_device_id = "T2sWMJ8aR1SNBSuUg7xxUHA9M8a";



        var uuid = device.uuid;

        //storage.setItem(key, value)
        setupButtons();

        var zeroconf = cordova.plugins.zeroconf;

        if (paired) {
            console.log("watching");
            zeroconf.watch('_pmdeckdiscovery._tcp.', 'local.', function (result) {
                var action = result.action;
                var service = result.service;
                if (action == 'added') {
                    console.log('service added', service);
                } else if (action == 'resolved') {
                    console.log('service resolved', service);
                    /* service : {
                    'domain' : 'local.',
                    'type' : '_http._tcp.',
                    'name': 'Becvert\'s iPad',
                    'port' : 80,
                    'hostname' : 'ipad-of-becvert.local',
                    'ipv4Addresses' : [ '192.168.1.125' ], 
                    'ipv6Addresses' : [ '2001:0:5ef5:79fb:10cb:1dbf:3f57:feb0' ],
                    'txtRecord' : {
                        'foo' : 'bar'
                    } */
                    console.log(service.txtRecord);
                    console.log(device.uuid);
                    if (service.txtRecord.uid == paired_device_id) {
                        connect(service.ipv4Addresses[0], service.port, function (socket) {
                            sendString(socket, "CONN:" + device.uuid + ";");

                        });
                    }
                } else {
                    console.log('service removed', service);
                }
            });
        } else {
            //watch for pairing
            console.log("watching for pairing");
            zeroconf.watch('_pmdeckpairing._tcp.', 'local.', function (result) {
                var action = result.action;
                var service = result.service;
                if (action == 'added') {
                    console.log('service added', service);
                } else if (action == 'resolved') {
                    console.log('service resolved', service);
                    /* service : {
                    'domain' : 'local.',
                    'type' : '_http._tcp.',
                    'name': 'Becvert\'s iPad',
                    'port' : 80,
                    'hostname' : 'ipad-of-becvert.local',
                    'ipv4Addresses' : [ '192.168.1.125' ], 
                    'ipv6Addresses' : [ '2001:0:5ef5:79fb:10cb:1dbf:3f57:feb0' ],
                    'txtRecord' : {
                        'foo' : 'bar'
                    } */
                    console.log(service.txtRecord);
                    tryuid = service.txtRecord.uid;

                    connect(service.ipv4Addresses[0], service.port);
                } else {
                    console.log('service removed', service);
                }
            });
        }
        

        cordova.plugins.barcodeScanner.scan(
            function (result) {
                console.log("We got a barcode\n" +
                    "Result: " + result.text + "\n" +
                    "Format: " + result.format + "\n" +
                    "Cancelled: " + result.cancelled);

                var spl = result.text.split(":");
                connect(spl[0], spl[1]);

                //Connect and if not paired, pair

            },
            function (error) {
                console.log("Scanning failed: " + error);
            },
            {
                preferFrontCamera: false, // iOS and Android
                showFlipCameraButton: true, // iOS and Android
                showTorchButton: true, // iOS and Android
                torchOn: false, // Android, launch with the torch switched on (if available)
                saveHistory: false, // Android, save scan history (default false)
                prompt: "Scan QR code to pair pc", // Android
                resultDisplayDuration: 500, // Android, display scanned text for X ms. 0 suppresses it entirely, default 1500
                formats: "QR_CODE", // default: all but PDF_417 and RSS_EXPANDED
                disableAnimations: true, // iOS
                disableSuccessBeep: false // iOS and Android
            }
        );
        
    };

    var openSockets = []

    function connect(ip, port, onSuccess) {
        var socket = new Socket();
        socket.onData = function (data) {
            onData(socket, data);
        };
        socket.onError = function (errorMessage) {
            console.log("ERROR: " + errorMessage);
        };
        socket.onClose = function (hasError) {
            console.log("CLOSE: " + hasError);
        };
        socket.open(
            ip,
            port,
            function () {
                onSuccess(socket)
            },
            function (errorMessage) {
                console.log(errorMessage);
            }
        );
    }

    function sendString(socket, str) {
        var data = new Uint8Array(str.length);
        for (var i = 0; i < data.length; i++) {
            data[i] = str.charCodeAt(i);
        }
        socket.write(data);
    }

    var leftover = "";

    var accepted_socket = null;

    function onData(socket, data) {
        var stream = leftover + (new TextDecoder("utf-8").decode(data));
        console.log(leftover);
        console.log(stream);
        var indexStart = 0;
        var found = false;
        for (var i = 0; i < stream.length; i++) {
            if (stream[i] === ";") {
                found = true;
                var msg = stream.substring(indexStart, i);
                indexStart = i + 1;
                console.log(msg);
                var spl = msg.split(":");
                var cmd = spl[0];
                switch (cmd) {
                    case "IMAGE":
                        if (paired) {
                            var args = spl[1].split(",");
                            var btn = buttons[args[0]]
                            var url = "url('data:image/png;base64," + args[1] + "')";
                            console.log(url);
                            //btn.style.backgroundImage = "url('" + url.replace(/(\r\n|\n|\r)/gm, "") + "')";
                            //btn.css("background-image", "url('" + url.replace(/(\r\n|\n|\r)/gm, "") + "')");
                            //btn.css("background-image", url);
                            //btn.style.backgroundImage = url;
                            btn.style.backgroundImage = url;
                        }
                        break;
                    case "CONN":
                        var args = spl[1].split(",")
                        //upgrade this connection to accepted one
                        accepted_socket = socket
                        zeroconf.close();
                        sendString(socket, "CONNACCEPT;");
                    default:
                        break;
                }
            }
        }
        if (found) {
            leftover = stream.substring(indexStart, stream.length);
        } else {
            leftover = stream;
        }
    }

    function setupButtons() {
        var heightPercent = 100 / grid_y;
        var widthPercent = 100 / grid_x;
        var buttonCount = grid_x * grid_y;

        var buttonContainer = document.getElementById("buttonContainer")
        buttonContainer.innerHTML = ""
        buttons = []
        for (let i = 0; i < buttonCount; i++) {
            var btn = document.createElement("BUTTON")
            btn.classList.add("button-wrapper");
            btn.classList.add("button");
            btn.style.width = widthPercent + "%";
            btn.style.height = heightPercent + "%";
            btn.addEventListener("touchstart", onKeyPressed.bind(this, i), false);
            btn.addEventListener("touchend", onKeyReleased.bind(this, i), false);
            buttons.push(btn)
            buttonContainer.appendChild(btn);
        }
    }

    function onPause() {
        // TODO: This application has been suspended. Save application state here.
    };

    function onResume() {
        // TODO: This application has been reactivated. Restore application state here.
    };

    function onKeyPressed(key) {
        console.log("Pressed Key " + key)
        //buttons[key].style.backgroundColor = "red";
        sendString("BTNEVENT:" + key + ",0;")
    };

    function onKeyReleased(key) {
        console.log("Released Key " + key)
        //buttons[key].style.backgroundColor = "blue";
        sendString("BTNEVENT:" + key + ",1;")
    };




} )();