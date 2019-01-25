// For an introduction to the Blank template, see the following documentation:
// http://go.microsoft.com/fwlink/?LinkID=397704
// To debug code on page load in cordova-simulate or on Android devices/emulators: launch your app, set breakpoints, 
// and then run "window.location.reload()" in the JavaScript Console.
(function () {
    "use strict";

    document.addEventListener( 'deviceready', onDeviceReady.bind( this ), false );

    function onDeviceReady() {
        // Handle the Cordova pause and resume events
        document.addEventListener('pause', onPause.bind(this), false);
        document.addEventListener('resume', onResume.bind(this), false);

        var paired = true;
        var pass = 123456;

        //Setup Buttons
        var grid_x = 3;
        var grid_y = 5;

        var heightPercent = 100 / grid_y;
        var widthPercent = 100 / grid_x;
        var buttonCount = grid_x * grid_y;

        var buttonContainer = document.getElementById("buttonContainer")
        var buttons = []
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

        //cordova.plugins.barcodeScanner.scan(
        //    function (result) {
        //        console.log("We got a barcode\n" +
        //            "Result: " + result.text + "\n" +
        //            "Format: " + result.format + "\n" +
        //            "Cancelled: " + result.cancelled);
        //    },
        //    function (error) {
        //        console.log("Scanning failed: " + error);
        //    },
        //    {
        //        preferFrontCamera: false, // iOS and Android
        //        showFlipCameraButton: true, // iOS and Android
        //        showTorchButton: true, // iOS and Android
        //        torchOn: false, // Android, launch with the torch switched on (if available)
        //        saveHistory: false, // Android, save scan history (default false)
        //        prompt: "Scan QR code to pair pc", // Android
        //        resultDisplayDuration: 500, // Android, display scanned text for X ms. 0 suppresses it entirely, default 1500
        //        formats: "QR_CODE", // default: all but PDF_417 and RSS_EXPANDED
        //        disableAnimations: true, // iOS
        //        disableSuccessBeep: false // iOS and Android
        //    }
        //);

        //QRScanner.show();

        //var body = document.getElementById("the-body")
        //document.body.classList.add("scanning-body");

        
    };

    function onPause() {
        // TODO: This application has been suspended. Save application state here.
    };

    function onResume() {
        // TODO: This application has been reactivated. Restore application state here.
    };

    function onKeyPressed() {

    };

    function onKeyReleased() {
        
    };




} )();