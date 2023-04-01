from objects.automaton import AFNε, AFN
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        prog="Conversão de AFNe em AFN.",
        description="O programa faz a conversão de automato finito não deterministico com movimento vazio para um automato finito não deterministico.",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        required=True,
        help="Arquivo onde se encontra o automato finito não deterministico com movimento vazio.",
    )

    parser.add_argument(
        "--word",
        "-w",
        type=str,
        required=True,
        help="Palavra a ser testada.",
    )

    args = parser.parse_args()

    afne = AFNε.from_file(args.file)
    afn = afne.to_AFN()

    result = afn.recognize(args.word)

    output = (
        f"A palavra '{args.word}' foi ACEITA pelo automato abaixo:\n\n{str(afn)}."
        if result
        else f"A palavra '{args.word}' NÃO FOI ACEITA pelo automato abaixo:\n\n{str(afn)}"
    )

    print(output)


if __name__ == "__main__":
    main()
