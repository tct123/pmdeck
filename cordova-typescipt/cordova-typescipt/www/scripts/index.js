// For an introduction to the Blank template, see the following documentation:
// http://go.microsoft.com/fwlink/?LinkID=397704
// To debug code on page load in cordova-simulate or on Android devices/emulators: launch your app, set breakpoints, 
// and then run "window.location.reload()" in the JavaScript Console.
(function () {
    "use strict";

    document.addEventListener( 'deviceready', onDeviceReady.bind( this ), false );

    var paired = false;
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

        var paired = storage.getItem("paired");
        if (paired == null) {
            paired = false;
        }
        var pass = storage.getItem("pass");
        if (pass == null) {
            pass = "";
        }
        var paired = storage.getItem("grid_x");
        if (grid_x == null) {
            grid_x = 3;
        }
        var paired = storage.getItem("grid_y");
        if (grid_y == null) {
            grid_y = 5;
        }

        //storage.setItem(key, value)



        setupButtons();

        cordova.plugins.barcodeScanner.scan(
            function (result) {
                console.log("We got a barcode\n" +
                    "Result: " + result.text + "\n" +
                    "Format: " + result.format + "\n" +
                    "Cancelled: " + result.cancelled);

                var spl = result.text.split(":");
                connect(spl[0], spl[1]);

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

    var socket = null;

    function connect(ip, port) {

        //TODO Disconnect current socket if exists

        socket = new Socket();

        socket.onData = onData;

        socket.onError = function (errorMessage) {
            // invoked after error occurs during connection
            console.log("ERROR: " + errorMessage);

        };
        socket.onClose = function (hasError) {
            // invoked after connection close
            console.log("CLOSE: " + hasError);

        };

        socket.open(
            ip,
            port,
            function () {
                console.log("connected");
                sendString("CONN:cordova1,123456;");
            },
            function (errorMessage) {
                // invoked after unsuccessful opening of socket
                console.log(errorMessage);
            }
        );

    }

    function sendString(str) {
        var data = new Uint8Array(str.length);
        for (var i = 0; i < data.length; i++) {
            data[i] = str.charCodeAt(i);
        }
        socket.write(data);
    }

    var leftover = "";

    function onData(data) {
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
                        var args = spl[1].split(",");
                        var btn = buttons[args[0]]
                        var url = "url('data:image/png;base64," + args[1] + "')";
                        console.log(url);
                        //btn.style.backgroundImage = "url('" + url.replace(/(\r\n|\n|\r)/gm, "") + "')";
                        //btn.css("background-image", "url('" + url.replace(/(\r\n|\n|\r)/gm, "") + "')");
                        //btn.css("background-image", url);
                        //btn.style.backgroundImage = url;
                        btn.style.backgroundImage = url;
                        break;
                    case "CONN":
                        var args = spl[1].split(",")
                        sendString("CONNACCEPT;");
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