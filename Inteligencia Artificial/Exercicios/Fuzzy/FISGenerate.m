fis = mamfis
fis = mamfis("NumInputs",4,"NumOutputs",1)
fis = mamfis("AndMethod","min","OrMethod","max");
fis = addInput(fis,[0 100],"Name","variance");
fis = addInput(fis,[0 100],"Name","skewness");
fis = addInput(fis,[0 100],"Name","curtosis");
fis = addInput(fis,[0 100],"Name","entropy");
fis = addOutput(fis,[1 2],"Name","cls");

fis = addMF(fis,"variance","trimf",[0 0 54],'Name',"Low");
fis = addMF(fis,"variance","trimf",[0 54 100],'Name',"Medium");
fis = addMF(fis,"variance","trimf",[54 100 100],'Name',"High");

fis = addMF(fis,"skewness","trimf",[0 0 60],'Name',"Low");
fis = addMF(fis,"skewness","trimf",[0 60 100],'Name',"Medium");
fis = addMF(fis,"skewness","trimf",[60 100 100],'Name',"High");

fis = addMF(fis,"curtosis","trimf",[0 0 36],'Name',"Low");
fis = addMF(fis,"curtosis","trimf",[0 36 100],'Name',"Medium");
fis = addMF(fis,"curtosis","trimf",[36 100 100],'Name',"High");

fis = addMF(fis,"entropy","trimf",[0 0 56],'Name',"Low");
fis = addMF(fis,"entropy","trimf",[0 56 100],'Name',"Medium");
fis = addMF(fis,"entropy","trimf",[56 100 100],'Name',"High");

fis = addMF(fis,"cls","trimf",[1 1 2],'Name',"c1");
fis = addMF(fis,"cls","trimf",[1 2 2],'Name',"c2");

ruleedit(fis)