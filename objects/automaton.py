from dataclasses import dataclass


@dataclass
class AFN:
    Q: set  # Conjunto de estados
    Σ: set  # Alfabetos
    δ: dict  # Tabela de transições
    q0: str  # Estado inicial
    F: set  # Estados finais

    def __repr__(self) -> str:
        transitions = list()
        for key in self.δ.keys():
            for char in self.δ[key].keys():
                transitions.append(f"δ({key}, {char}) -> {self.δ[key][char]}")

        transitions_str = "\n".join(transitions)
        attrs = f"Conjunto de estados: {self.Q}\nAlfabeto : {self.Σ}\nTransições:\n{transitions_str}\nEstado inicial: {self.q0}\nConjunto de estados finais: {self.F}"

        return attrs

    def recognize(self, word: str) -> bool:
        Q = {self.q0}

        for char in word:
            new = set()
            for q in Q:
                if char in self.δ[q]:
                    for q1 in self.δ[q][char]:
                        new.add(q1)
            Q = new

        return len(Q & self.F) > 0


@dataclass
class AFNε:
    Q: set  # Conjunto de estados
    Σ: set  # Alfabetos
    δ: dict  # Tabela de transições
    q0: str  # Estado inicial
    F: set  # Estados finais

    @classmethod
    def from_file(cls, filename: str) -> "AFNε":
        with open(filename, "r") as file:
            lines = file.readlines()
            component: dict = dict()
            for line in lines:
                line = "".join(line.split())
                key: str
                values: str
                key, values = line.split(":")
                match key:
                    case "q":
                        component[key] = values
                    case "P":
                        component[key] = dict()
                        productions: list[str] = values.split(";")
                        for production in productions:
                            left: str | list[str]
                            right: str | list[str]
                            left, right = production.split("->")
                            state, char = left.split(",")
                            try:
                                component[key][state][char] = {right}
                            except:
                                component[key][state] = dict()
                                component[key][state][char] = {right}
                    case _:
                        component[key] = set(values.split(","))
        return AFNε(
            component["Q"],
            component["T"],
            component["P"],
            component["q"],
            component["F"],
        )

    def get_ε_reachable(self, state: set) -> set:
        S = set(state)
        queue = list(state)
        while len(queue) > 0:
            q = queue.pop()
            if "ε" in self.δ[q]:
                new = self.δ[q]["ε"] - S
                S.update(new)
                queue.extend(new)

        return S

    def recognize(self, word: str) -> bool:
        Q = self.get_ε_reachable({self.q0})
        for c in word:
            new = set()
            for q in Q:
                if c in self.δ[q]:
                    new.update(self.get_ε_reachable(self.δ[q][c]))

            Q = new
        return len(Q & self.F) > 0

    def to_AFN(self):
        newF = set(self.F)
        newδ = dict()

        for q, t in self.δ.items():
            newδ[q] = dict()
            for symbol, transitions in t.items():
                if symbol != "ε":
                    newδ[q][symbol] = transitions

        for q in self.Q:
            reachable = self.get_ε_reachable({q})
            reachable.remove(q)
            if reachable & self.F:
                newF.add(q)

            for q1 in reachable:
                for sym in self.Σ:
                    if sym not in newδ[q]:
                        newδ[q][sym] = set()
                    newδ[q][sym].add(q1)

        return AFN(self.Q, self.Σ, newδ, self.q0, newF)
