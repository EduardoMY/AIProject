/*
aeropuerto(mxl, mexicali).
aeropuerto(bar, barcelona).
aeropuerto(cal, calcuta).
aeropuerto(dam, damasco).
aeropuerto(est, estambul).
aeropuerto(den, denver).

vuelo(v001, mxl, den, 300).
vuelo(v002, mxl, bar, 125).
vuelo(v003,  bar, cal, 125).
vuelo(v004, cal, den, 125).

*/

/* Thanks Tony : V*/

vuelos(A, B, C, Path, Vuelos, Len) :- path(A, B, Path, Vuelos, Len), length(Path, C1), C is C1 - 2.

path(A,B,Path,Vuelos,Len) :-
    travel(A,B,[A],[],Q,R,Len), 
    reverse(Q,Path),
    reverse(R,Vuelos).

travel(A,B,P,P2,[B|P],[I|P2],L) :- 
    vuelo(I,A,B,L).

travel(A,B,Visited,V2,Path,Vuelos,L) :-
    vuelo(I,A,C,D),           
    C \== B,
    \+member(C,Visited),
    travel(C,B,[C|Visited],[I|V2],Path,Vuelos,L1),
    L is D+L1. 
