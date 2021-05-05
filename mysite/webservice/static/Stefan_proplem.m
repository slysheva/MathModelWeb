(* ::Package:: *)

(* ::Input:: *)
rhos:=920;
Cps:=2010;
ks:=2.219;
Tb[t_]:=-20*t/10800.0+UnitStep[(t-5000)*(6000-t)]*5;
Th:=0;
L:=3.35*10^5;
h0:=0.001;
(**)

getArg[args_, varName_, default_]:= If[KeyExistsQ[args, varName], args[varName], default];
args :=Association[Import["args.json"]];


rhos= getArg[args, "rhos", rhos];
Cps= getArg[args, "Cps", Cps];
ks= getArg[args, "ks", ks];
Th= getArg[args, "Th", Th];
L= getArg[args, "L", L];
h0= getArg[args, "h0", h0];

(* ::Input:: *)
h[tt_]:=Sqrt[h0^2+2*ks/(rhos*L)*NIntegrate[Th-Tb[t],{t,0,tt}]];
(*{Plot[h[t],{t,0,11000},PlotLegends->{"h[t]"}],Plot[Tb[t],{t,0,11000},PlotLegends->{"Tb[t]"}]}*)


(* ::Input::Initialization:: *)
Export["h.csv", Table[h[t],{t, 0, 11000}], "CSV"];
Export["Tb.csv", Table[Tb[t],{t, 0, 11000}], "CSV"];


(* ::Input:: *)
(**)


(* ::Input:: *)
(**)


(* ::Input:: *)
(**)
