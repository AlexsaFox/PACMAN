FILENAME = 'scoreboard.dat'

def load() -> list[tuple[str, int]]:
    scores = []
    try:
        with open(FILENAME, 'r') as file:
            data = file.read().split('\n')
            for line in data:
                name, result = line.split()
                scores.append((name, int(result)))
    except FileNotFoundError:
        pass
    except ValueError:
        pass
    
    return sorted(scores, key=lambda score: -score[1])

def save(scores: list[tuple[str, int]]):
    with open(FILENAME, 'w') as file:
        for name, result in sorted(scores, key=lambda score: -score[1]):
            file.write(f'{name} {result}\n')

def save_result(name: str, result: int):
    scores = load()
    scores.append((name, result))
    save(scores)
