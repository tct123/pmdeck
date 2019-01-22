package com.seyahdoo.pmdeck

import android.util.Log
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket

class Connection {

    var socket: Socket? = null
    var writer: PrintWriter? = null
    var reader: BufferedReader? = null
    var readThread:Thread? = null
    var pingThread:Thread? = null

    constructor(ip:InetAddress, port: Int, onData: (Connection,String)->Unit, onSuccess: ((Connection)->Unit)? = null){
        OnDataCallback = onData
        openConnection(ip, port, onSuccess)
    }

    private fun openConnection(ip:InetAddress, port:Int, onSuccess: ((Connection)->Unit)? = null) {
        doThreaded {
            try {
                socket = Socket(ip, port)
//                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                reader = BufferedReader(InputStreamReader(socket?.getInputStream()))
                readThread = doThreaded {
                    while (!Thread.interrupted()) {
                        try {
                            val input: String = reader?.readLine() ?: continue
                            Log.e("Message Received", "from: ${socket!!.inetAddress.hostAddress}:${socket!!.port} ->  $input")
                            OnDataCallback?.invoke(this@Connection, input)
                        } catch (e: Exception) {
                            e.printStackTrace()
                            this.closeConnection()
                            break
                        }
                    }
                }
                pingThread = doThreaded {
                    while (!Thread.interrupted()){
                        try {
                            Thread.sleep(1000)
                            this.sendMessage("PING;")
                        }catch (e: Exception){
                            e.printStackTrace()
                            this.closeConnection()
                            break
                        }
                    }
                }

                onSuccess?.invoke(this)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun closeConnection(){
        doThreaded {
            Log.e("Connection","Closing connection")

            readThread?.interrupt()
            pingThread?.interrupt()
            socket?.close()
            reader?.close()
            writer?.close()

            readThread = null
            pingThread = null
            writer = null
            reader = null
            socket = null
        }
    }

    var OnDataCallback: ((Connection,String)->Unit)? = null

    fun sendMessage(message:String){
        Log.e("Message Sent","To ${socket!!.inetAddress.hostAddress}:${socket!!.port} -> $message")
        try{
            writer!!.write(message)
            writer!!.flush()
        }catch (e: Exception){
            e.printStackTrace()
            closeConnection()
        }
    }

}