
import QtQuick 1.0
Rectangle {
    id: window
    width: 800
    height: 600
    //anchors.fill: parent
    color: "lightblue"

    function set_scanner_battery_level(level) {
        if (level==0) {
        detector_battery.source = "res\\pwr0.png"
            }
        if (level==1) {
            detector_battery.source = "res\\pwr1.png"
            }
    if (level==2) {
            detector_battery.source = "res\\pwr2.png"
            }
    if (level==3) {
            detector_battery.source = "res\\pwr3.png"
            }
    if (level==4) {
            detector_battery.source = "res\\pwr4.png"
            }
    if (level==5) {
            detector_battery.source = "res\\pwr5.png"
            }
    }

    function set_xray_battery_level(level) {
    }

    function set_detector_running (running) {
            runing_status.running = running
    }


    function set_detector_connected(connected) {
        if (connected) {
            detector_connection.source = "res\\ct.png"
        } else {
            detector_connection.source = "res\\noct.png"
        }
    }

    function set_xray_connected(connected) {
        if (connected) {
            xray_connection.source = "res\\CONNECTED.png"
        } else {
            xray_connection.source = "res\\UNCONNECTED.png"
        }
    }

    function set_speaker_status (on) {
        if(on) {
            speaker.source = "res\\pcs.png"
        } else {
            speaker.source = "res\\dis-pcs.png"
        }
    }

    function set_stop_status (stopped) {
        if (stopped) {
            emstop.source = "res\\stop.png"
        } else {
            emstop.source = "res\\stop-lk.png"
        }
    }

    function set_trace_info(msg) {
    log.text = msg
    }


    function set_detector_speed(s) {
        console.log("speed is "+s)
        speed.text = s
    }


    Image {
        anchors.fill:parent
        anchors.horizontalCenter : title_area.horizontalCenter
        id: appons
        source:"res\\portable-UI-bk.png"
    }

    Item {
        AnimatedCircle {
            id: runing_status
            color:"transparent"
            x:108;y:175
            height: 300
            width: 300
        }
    }
    Image {
        id: detector_connection
        x:620;y:135
        height : 270
        width : 112
        fillMode: Image.PreserveAspectFit
        source: "res\\noct.png"
    }
    Image {
        id: detector_battery
        x:620;y:190
        height : 270
        width : 112
        fillMode: Image.PreserveAspectFit
        source: "res\\pwr5.png"
    }
    Text {
        id: speed
        x:630;y:375
        height: 100
        width: 270
        font.pointSize:20
        color:"lightgreen"
        text: "0"

    }
    Text {
        id: log
        x:150;y:500
        height: 120
        width: 500
        text: "Waiting"
        font.pointSize:30
        font.bold: true
        color:"lightgreen"

    }

    Image {
        id: emstop
        x:550;y:480
        height : 100
        width : height
        fillMode: Image.PreserveAspectFit
        source: "res\\stop.png"
    }

    Image {
        id: speaker
        x:680;y:480
        height : 100
        width : height
        fillMode: Image.PreserveAspectFit
        source: "res\\dis-pcs.png"

    }

    Item {
        id: status_system
        width:parent.width/1.1
        height:window.height/5

    }
}
