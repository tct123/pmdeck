/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var app = {
    // Application Constructor
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
        document.addEventListener('pause', this.onPause.bind(this), false);
        document.addEventListener('resume', this.onResume.bind(this), false);
    },

    // deviceready Event Handler
    //
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        console.log("device really ready");

        var paired = true;
        var paired_device_id = "";
        var pass = 123456;

        //Setup Buttons
        var grid_x = 3;
        var grid_y = 5;

        var heightPercent = 100/grid_y;
        var widthPercent = 100/grid_x;
        var buttonCount = grid_x * grid_y;
        
        var buttonContainer = document.getElementById("buttonContainer")
        var buttons = []
        for (let i = 0; i < buttonCount; i++) {
            var btn = document.createElement("BUTTON")
            btn.classList.add("button-wrapper");
            btn.classList.add("button");
            btn.style.width = widthPercent+"%";
            btn.style.height = heightPercent+"%";
            btn.addEventListener("touchstart", this.onKeyPressed.bind(this, i), false);
            btn.addEventListener("touchend", this.onKeyReleased.bind(this, i), false);
            buttons.push(btn)
            buttonContainer.appendChild(btn);
        }

        // Start a scan. Scanning will continue until something is detected or
        // `QRScanner.cancelScan()` is called.
        QRScanner.scan(displayContents);
        
        function displayContents(err, text){
            if(err){
                console.log(err);
                // an error occurred, or the scan was canceled (error code `6`)
            } else {
                // The scan completed, display the contents of the QR code:
                console.log(text);
                QRScanner.hide();
            }
        }
        
        var body = document.getElementById("the_body")
        body.style.opacity = 0.0;


        //Wifi https://github.com/apache/cordova-plugin-network-information

        var zeroconf = cordova.plugins.zeroconf;

        var goneOnlineEntered = false

        document.addEventListener("online", onOnline, false);
        console.log(navigator.connection.type);
        
        function onOnline() {
            // Handle the online event
            console.log("chack");
            
            var networkState = navigator.connection.type;

            if (networkState == Connection.WIFI) {
                if(goneOnlineEntered == true) return;
                goneOnlineEntered = true
                console.log("Connected now")
                setTimeout(function () {
                    discover();
                }, 1000);
                
            }else{
                goneOnlineEntered = false
            }

        }

        //initial wifi check
        if(navigator.connection.type == Connection.WIFI){
            onOnline();
        }

        var zeroconf = cordova.plugins.zeroconf;
        
        function discover(){
            zeroconf.reInit()
            zeroconf.watch('_pmdeck._tcp.', 'local.', function(result) {
                var action = result.action;
                var service = result.service;
                if (action == 'added') {
                    console.log('service added'+ service);
                } else if (action == 'resolved') {
                    console.log('service resolved'+ service.ipv4Addresses[0] + ":" + service.port +";");
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

                    console.log(device.uuid);
                    if (service.txtRecord.uid == paired_device_id) {
                        connect(service.ipv4Addresses[0], service.port, function (socket) {
                            sendString(socket, "CONN:" + device.uuid + ";");
                            accepted_socket = socket;
                        });
                    }

                } else {
                    console.log('service removed'+ service);
                }
            });
        }
    },

    openSockets: [],

    connect: function (ip, port, onSuccess) {
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
    },

    sendString: function (socket, str) {
        var data = new Uint8Array(str.length);
        for (var i = 0; i < data.length; i++) {
            data[i] = str.charCodeAt(i);
        }
        socket.write(data);
    },

    leftover: "",

    accepted_socket: null,

    onData: function (socket, data) {
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
                            var btn = buttons[args[0]];
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
                        accepted_socket = socket;
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

    setupButtons: function () {
        var heightPercent = 100 / grid_y;
        var widthPercent = 100 / grid_x;
        var buttonCount = grid_x * grid_y;

        var buttonContainer = document.getElementById("buttonContainer");
        buttonContainer.innerHTML = "";
        buttons = [];
        for (let i = 0; i < buttonCount; i++) {
            var btn = document.createElement("BUTTON");
            btn.classList.add("button-wrapper");
            btn.classList.add("button");
            btn.style.width = widthPercent + "%";
            btn.style.height = heightPercent + "%";
            btn.addEventListener("touchstart", onKeyPressed.bind(this, i), false);
            btn.addEventListener("touchend", onKeyReleased.bind(this, i), false);
            buttons.push(btn);
            buttonContainer.appendChild(btn);
        }
    },

    onPause: function () {
        // TODO: This application has been suspended. Save application state here.
    },

    onResume: function () {
        // TODO: This application has been reactivated. Restore application state here.
    },

    onKeyPressed: function (key) {
        console.log("Pressed Key " + key);
        //buttons[key].style.backgroundColor = "red";
        if (accepted_socket != null) {
            sendString(accepted_socket, "BTNEVENT:" + key + ",0;");
        }
    },

    onKeyReleased: function (key) {
        console.log("Released Key " + key);
        //buttons[key].style.backgroundColor = "blue";
        if (accepted_socket != null) {
            sendString(accepted_socket, "BTNEVENT:" + key + ",1;");
        }
    }


};

app.initialize();