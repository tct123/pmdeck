package com.seyahdoo.pmdeck

import android.util.Log
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket

class Connection {

    var socket: Socket? = null;
    var writer: PrintWriter? = null;
    var readThread:Thread? = null
    var pingThread:Thread? = null


    fun openConnection(ip:InetAddress, port:Int, onSuccess: (()->Unit)? = null) {
        doThreaded {
            try {
                socket = Socket(ip, port)
                socket?.soTimeout = 10000
                writer = PrintWriter(socket!!.getOutputStream())
                reader(BufferedReader(InputStreamReader(socket?.getInputStream())))
//                openConnections.add(this)
                pingThread = doThreaded {
                    while (true){
                        try {
                            Thread.sleep(1000)
                            this.sendMessage("PING;")
                        }catch (e: Exception){
                            e.printStackTrace()
                        }
                    }
                }

                onSuccess?.invoke()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun closeConnection(){
        doThreaded {
            Log.e("Connection","Closing connection")
//            openConnections.remove(this);

            readThread?.interrupt()
            pingThread?.interrupt()
            writer?.close()
            socket?.close()

            readThread = null
            pingThread = null
            writer = null
            socket = null
        }
    }

    interface OnDataListener {
        fun onData(s: String)
    }

    var OnDataCallback: ((Connection,String)->Unit)? = null

    fun setOnDataListener(listener: (Connection,String) -> Unit){
        OnDataCallback = listener
    }


    private fun reader(bufreader: BufferedReader) {
        readThread = doThreaded {
            while (true) {
                try {
                    val input: String = bufreader.readLine() ?: continue
                    Log.e("Message Received", input)
                    OnDataCallback?.invoke(this@Connection, input)
                } catch (e: Exception) {
                    e.printStackTrace()
                    this.closeConnection()
                    return@doThreaded
                }
            }
        }
    }

    fun sendMessage(message:String){
        Log.e("Message Sent",message)
        try{
            writer?.write(message)
            writer?.flush()
        }catch (e: Exception){
            e.printStackTrace()
            closeConnection()
        }
    }

}