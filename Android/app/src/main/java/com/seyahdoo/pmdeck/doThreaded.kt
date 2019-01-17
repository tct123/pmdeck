package com.seyahdoo.pmdeck

fun <T> T.doThreaded (func: ()->Unit): Thread {
    val t:Thread = Thread(Runnable {
        func()
    })
    t.start()
    return t
}