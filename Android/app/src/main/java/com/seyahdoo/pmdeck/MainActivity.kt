package com.seyahdoo.pmdeck

import android.annotation.SuppressLint
import android.content.*
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Base64
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import android.view.View
import android.widget.ImageButton
import com.danimahardhika.cafebar.CafeBar
import com.danimahardhika.cafebar.CafeBarTheme
import kotlinx.android.synthetic.main.activity_main.*
import java.net.InetAddress
import java.util.*


class MainActivity : AppCompatActivity() {

    private var uid:String = ""
    private var synced:Boolean = false
    private var syncedID:String = ""
    private var pass:String = ""

    private var syncTrying:Boolean = false
    private var syncPass:String = ""
    private var syncCon:Connection? = null
    private var passAccepted:Boolean = false

    private var sharedPref:SharedPreferences? = null

    private var c:Connection? = null
    private var d:NetworkDiscovery? = null
    private var wifiStateWatcher:WifiStateWatcher? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        Log.d("MainActivity", "onCreate Run!")

        sharedPref = this.getPreferences(Context.MODE_PRIVATE)

        if (!sharedPref?.contains("uid")!!){
            uid = UUID.randomUUID().toString()
            with (sharedPref?.edit()) {
                this?.putString("uid", uid)
                this?.commit()
            }
        }else{
            uid = sharedPref?.getString("uid", "") ?: ""
        }

        synced = sharedPref?.getBoolean("synced", false) ?: false
        syncedID = sharedPref?.getString("syncedID", "") ?: ""
        pass = sharedPref?.getString("pass", "") ?: ""

        val buttonList = listOf(btn0,btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10,btn11,btn12,btn13,btn14)

        buttonList!!.forEachIndexed{ index, element ->
            element.setOnTouchListener { _:View, e:MotionEvent ->
                if (!synced) return@setOnTouchListener true
                doThreaded {
                    when (e.action){
                        MotionEvent.ACTION_DOWN -> {
                            c?.sendMessage("BTNEVENT:$index,0;")
                        }
                        MotionEvent.ACTION_UP -> {
                            c?.sendMessage("BTNEVENT:$index,1;")
                        }
                        MotionEvent.ACTION_POINTER_UP -> {

                        }

                    }
                }
                return@setOnTouchListener true
            }
        }

        val controlListener = fun (con:Connection, s:String){
            for (msg in s.split(";")){
                val spl = msg.split(":");
                val cmd = spl[0]
                @SuppressLint("Range")
                when (cmd){
                    "IMAGE" -> {
                        if (!synced || (synced && !passAccepted)){
                            con.closeConnection()
                            return
                        }
                        try {
                            val args = spl[1].split(",")
                            val image = buttonList!![(args[0]).toInt()]
                            val decodedString = Base64.decode(args[1], Base64.DEFAULT);
                            var bitmap: Bitmap = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
                            bitmap = Bitmap.createScaledBitmap(bitmap, image.measuredWidth, image.measuredHeight, true)
                            runOnUiThread {
                                image.setImageBitmap(bitmap)
                            }
                        }catch (e: Exception){
                            e.printStackTrace()
                        }
                    }
                    "PING" -> {
                        con.sendMessage("PONG;")
                    }
                    "PONG" -> {

                    }
                    "CONN" -> {
                        try {
                            val args = spl[1].split(",")
                            if (args[0] == syncedID && args[1] == pass){
                                passAccepted = true
                                con.sendMessage("CONNACCEPT;")
                                c = con
                            }
                        }catch (e:Exception){
                            e.printStackTrace()
                            con.closeConnection()
                        }
                    }
                    "SYNCREJ" -> {
                        con.closeConnection()
                    }
                    "SYNCTRY" -> {
                        if (synced) return
                        if (syncTrying) return
                        try {
                            val args = spl[1].split(",")
                            syncPass = args[1]
                            syncTrying = true
                            //Open Sync UI
                            CafeBar.builder(this)
                                .theme(CafeBarTheme.LIGHT)
                                .floating(true)
                                .swipeToDismiss(true)
                                .duration(Int.MAX_VALUE)
                                .content("Sync request came Do you accept? Password is $syncPass ")
                                .positiveText("Accept")
                                .positiveColor(Color.BLUE)
                                .negativeText("Reject")
                                .negativeColor(Color.RED)
                                .onPositive {
                                    if (!syncTrying) return@onPositive
                                    synced = true
                                    syncedID = args[0]
                                    pass = syncPass
                                    with (sharedPref?.edit()) {
                                        this?.putBoolean("synced", synced)
                                        this?.putString("syncedID", syncedID)
                                        this?.putString("pass", pass)
                                        this?.commit()
                                    }

                                    syncTrying = false
                                    syncPass = "0"
                                    doThreaded {
                                        con.sendMessage("SYNCACCEPT:$uid,$pass;")
                                    }
                                    it.dismiss()
                                }
                                .onNegative {
                                    if (!syncTrying) return@onNegative
                                    syncCon?.sendMessage("SYNCREJ;")
                                    syncTrying = false
                                    syncPass = "0"
                                    syncCon?.closeConnection()
                                    it.dismiss()
                                }
                                .show()
                        }catch (e:Exception){
                            e.printStackTrace()
                            Log.e("Network Listener","Closing Connection, Stuff Happened")
                            con.closeConnection()
                        }
                    }
                }
            }
        }

