package com.seyahdoo.pmdeck

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.NetworkInfo
import android.net.wifi.SupplicantState
import android.net.wifi.WifiManager
import android.util.Log

class WifiStateWatcher {

    private var onEnabled: (()->Unit)? = null
    private var onDisabled: (()->Unit)? = null
    private var intentFilter: IntentFilter? = null
    private var context: Context? = null

    constructor(context:Context, onEnabled: (()->Unit)? = null, onDisabled: (()->Unit)? = null){
        this.context = context

        intentFilter = IntentFilter()
        intentFilter?.addAction(WifiManager.NETWORK_STATE_CHANGED_ACTION)

        this.onEnabled = onEnabled
        this.onDisabled = onDisabled
    }

    private val br: BroadcastReceiver? = object : BroadcastReceiver() {
        var lastState: Boolean = false
        override fun onReceive(context: Context, intent: Intent) {
            val action = intent.action
            if (action == WifiManager.NETWORK_STATE_CHANGED_ACTION) {
                val info = intent.getParcelableExtra<NetworkInfo>(WifiManager.EXTRA_NETWORK_INFO)
                val connected = info.isConnected
                if (connected != lastState) {
                    lastState = connected
                    Log.i("WIFI", "Wifi state changed: $connected")
                    if (connected){
                        onEnabled?.invoke()
                    }else{
                        onDisabled?.invoke()
                    }
                }
            }
        }
    }

    fun pause(){
        context?.unregisterReceiver(br)
    }

    fun resume(){
        context?.registerReceiver(br, intentFilter)
    }

    fun isWifiConnected(): Boolean {
        val wifiManager = context?.applicationContext?.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val wifiInfo = wifiManager.connectionInfo
        val supState = wifiInfo.supplicantState
        return (supState == SupplicantState.COMPLETED)
    }

}