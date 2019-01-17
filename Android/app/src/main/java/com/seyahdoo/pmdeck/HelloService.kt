package com.seyahdoo.pmdeck

import android.content.Context
import android.net.wifi.WifiManager
import android.util.Log
import java.io.IOException
import java.io.PrintWriter
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket
import java.util.*
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceInfo
import javax.jmdns.ServiceListener

class HelloService{

    private val DEBUG_TAG = NetworkDiscovery::class.java.name
    private val TYPE = "_pmdeck._tcp.local."
    private val SERVICE_NAME = "LocalCommunication"

    private var mContext: Context? = null
    private var mJmDNS: JmDNS? = null
    private var mServiceInfo: ServiceInfo? = null
    private var mServiceListener: ServiceListener? = null
    private var mMulticastLock: WifiManager.MulticastLock? = null

    var localIp:InetAddress? = null
    var connectionDatabase = HashMap<String, MainActivity.IpPort>()


    constructor(context: Context){
        mContext = context
        try {
            val wifi = mContext?.getSystemService(android.content.Context.WIFI_SERVICE) as WifiManager
            val wifiInfo = wifi.connectionInfo
            val intaddr = wifiInfo.ipAddress

            val byteaddr = byteArrayOf(
                (intaddr and 0xff).toByte(),
                (intaddr shr 8 and 0xff).toByte(),
                (intaddr shr 16 and 0xff).toByte(),
                (intaddr shr 24 and 0xff).toByte()
            )
            val addr = InetAddress.getByAddress(byteaddr)
            localIp = addr
            mJmDNS = JmDNS.create(addr)
        } catch (e: IOException) {
            Log.d(DEBUG_TAG, "Error in JmDNS creation: $e")
        }

        startServer()
        startDiscovery()
    }

    private fun startDiscovery() {
        mJmDNS?.addServiceListener(TYPE, object : ServiceListener {
            override fun serviceAdded(serviceEvent: ServiceEvent) {
                Log.d("Service", "Added")
                val info = mJmDNS?.getServiceInfo(serviceEvent.type, serviceEvent.name)
                //On Found
                //onFound(info)
                val s = Socket(info!!.inetAddresses[0],info?.port)
                val w = PrintWriter(s!!.getOutputStream())
                //TODO write MY SERVER ADRESS
                s.close()
            }

            override fun serviceRemoved(serviceEvent: ServiceEvent) {
                Log.d("Service", "Removed")

            }

            override fun serviceResolved(serviceEvent: ServiceEvent) {
                Log.d("Service", "Resolved")
                mJmDNS?.requestServiceInfo(serviceEvent.type, serviceEvent.name, 1)
            }
        })
    }




    fun startServer(){

        //val d = NetworkDiscovery(this@MainActivity)
        //d.startServer(server.localPort)


        val server = ServerSocket(0)
        registerService(localIp, server.localPort)
        try {
            while (true){
                val client = server.accept()
                doThreaded {
                    val reader = Scanner(client.getInputStream())
                    try {
                        val s = reader.nextLine()
                        val lines = s.split(";")
                        for (l in lines){
                            val spl = l.split(":")
                            val cmd = spl[0]
                            val args = spl[1].split(",")

                            if (cmd == "HELLO"){
                                connectionDatabase[args[0]] = MainActivity.IpPort(args[1], args[2].toInt())
                            }

                        }
                    }catch (e:java.lang.Exception){

                    }finally {
                        //Might be an issue
                        client.close()
                    }
                }

            }
        }finally {
            unRegisterService()
        }

    }

    fun registerService(ip:InetAddress?, port:Int){

    }

    private fun unRegisterService() {
        TODO("not implemented") //To change body of created functions use File | Settings | File Templates.
    }


}