use_module(library(pce)).

conexion(a, b, 1000).
    conexion(b, a, 900).
    conexion(c, a, 1200).
    conexion(a, c, 1400).
    conexion(d, c, 500).
    conexion(b, d, 800).
    conexion(d, m, 600).
             conexion(m, d, 700).

