package com.seyahdoo.pmdeck

import android.os.Debug
import android.util.Log
import org.jetbrains.anko.doAsync
import java.io.*
import java.lang.Exception
import java.net.InetAddress
import java.net.Socket
import java.net.SocketException
import kotlin.math.log

class Connection {

//    companion object {
//        var openConnections:MutableList<Connection> = mutableListOf()
//    }

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
                        Thread.sleep(1000);
                        this.sendMessage("PING;")
                    }
                }

                onSuccess?.invoke()
            } catch (e: Exception) {
                Log.e("Connection", e.toString());
            }
        }
    }

    fun closeConnection(){
        doThreaded {
            Log.e("Connection","Closing connection")
//            openConnections.remove(this);

            readThread?.interrupt()
            writer?.close()
            socket?.close()

            readThread = null
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
            Log.e("SEVERE",e.toString())
            closeConnection()
        }
    }

}