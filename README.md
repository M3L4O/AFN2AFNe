> A aplicação foi feita utilizando o Python 3.11

Para executar a aplicação é necessário inserir o seguinte comando:

```
python main.py -f <arquivo do AFNe> -w <a palavra que deseja testar>
```

O arquivo que representa o AFNe pode ser escrito da seguinte forma:

```
Q: 0, 1, 2
T: a, b
P: 0, ε -> 1; 0, a -> 0; 1, b -> 1; 1, ε -> 2; 2, a -> 2  
q: 0
F: 2
```

Em que o Q representa os estados, de 0 até N, já T, representa o alfabeto, P as transições, q o estado inicial e, por fim F representa o estado final.

Todas as essa chaves acima descritas devem ser acompanhadas de `:`, já as transições são represetadas por `<estado>, <simbolo> -> <estado alcançado>`, sendo a palavra vazia represetada por `ε`. 
