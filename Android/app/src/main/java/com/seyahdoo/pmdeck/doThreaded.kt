package com.seyahdoo.pmdeck

fun doThreaded (func: () -> Unit): Thread {
    val t = Thread(Runnable {
        func()
    })
    t.start()
    return t
}

fun doThreaded (func: () -> Unit, onDone: () -> Unit): Thread {
    val t = Thread(Runnable {
        func()
        onDone()
    })
    t.start()
    return t
}
