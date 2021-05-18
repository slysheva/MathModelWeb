(* ::Package:: *)

(* ::Input:: *)
(*Button["\:041d\:0430\:0447\:0430\:0442\:044c \:0441\:043d\:0430\:0447\:0430\:043b\:0430", Remove["Global`*"]; FrontEndTokenExecute@"EvaluateInitialization";] *)


(* ::Input::Initialization:: *)
parentPath=$InputFileName/."":>NotebookFileName[];
parentDir=DirectoryName@parentPath;
SetDirectory[parentDir]
Print[parentDir]


(* ::Input:: *)
(**)


(* ::Input::Initialization:: *)
"\:0417\:043d\:0430\:0447\:0435\:043d\:0438\:044f \:043a\:043e\:043d\:0441\:0442\:0430\:043d\:0442 \:043f\:043e-\:0443\:043c\:043e\:043b\:0447\:0430\:043d\:0438\:044e \:0434\:043b\:044f \:0441\:043f\:043b\:0430\:0432\:0430 Ti-Al";
METR2CM:=100;
GRAMPERMOL:=36.38;

ks:=29.22/METR2CM;
kl:=29/METR2CM;
k:=0.8;

gl:=1;

L:=12268.8/GRAMPERMOL;
rho:=3.46;
LV:=L*rho;

Dl:=8.27*10^(-9)*METR2CM*METR2CM;

T0:=0;
sigmaInf:=0.55;

m:=-8.8;

gsMin:=2;
gsMax:=25;

nmin :=-2;
nmax:=2;


