#-----------------------------------------------------------------------
#liczba węzły, łuki, zapotrzebowań oraz ścieżek:
#-----------------------------------------------------------------------
param Vn, integer, >= 2;  #liczba węzły
param En, integer, >= 1;  #liczba łuki
param Dn, integer, >= 1;  #liczba zapotrzebowań
param Pn, integer, >= 1;  #liczba zapotrzebowań
 
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Indeksy:
#-----------------------------------------------------------------------
set V, default {1..Vn};
set E, default {1..En};
set D, default {1..Dn};
set VS, default {2,3};
set VH, default {};
set P, default {1..Pn};
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Stałe:
#-----------------------------------------------------------------------
param h{D} >= 0;  			    #Rozmiar zapotrzebowań
param del, integer, >= 0, default 1000; #max delay
param K{E} >= 0; 			    #Koszt użyć łuku
param t{D} >= 0;               #węzeł docelowy   
param A{E,V}, >= 0, default 0; #rozpoczyna się w węzeł v
param B{E,V}, >= 0, default 0; #kończy się w węzeł v
param W, integer, >= 0, default 9000000; #wystarczająco duża wartość
param kol{E} >= 0, default 5;    #Koszt otwarcia łuku
param Kow{V} >= 0, default 5;  #Koszt otwarcia wierzchołki
param C{E} >= 0, default 8;    #przepływność dostępną na łączu
param G{V} >= 0;				#stopień węzła
param Del{V} >=0, default 10;   #delay in ms
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Zmienne:
#-----------------------------------------------------------------------
var x{E,D,P}, binary;    #Wielkość  przepływności  zapotrzebowań na łuku
var y{E} >= 0;            #Wielkość przepływności na łuku
var u{E,D}, binary;         #Ue = 1 jeśli łącze e jest zainstalowane
var Uw{V}, binary;		    #Uw = 1 jeśli węzeł jest zainstalowane
var dl{D} >= 0;
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Funkcja celu:
#-----------------------------------------------------------------------
minimize z: sum{e in E} (K[e]*y[e]);
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Ograniczenia: bifurcated and non-bifurcated
#-----------------------------------------------------------------------
#Wielkość  przepływności  zapotrzebowań na łuku




s.t. c1{d in D, v in (VS)} : sum{e in E, p in (P)} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = 1;
s.t. c2{d in D, v in V diff (VS) : v != t[d]} : sum{e in E, p in (P)} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = 0;
s.t. c3{d in D, v in V : v == t[d]} : sum{e in E, p in (P)} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = -Pn;

s.t. c5 {e in E, d in D} : sum {p in P} x[e,d,p] >= u[e,d];
s.t. c6{d in D, v in V : v == t[d]} : sum{e in E} (A[e,v]*u[e,d] - B[e,v]*u[e,d]) = -2;

s.t. c7 {e in E, d in D}: sum {p in P} x[e,d,p] <= Pn-1;
s.t. c4{e in E} : sum{d in D, p in P} x[e,d,p] = y[e];

#-----------------------------------------------------------------------
data;
#-----------------------------------------------------------------------
#liczba łuki, zapotrzebowań oraz ścieżek
param En := 16; 
param Dn := 1; 
param Vn := 10; 
param Pn := 3; 
set VS := 
			1
			3
			2
; 
set VH := 
			5
; 
#-----------------------------------------------------------------------
#rozmiar zapotrzebowania d, węzeł żródłowy d, węzeł docelowy d

param : h   t :=
 1      8  10
# 2     8  2 8
 ;
#-----------------------------------------------------------------------
#węzłe-łącze  Aev(e,v) 
param : A :=
       1 1    1
       2 1    1
       
       3 2    1
       6 2    1
       7 2    1
       
       4 3    1
       5 3	  1
       
       8 4	  1
       
       10 5   1
       11 5   1
       
       9 6    1
       15 6   1
       
       12 7   1
       13 7   1       
       
       16 9   1
       14 10  1;
#----------------------------------------------------------------------- 
#węzłe-łącze  Bev(e,v) 
param : B :=
       2 2    1
       
       1 3    1
       3 3    1
       
       4 4    1
       
       7 5	  1
       
       5 6    1
       6 6    1
       8 6    1
       
       9 7    1
       10 7   1
       
       11 8   1
       14 8   1 
       
       12 9   1
       15 9   1
       
       13 10  1     
       16 10  1;
#-----------------------------------------------------------------------       
#koszt jednostkowy użycia przepływności na łączach
param : K :=
	 1      90
	 2      30
	 3      10
	 4      10
	 5      30
	 6      35
	 7      500
	 8      10
	 9      15
	 10     10
	 11     300
	 12     45
	 13     25
	 14     35
	 15     50
	 16     90;
#----------------------------------------------------------------------- 
#upper bound for the degree of transit node v
param : G :=
	 1      2
	 2      4
	 3      4
	 4      2
	 5      3
	 6      5
	 7      4
	 8      2
	 9      3
	 10     3;
#-----------------------------------------------------------------------
end;
#-----------------------------------------------------------------------
