import random
def generate_challenges(total=6):
    challenges = []
    for i in range(total):
        number = random.randint(1, 5)
        challenges.append(number)
    return challenges