        wifiStateWatcher = WifiStateWatcher(
            this,
            fun() {
                //start discovery
                val discover = fun (){
                    Thread.sleep(1000)
                    Log.e("WIFI", "internet state -> ${wifiStateWatcher?.isInternetAvailable()}")

                    if (d == null) d = NetworkDiscovery(this@MainActivity)
                    else d?.reset()
                    d?.findServers("_pmdeck._tcp.local."){ it ->
                        Log.e("Main", "Found a server, connectiong. ${it.inet4Addresses[0]} : ${it.port}")
                        Connection(it.inetAddresses[0],it.port, controlListener){ con ->
                            if(synced){
                                con.sendMessage("CONN:$uid;")
                            }else{
                                syncTrying = false
                                syncPass = ""
                                con.sendMessage("SYNCREQ:$uid;")
                            }
                        }
                    }
                }
                doThreaded {
                    try {
                        c!!.closeConnection {
                            c = null
                            discover()
                        }
                    }catch (e:Exception){
                        discover()
                    }
                }
            },
            fun() {
                Log.e("WIFI", "internet state -> ${wifiStateWatcher?.isInternetAvailable()}")
            }
        )
    }

    override fun onPause() {
        Log.d("OnPause","OnPause")
        wifiStateWatcher?.pause()
        super.onPause()
    }

    override fun onResume() {
        Log.d("onResume","onResume")
        wifiStateWatcher?.resume()
        super.onResume()
    }

//    var swap:Boolean = true

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP){
            synced = false
            syncedID = ""
            syncPass = "0"
            syncTrying = false

            with (sharedPref?.edit()) {
                this?.putBoolean("synced", synced)
                this?.putString("syncedID", syncedID)
                this?.putString("pass", pass)
                this?.commit()
            }

            RebirthHelper.doRestart(this)
        }else if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN){
            //swap = !swap;
            //setSystemUIEnabled(swap);
        }
        return true
    }

    override fun onKeyLongPress(keyCode: Int, event: KeyEvent): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {

            synced = false
            syncedID = ""
            syncPass = "0"
            with (sharedPref?.edit()) {
                this?.putBoolean("synced", synced)
                this?.putString("syncedID", syncedID)
                this?.putString("pass", pass)
                this?.commit()
            }


            syncTrying = false
            RebirthHelper.doRestart(this)
            //c?.closeConnection()
            return true
        }
        return super.onKeyLongPress(keyCode, event)
    }

}