(* ::Input::Initialization:: *)
getArg[args_, varName_, default_]:= If[KeyExistsQ[args, varName], Internal`StringToDouble[args[varName]], default];

args :=Association[Import["args.json"]];

ks= getArg[args,"ks", ks];
kl= getArg[args,"kl", kl];
k= getArg[args,"k", k];

gl= getArg[args,"gl", gl];

L = getArg[args,"L", L];
rho = getArg[args,"rho", rho];
LV=L*rho;

Dl = getArg[args,"Dl", Dl];
sigmaInf = getArg[args,"sigmaInf", sigmaInf];
m = getArg[args,"m", m];

gsMin = getArg[args,"gsMin", gsMin];
gsMax = getArg[args,"gsMax", gsMax];

nmin =getArg[args,"nmin", nmin];
nmax=getArg[args,"nmax", nmax];


(* ::Input:: *)
(*Dl*)


addRow[varName_, var_, tooltip_, units_]:={
Tooltip[varName, tooltip], InputField[var, Number], units
};

Panel[
Grid[{
{Tooltip["t","\:0415\:0434\:0438\:043d\:0438\:0446\:044b \:0438\:0437\:043c\:0435\:0440\:0435\:043d\:0438\:044f \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b"],RadioButtonBar[Dynamic[temperature],{" K","\[Degree]C"}],""},
{Tooltip["e","\:0415\:0434\:0438\:043d\:0438\:0446\:044b \:0438\:0437\:043c\:0435\:0440\:0435\:043d\:0438\:044f \:044d\:043d\:0435\:0440\:0433\:0438\:0438"],RadioButtonBar[Dynamic[energy],{"\:043a\:0430\:043b","\:0414\:0436"}],""},
addRow[Subscript["k", "s"],Dynamic[ks], "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:0442\:0435\:043f\:043b\:043e\:043f\:0440\:043e\:0432\:043e\:0434\:043d\:043e\:0441\:0442\:0438 \:043f\:043e \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:0435", Dynamic[StringJoin[energy,"/\:0441\:0435\:043a \:0441\:043c",temperature]]],
addRow[Subscript["k", "l"], Dynamic[kl],"\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:0442\:0435\:043f\:043b\:043e\:043f\:0440\:043e\:0432\:043e\:0434\:043d\:043e\:0441\:0442\:0438 \:043f\:043e \:0436\:0438\:0434\:043a\:043e\:0439 \:0444\:0430\:0437\:0435", Dynamic[StringJoin[energy,"/\:0441\:0435\:043a \:0441\:043c",temperature]]],
addRow["k",Dynamic[k], "\:0420\:0430\:0432\:043d\:043e\:0432\:0435\:0441\:043d\:044b\:0439 \:043a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:0440\:0430\:0441\:043f\:0440\:0435\:0434\:0435\:043b\:0435\:043d\:0438\:044f \:043f\:0440\:0438\:043c\:0435\:0441\:0438",""],
addRow[Subscript["g", "l"],Dynamic[gl],"\:0413\:0440\:0430\:0434\:0438\:0435\:043d\:0442 \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b \:0432 \:0436\:0438\:0434\:043a\:043e\:0439 \:0444\:0430\:0437\:0435",Dynamic[StringJoin[temperature,"/\:0441\:043c"]]],
addRow["L", Dynamic[L], "\:0421\:043a\:0440\:044b\:0442\:0430\:044f \:0442\:0435\:043f\:043b\:043e\:0442\:0430 \:0437\:0430\:0442\:0432\:0435\:0440\:0434\:0435\:0432\:0430\:043d\:0438\:044f", Dynamic[StringJoin[energy,"/\:0433"]]],
addRow[\[Rho], Dynamic[rho], "\:041f\:043b\:043e\:0442\:043d\:043e\:0441\:0442\:044c", "\:0433/\!\(\*SuperscriptBox[\(\:0441\:043c\), \(3\)]\)"],
{Tooltip[Subscript["L", "V"], "\:0421\:043a\:0440\:044b\:0442\:0430\:044f \:0442\:0435\:043f\:043b\:043e\:0442\:0430 \:0437\:0430\:0442\:0432\:0435\:0440\:0434\:0435\:0432\:0430\:043d\:0438\:044f"],Dynamic[LV],Dynamic[StringJoin[energy,"/\!\(\*SuperscriptBox[\(\:0441\:043c\), \(3\)]\)"]]},
addRow[Subscript["D", "l"], Dynamic[Dl], "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:0434\:0438\:0444\:0444\:0443\:0437\:0438\:0438 \:043f\:0440\:0438\:043c\:0435\:0441\:0438 \:043f\:043e \:0436\:0438\:0434\:043a\:043e\:0439 \:0444\:0430\:0437\:0435", "\!\(\*SuperscriptBox[\(\:0441\:043c\), \(2\)]\)/\:0441\:0435\:043a"],
addRow[Subscript[\[Sigma], \[Infinity]], Dynamic[sigmaInf], "\:041a\:043e\:043d\:0446\:0435\:043d\:0442\:0440\:0430\:0446\:0438\:044f \:043f\:0440\:0438\:043c\:0435\:0441\:0438 \:0432 \:0440\:0430\:0441\:043f\:043b\:0430\:0432\:0435 \:0432\:0434\:0430\:043b\:0438 \:043e\:0442 \:0434\:0432\:0443\:0445\:0444\:0430\:0437\:043d\:043e\:0439 \:0437\:043e\:043d\:044b",""],
addRow["m", Dynamic[m], "\:041d\:0430\:043a\:043b\:043e\:043d \:043b\:0438\:043d\:0438\:0438 \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430", Dynamic[StringJoin[temperature,"/\:0432\:0442%"]]]
}],
Row[Pane[#,{Automatic,15}]&/@ {MouseAppearance[Tooltip[Graphics[{Circle[], Text["?"]}], "\:041d\:0430\:0432\:0435\:0434\:0438\:0442\:0435 \:043a\:0443\:0440\:0441\:043e\:0440 \:043d\:0430 \:0438\:043c\:044f \:043a\:043e\:043d\:0441\:0442\:0430\:043d\:0442\:044b, \:0447\:0442\:043e\:0431\:044b \:0443\:0437\:043d\:0430\:0442\:044c \:0435\:0451 \:0441\:043c\:044b\:0441\:043b"], "LinkHand"],Text["  \:0412\:0432\:0435\:0434\:0438\:0442\:0435 \:0437\:043d\:0430\:0447\:0435\:043d\:0438\:044f \:043a\:043e\:043d\:0441\:0442\:0430\:043d\:0442:"]}]
]

Panel[Row[{"\:0413\:0440\:0430\:043d\:0438\:0446\:044b \:0434\:043b\:044f "Tooltip["n", "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430 \:043e\:0442 \:043b\:0438\:043d\:0435\:0439\:043d\:043e\:0433\:043e \:0432\:0438\:0434\:0430"],IntervalSlider[Dynamic[{nmin, nmax}],{-3,3,1},Appearance->{"ThumbAppearance"->{Dynamic[Framed[nmin,Background->White]],None,Dynamic[Framed[nmax,Background->White]]}}, Method->"Stop", MinIntervalSize -> 1 ],Dynamic[{nmin, nmax}]}],FrameMargins->15]




(* ::Text:: *)
(**)
(*\:0413\:0440\:0430\:0444\:0438\:043a\:0438 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430 \:043e\:0442 \:043b\:0438\:043d\:0435\:0439\:043d\:043e\:0433\:043e \:0432\:0438\:0434\:0430:*)


(* ::Input:: *)
(*Tm[sigmaM_, n_]:=T0+m*sigmaM+n*sigmaM^2;*)


(* ::Input:: *)
(*Manipulate[*)
(* Plot[{Tm[sigmaM, n]}, {sigmaM, 0, 1},*)
(*  AxesLabel -> {\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(\[Sigma]\), \(\[ScriptM]\)]\), \!\(TraditionalForm\`*)
(*\*SubscriptBox[\(T\), \(\[ScriptM]\)]\)}, *)
(*  GridLines -> Automatic, *)
(*  PlotLegends -> "\[ScriptN]=" <> ToString[n]*)
(*  ], *)
(* {{n, nmin, "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"}, nmin, nmax}]*)


(* ::Input:: *)
(*Manipulate[*)
(* Plot[Evaluate@Table[Tm[sigmaM, n], {n, chosenN}], {sigmaM, 0, 1},*)
(*  AxesLabel -> {\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(\[Sigma]\), \(\[ScriptM]\)]\), \!\(TraditionalForm\`*)
(*\*SubscriptBox[\(T\), \(\[ScriptM]\)]\)},*)
(*  PlotLegends -> LineLegend[Table[n, {n, chosenN}], LegendLabel -> \[ScriptN]]],*)
(* {*)
(*  {chosenN, {0}, "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"},*)
(*  Range[nmin, nmax],*)
(*  ControlType -> CheckboxBar*)
(*  }*)
(* ]*)


(* ::Text:: *)
(*\:0414\:043b\:044f \:043f\:0435\:0440\:0435\:0441\:0447\:0451\:0442\:0430 \:043c\:043e\:0434\:0435\:043b\:0438 \:043f\:0435\:0440\:0435\:0441\:0447\:0438\:0442\:0430\:0439\:0442\:0435 \:0441\:043b\:0435\:0434\:0443\:044e\:0449\:0443\:044e \:043a\:043b\:0435\:0442\:043a\:0443:*)


(* ::Input::Initialization:: *)
km[phi_]:=ks*phi + kl*(1-phi);
Diff[phi_]:=Dl*(1-phi);

us := (ks*gs - kl*gl)/LV;
D0[phi_]:= Diff[phi]/Dl;

Tm[sigmaM_]:=T0+m*sigmaM+n*sigmaM^2;
f [sigmaM_]:=D[Tm[sigmaMI], sigmaMI] /.sigmaMI->sigmaM;
f0:= f[0];

r:=(2*n*sigmaInf)/m;
L0[phi_]:=phi +kl/ks*(1-phi);
Ll := kl/ks;
P := (ks*f0*sigmaInf)/(LV*Dl);
Gl := (gl*Dl)/(us*f0*sigmaInf);

h[phi_] := (D0[phi]*(P*Ll*Gl + phi))/(P*L0[phi]);
b:=If[r!=0,(-(1+r)+Sqrt[(1+r)^2-4*r*Gl])/(2*r), -Gl];

Eq1[phi_]:=((1-phi)*(1+r*Cm[phi])^2-r*h[phi])*Cm'[phi]+(k-1)*(1+r*Cm[phi])^2*Cm[phi]+(1+r*Cm[phi])*h'[phi];
sol1=ParametricNDSolve[{Eq1[phi]==0,Cm[0]==1+b},Cm,{phi,0,0.99},{n,gs}];
(*\:0421\:0447\:0438\:0442\:0430\:0435\:043c \[CurlyPhi]^**)
NCm[n_,gs_,phi_]:=Evaluate[Cm[n,gs][phi]/.sol1]

phistar=Table[phi/.FindRoot[(1-k)*NCm[n,gs,phi]*P*L0[phi]*(1+r/.n->n*NCm[n,gs,phi])+P*Ll*Gl+phi==0,{phi,0.8}],{n,nmin,nmax},{gs,gsMin,gsMax}];
phistarI[n_,gs_]:=ListInterpolation[phistar,InterpolationOrder->3,Method->"Spline"][n - nmin + 1,gs - gsMin + 1];

(*\:0421\:0447\:0438\:0442\:0430\:0435\:043c \[Delta]*)
g[n_, gs_,phi_] := 1+(r/.n->n)*NCm[n, gs, phi];
dNCmdx[n_, gs_, phi_] := (P*Ll*Gl+phi)/(P*L0[phi]*g[n, gs,phi]);
dxdphi[n_,gs_,phi_]:=  D[NCm[n,gs,phi],phi]/dNCmdx[n, gs, phi];
eps[n_,gs_]:=x[0]/. NDSolve[{dxdphi[n,gs,phi]-x'[phi]==0,x[phistarI[n,gs]]==0},x,{phi,0,0.01}];



(* ::Input::Initialization:: *)
"\:0422\:0430\:0431\:043b\:0438\:0447\:043d\:044b\:0435 \:0437\:043d\:0430\:0447\:0435\:043d\:0438\:044f \!\(\*FormBox[SuperscriptBox[\(\[CurlyPhi]\), \(*\)],
TraditionalForm]\)"
(*ListPlot3D[phistar,AxesLabel\[Rule]{Subscript[g, s],n,\[CurlyPhi]^*}, PlotRange\[Rule]{0,1}]*)


(* ::Input::Initialization:: *)
"\:0418\:043d\:0442\:0435\:0440\:043f\:043e\:043b\:0438\:0440\:0443\:044e\:0449\:0430\:044f \:0444\:0443\:043d\:043a\:0446\:0438\:044f \!\(\*FormBox[SuperscriptBox[\(\[CurlyPhi]\), \(*\)],
TraditionalForm]\)"
exportCSV[fileName_, data_]:=Export[fileName, TableForm[Join@@data], "CSV"];

phiIData = Table[phistarI[n,gs],{n,nmin,nmax}, {gs,gsMin,gsMax}];
exportCSV["phi_interpolated.csv", Table[{n, gs, phistarI[n,gs]},{n,nmin,nmax}, {gs,gsMin,gsMax}]];



(* ::Input::Initialization:: *)
(*phiIPlot =Plot3D[phistarI[n,gs],{n,nmin,nmax}, {gs,gsMin,gsMax},AxesLabel\[Rule]{n,Subscript[g, s],\[CurlyPhi]^*}, PlotRange\[Rule]{0,1}];
Export["phi_interpolated.png",phiIPlot];*)


(* ::Input:: *)
(*Show[phiIPlot]*)


(* ::Text:: *)
(*\:0414\:043e\:043b\:044f \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:044b \:043d\:0430 \:0433\:0440\:0430\:043d\:0438\:0446\:0435 \:043a\:0440\:0438\:0441\:0442\:0430\:043b\:043b-\:0434\:0432\:0443\:0445\:0444\:0430\:0437\:043d\:0430\:044f \:0437\:043e\:043d\:0430 \:0432 \:0437\:0430\:0432\:0438\:0441\:0438\:043c\:043e\:0441\:0442\:0438 \:043e\:0442 \:0433\:0440\:0430\:0434\:0438\:0435\:043d\:0442\:0430 \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b \:0432 \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:0435 Subscript[g, s] \:0438 \:043a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442\:0430 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430 \:043e\:0442 \:043b\:0438\:043d\:0435\:0439\:043d\:043e\:0433\:043e \:0432\:0438\:0434\:0430 \[ScriptN]*)
(**)


(* ::Input:: *)
(*Manipulate[Plot3D[phistarI[n,gs],{n,localNInterval[[1]], localNInterval[[2]]}, {gs,localgsInterval[[1]], localgsInterval[[2]]},AxesLabel->{n,\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\),SuperStar[\[CurlyPhi]]}, PlotRange->{0,1}],*)
(*{{localNInterval,{nmin, nmax, 0.2},*)
(*Row[{"\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"}]*)
(*},nmin,nmax,ControlType->IntervalSlider,Appearance->"Paired",Method->"Stop", MinIntervalSize -> 0.2*)
(*},*)
(*{{localgsInterval,{gsMin, gsMax},*)
(*Row[{"\:0413\:0440\:0430\:0434\:0438\:0435\:043d\:0442 \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b \:0432 \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:0435:"}]*)
(*},gsMin,gsMax,0.5,ControlType->IntervalSlider,Appearance->"Paired",Method->"Stop", MinIntervalSize -> 0.2*)
(*}*)
(*]*)
(**)


(* ::Input:: *)
(*Manipulate[*)
(*Plot[{phistarI[n, gs]},{gs,gsMin,7},*)
(*AxesLabel->{\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\),SuperStar[\[CurlyPhi]]}, *)
(*GridLines->Automatic, *)
(*PlotLegends->"n="<>ToString[n]*)
(*], *)
(*{{n,nmin, "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"}, nmin, nmax}]*)


(* ::Input:: *)
(*Manipulate[*)
(*Plot[Evaluate@Table[phistarI[n, gs],{n,chosenN}],{gs,gsMin,5},*)
(*AxesLabel->{\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\),SuperStar[\[CurlyPhi]]},*)
(*PlotLegends->LineLegend[Table[n,{n, chosenN}],LegendLabel->n]],*)
(*{*)
(*{chosenN,{nmin, nmax}, "\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"},*)
(*Range[nmin, nmax],*)
(*ControlType->CheckboxBar*)
(*}*)
(*]*)


(* ::Input:: *)
(*Plot3D[NCm[n,gs, 0],{n,nmin,nmax}, {gs,gsMin,gsMax},AxesLabel->{n,\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\),\!\(TraditionalForm\`\*"\"\<\!\(\*SubscriptBox[\(C\), \(m\)]\)\>\""\)}]*)
(**)


(* ::Text:: *)
(*\:041a\:043e\:043d\:0446\:0435\:043d\:0442\:0440\:0430\:0446\:0438\:044f \:043f\:0440\:0438\:043c\:0435\:0441\:0438 \:0432 \:0434\:0432\:0443\:0445\:0444\:0430\:0437\:043d\:043e\:0439 \:0437\:043e\:043d\:0435 \:0432 \:0437\:0430\:0432\:0438\:0441\:0438\:043c\:043e\:0441\:0442\:0438 \:043e\:0442 \:0433\:0440\:0430\:0434\:0438\:0435\:043d\:0442\:0430 \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b \:0432 \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:0435 Subscript[g, s] \:0438 \:043a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442\:0430 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430 \:043e\:0442 \:043b\:0438\:043d\:0435\:0439\:043d\:043e\:0433\:043e \:0432\:0438\:0434\:0430 \[ScriptN]*)
(**)
(**)


(* ::Input:: *)
(*Manipulate[Plot3D[NCm[n,gs, 0],{n,localNInterval[[1]], localNInterval[[2]]}, {gs,localgsInterval[[1]], localgsInterval[[2]]},AxesLabel->{n,\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\),\!\(TraditionalForm\`\*"\"\<\!\(\*SubscriptBox[\(C\), \(m\)]\)\>\""\)}],*)
(*{{localNInterval,{nmin, nmax},*)
(*Row[{"\:041a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442 \:043e\:0442\:043a\:043b\:043e\:043d\:0435\:043d\:0438\:044f \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \:043b\:0438\:043a\:0432\:0438\:0434\:0443\:0441\:0430:"}]*)
(*},nmin,nmax,1,ControlType->IntervalSlider,Appearance->"Paired",Method->"Stop", MinIntervalSize ->0.5*)
(*},*)
(*{{localgsInterval,{gsMin,gsMax},*)
(*Row[{"\:0413\:0440\:0430\:0434\:0438\:0435\:043d\:0442 \:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b \:0432 \:0442\:0432\:0451\:0440\:0434\:043e\:0439 \:0444\:0430\:0437\:0435:"}]*)
(*},gsMin,gsMax,1,ControlType->IntervalSlider,Appearance->"Paired",Method->"Stop", MinIntervalSize ->0.5*)
(*}*)
(*]*)


(* ::Input:: *)
(*"\:0421\:0442\:0440\:043e\:0438\:043c "\[CurlyEpsilon]*)
(*Plot3D[eps[n,gs],{n,nmin, nmax},{gs,gsMin,gsMax},AxesLabel->{n,Subscript[g, s],\[CurlyEpsilon]}]*)


(* ::Input:: *)
(*Manipulate[Plot3D[eps[n,gs],{n,localNmin, localNmax}, {gs,localgsmin, localgsmax},AxesLabel->{n,Subscript[g, s],\[CurlyEpsilon]}],*)
(*Row[{Control[{{localNmin, nmin,"\!\(\*SubscriptBox[\(n\), \(min\)]\)"},Range[nmin, localNmax-1, 0.5], ControlType -> PopupMenu}],Spacer[50],*)
(*Control[{{localNmax, nmax,"\!\(\*SubscriptBox[\(n\), \(max\)]\)"},Range[localNmin+1, nmax, 0.5], ControlType -> PopupMenu}]}],*)
(*Row[{Control[{{localgsmin, gsMin,"\!\(\*SubscriptBox[SubscriptBox[\(g\), \(s\)], \(min\)]\)"},Range[gsMin, localgsmax-1, 0.5], ControlType -> PopupMenu}],Spacer[50],*)
(*Control[{{localgsmax, gsMax,"\!\(\*SubscriptBox[SubscriptBox[\(g\), \(s\)], \(max\)]\)"},Range[localgsmin+1, gsMax, 0.5], ControlType -> PopupMenu}]}]*)
(*]*)


(* ::Input:: *)
(*"\:0421\:0442\:0440\:043e\:0438\:043c \[Delta][\!\(\**)
(*StyleBox[\"n\",\nFontSlant->\"Italic\"]\), \!\(\*FormBox[SubscriptBox[\(g\), \(s\)],*)
(*TraditionalForm]\)]"*)
(*deltaPlot = Plot3D[Dl/us*eps[n,gs],{n,nmin,nmax},{gs,gsMin,gsMax},AxesLabel->{n,\!\(TraditionalForm\`*)
(*\*SubscriptBox[\(g\), \(s\)]\), \[Delta]}];*)
(*Show[deltaPlot]*)
(*"\!\(\**)
(*StyleBox[\"\:041f\:0440\:043e\:0442\:044f\:0436\:0435\:043d\:043d\:043e\:0441\:0442\:044c\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:043e\:0431\:043b\:0430\:0441\:0442\:0438\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0444\:0430\:0437\:043e\:0432\:043e\:0433\:043e\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:043f\:0435\:0440\:0435\:0445\:043e\:0434\:0430\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0432\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0437\:0430\:0432\:0438\:0441\:0438\:043c\:043e\:0441\:0442\:0438\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:043e\:0442\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0433\:0440\:0430\:0434\:0438\:0435\:043d\:0442\:0430\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0442\:0435\:043c\:043f\:0435\:0440\:0430\:0442\:0443\:0440\:044b\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0432\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0442\:0432\:0435\:0440\:0434\:043e\:0439\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0444\:0430\:0437\:0435\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:043f\:0440\:0438\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\" \",\nFontSlant->\"Italic\"]\)\!\(\*FormBox[\(\*SubscriptBox[\(g\), \(l\)]\(=\)\),*)
(*TraditionalForm]\) "<>StringJoin[ToString[gl]," " ,temperature, "\!\(\**)
(*StyleBox[\"/\",\nFontSlant->\"Italic\"]\)\!\(\**)
(*StyleBox[\"\:0441\:043c\",\nFontSlant->\"Italic\"]\)"]*)


(* ::Input::Initialization:: *)
exportCSV["epsilon.csv", Table[{n, gs, eps[n,gs][[1]]},{n,nmin,nmax}, {gs,gsMin,gsMax}]];
exportCSV["delta.csv", Table[{n, gs, Dl/us*eps[n,gs][[1]]},{n,nmin,nmax}, {gs,gsMin,gsMax}]];


(* ::Text:: *)
(**)
