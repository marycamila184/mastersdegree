fis = readfis('fis_m');
arrayTesteNorm = table2array(testnormalized)
entradaTeste = arrayTesteNorm(:,1:4);
saidaTeste = arrayTesteNorm(:,5);
output = evalfis(fis, entradaTeste)
outputRounded = round(output)
acertos = numel(find(saidaTeste==outputRounded))
accuracy = acertos/275
accuracy
C = confusionmat(saidaTeste,outputRounded)
confusionchart(C)