package com.seyahdoo.pmdeck

fun doThreaded (func: () -> Unit): Thread {
    val t = Thread(Runnable {
        func()
    })
    t.start()
    return t
}