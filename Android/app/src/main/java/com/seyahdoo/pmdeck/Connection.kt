package com.seyahdoo.pmdeck

import android.util.Log
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket
import java.util.concurrent.atomic.AtomicBoolean

class Connection {

    var socket: Socket? = null
    var writer: PrintWriter? = null
    var reader: BufferedReader? = null
    var readThread:Thread? = null
    val readRun: AtomicBoolean = AtomicBoolean(true)

    var pingThread:Thread? = null
    val pingRun: AtomicBoolean = AtomicBoolean(true)


    constructor(ip:InetAddress, port: Int, onData: (Connection,String)->Unit, onSuccess: ((Connection)->Unit)? = null){
        OnDataCallback = onData
        openConnection(ip, port, onSuccess)
    }

    private fun openConnection(ip:InetAddress, port:Int, onSuccess: ((Connection)->Unit)? = null) {
        closed = false

        doThreaded {
            try {
                socket = Socket(ip, port)
//                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                reader = BufferedReader(InputStreamReader(socket?.getInputStream()))
                readThread = doThreaded {
                    readRun.set(true)
                    while (readRun.get()) {
                        try {
                            val input: String = reader?.readLine() ?: continue
                            Log.e("Message Received", "from: ${socket!!.inetAddress.hostAddress}:${socket!!.port} ->  $input")
                            OnDataCallback?.invoke(this@Connection, input)
                        } catch (e: Exception) {
                            e.printStackTrace()
                            this@Connection.closeConnection()
                        }
                    }
                    return@doThreaded
                }
                pingThread = doThreaded {
                    pingRun.set(true)
                    while (pingRun.get()){
                        try {
                            Thread.sleep(1000)
                            this.sendMessage("PING;")
                        }catch (e: Exception){
                            e.printStackTrace()
                            this@Connection.closeConnection()
                        }
                    }
                    return@doThreaded
                }

                onSuccess?.invoke(this)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    var closed = false

    fun closeConnection(onSuccess: ((Connection)->Unit)? = null){
        if(closed){
            Log.e("Connection","Tried Closing connection when its already closed")
            onSuccess?.invoke(this)
            return
        }else{
            doThreaded {
                Log.e("Connection","Closing connection")

                pingRun.set(false)
                readRun.set(false)
                pingThread?.join()
                readThread?.join()

                sendMessage("CLOSE;")

                socket?.close()
                reader?.close()
                writer?.close()

                readThread = null
                pingThread = null
                writer = null
                reader = null
                socket = null
                closed = true

                onSuccess?.invoke(this)
            }
        }


    }

    var OnDataCallback: ((Connection,String)->Unit)? = null

    fun sendMessage(message:String){
        try{
            writer!!.write(message)
            writer!!.flush()
            Log.e("Message Sent","To ${socket!!.inetAddress.hostAddress}:${socket!!.port} -> $message")
        }catch (e: Exception){
            e.printStackTrace()
            closeConnection()
        }
    }

}