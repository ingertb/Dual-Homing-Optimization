#-----------------------------------------------------------------------
#liczba węzły, łuki, zapotrzebowań oraz ścieżek:
#-----------------------------------------------------------------------
param Vn, integer, >= 2;  #Number of nodes
param En, integer, >= 1;  #Number of links
param Dn, integer, >= 1;  #Number of demansd
param Pn, integer, >= 1;  #Number of paths to servers
 
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Indeksy:
#-----------------------------------------------------------------------
set V, default {1..Vn}; #Nodes
set E, default {1..En}; #Links
set D, default {1..Dn}; #Demans
set VS, default {};     #Servers
set P, default {1..Pn}; #Paths
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Stałe:
#-----------------------------------------------------------------------
param h{D} >= 0;  			    #Volume of demand d
param K{E} >= 0; 			    #Unit cost of link e
param t{D} >= 0;               	#Sink node of demand d   
param A{E,V}, >= 0, default 0;  #= 1 if node v is the originating node of link e; 0, otherwise
param B{E,V}, >= 0, default 0;  #= 1 if node v is the terminating node of link e; 0, otherwise
param c{E} >= 0, default 1000;    #Capacity of link e 
#-----------------------------------------------------------------------
#***********************************************************************
#-----------------------------------------------------------------------
#Zmienne:
#-----------------------------------------------------------------------
var u{E,D,P}, binary;    #Binary variable corresponding to availability of the link e for all the demands d 
var ud{E,D,P}, binary;	 #Binary variable corresponding to flow of all the demands d allocated to link e
var ue{E,D}, binary;     # Binary variable corresponding to flow of all the demands d allocated to link e
var y{E} >= 0;           #Flow realizing all the  demands d allocated to link e (continuous non-negative)
var x{E,D,P}, >=0;       #Flow realizing demand d allocated to link e (continuous non-negative)
var f{D,V}, >=0;		 #Outgoing flow for the  demand d allocated to node v (continuous non-negative) 
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
#The size of the demand on the link
s.t. c1f{d in D, v in (VS)} : sum{e in E, p in (P)} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = f[d,v];
s.t. c2f{p in (P), d in D, v in V diff (VS) : v != t[d]} : sum{e in E} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = 0;
s.t. c3f{d in D, v in V : v == t[d]} : sum{e in E, p in (P)} (A[e,v]*x[e,d,p] - B[e,v]*x[e,d,p]) = -f[d,v];

#Bifurcation of the paths
s.t. c1b{d in D, v in (VS)} : sum{e in E, p in (P)} (A[e,v]*u[e,d,p] - B[e,v]*u[e,d,p]) = 1;
s.t. c2b{p in (P), d in D, v in V diff (VS) : v != t[d]} : sum{e in E} (A[e,v]*u[e,d,p] - B[e,v]*u[e,d,p]) = 0;
s.t. c3b{d in D, v in V : v == t[d]} : sum{e in E, p in (P)} (A[e,v]*u[e,d,p] - B[e,v]*u[e,d,p]) = -Pn;

s.t. c4b{e in E, d in D} : sum {p in P} u[e,d,p] >= ue[e,d];
s.t. c5b{d in D, v in V : v == t[d]} : sum{e in E} (A[e,v]*ue[e,d] - B[e,v]*ue[e,d]) = -2;
s.t. c6b{e in E, d in D}: sum {p in P} u[e,d,p] <= Pn-1;


s.t. cd{e in E, d in D, p in P} : u[e,d,p] >= ud[e,d,p];

s.t. c4f{p in P, d in D, e in E} : x[e,d,p] <= h[d]*ud[e,d,p];

s.t. c6f{d in D} : sum{v in VS} f[d,v] = h[d];

s.t. c4{e in E} : sum{d in D, p in P} x[e,d,p] = y[e];

s.t. cc{e in E} : y[e] <= c[e];


#-----------------------------------------------------------------------
end;
#-----------------------------------------------------------------------
